// Simple UUID generator to avoid external dependency
const generateId = () => Math.random().toString(36).substring(2) + Date.now().toString(36);

// Configuration from environment variables
const AGENT_CONFIG = {
  AGENT_RUNTIME_ARN: import.meta.env.VITE_AGENT_RUNTIME_ARN || '',
  AGENT_ENDPOINT_NAME: import.meta.env.VITE_AGENT_ENDPOINT_NAME || 'DEFAULT',
  AWS_REGION: import.meta.env.VITE_AWS_REGION || 'us-east-1',
  IDENTITY_POOL_ID: import.meta.env.VITE_IDENTITY_POOL_ID || '',
  GUEST_ROLE_ARN: import.meta.env.VITE_GUEST_ROLE_ARN || '',
};

// Bedrock Agent Core endpoint
const BEDROCK_AGENT_CORE_ENDPOINT_URL = `https://bedrock-agentcore.${AGENT_CONFIG.AWS_REGION}.amazonaws.com`;

// --- SigV4 signing utilities ---
async function sha256Hash(data: string): Promise<ArrayBuffer> {
  const encoder = new TextEncoder();
  return crypto.subtle.digest('SHA-256', encoder.encode(data));
}

function toHex(buffer: ArrayBuffer): string {
  return Array.from(new Uint8Array(buffer)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function hmacSha256(key: ArrayBuffer | Uint8Array, data: string): Promise<ArrayBuffer> {
  const keyBuffer = key instanceof Uint8Array ? key.buffer as ArrayBuffer : key;
  const cryptoKey = await crypto.subtle.importKey('raw', keyBuffer, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return crypto.subtle.sign('HMAC', cryptoKey, new TextEncoder().encode(data));
}

interface AwsCredentials {
  accessKeyId: string;
  secretAccessKey: string;
  sessionToken?: string;
}

let cachedCredentials: { creds: AwsCredentials; expiry: number } | null = null;

async function getGuestCredentials(): Promise<AwsCredentials> {
  // Return cached if still valid (refresh 5 min before expiry)
  if (cachedCredentials && Date.now() < cachedCredentials.expiry - 300000) {
    return cachedCredentials.creds;
  }

  const region = AGENT_CONFIG.AWS_REGION;
  const identityPoolId = AGENT_CONFIG.IDENTITY_POOL_ID;

  // Step 1: Get identity ID
  const idRes = await fetch(`https://cognito-identity.${region}.amazonaws.com/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-amz-json-1.1',
      'X-Amz-Target': 'AWSCognitoIdentityService.GetId',
    },
    body: JSON.stringify({ IdentityPoolId: identityPoolId }),
  });
  const idData = await idRes.json();
  if (idData.__type) throw new Error(`Cognito GetId failed: ${idData.message || idData.__type}`);
  const { IdentityId } = idData;

  // Step 2: Get OpenID token (basic/classic auth flow)
  // This avoids the session policy restrictions of GetCredentialsForIdentity (enhanced flow)
  const tokenRes = await fetch(`https://cognito-identity.${region}.amazonaws.com/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-amz-json-1.1',
      'X-Amz-Target': 'AWSCognitoIdentityService.GetOpenIdToken',
    },
    body: JSON.stringify({ IdentityId }),
  });
  const tokenData = await tokenRes.json();
  if (tokenData.__type) throw new Error(`Cognito GetOpenIdToken failed: ${tokenData.message || tokenData.__type}`);
  const { Token } = tokenData;

  // Step 3: Assume the unauthenticated role via STS using the OpenID token
  const stsParams = new URLSearchParams({
    Action: 'AssumeRoleWithWebIdentity',
    Version: '2011-06-15',
    RoleArn: AGENT_CONFIG.GUEST_ROLE_ARN,
    RoleSessionName: 'CognitoGuest',
    WebIdentityToken: Token,
    DurationSeconds: '3600',
  });

  const stsRes = await fetch(`https://sts.${region}.amazonaws.com/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: stsParams.toString(),
  });
  const stsText = await stsRes.text();

  // Parse XML response from STS
  const getXmlValue = (xml: string, tag: string): string => {
    const match = xml.match(new RegExp(`<${tag}>([^<]+)</${tag}>`));
    return match ? match[1] : '';
  };

  if (stsText.includes('<Error>')) {
    const code = getXmlValue(stsText, 'Code');
    const message = getXmlValue(stsText, 'Message');
    throw new Error(`STS AssumeRoleWithWebIdentity failed: ${code} - ${message}`);
  }

  const creds: AwsCredentials = {
    accessKeyId: getXmlValue(stsText, 'AccessKeyId'),
    secretAccessKey: getXmlValue(stsText, 'SecretAccessKey'),
    sessionToken: getXmlValue(stsText, 'SessionToken'),
  };

  const expirationStr = getXmlValue(stsText, 'Expiration');
  const expiry = expirationStr ? new Date(expirationStr).getTime() : Date.now() + 3600000;

  cachedCredentials = { creds, expiry };
  return creds;
}

// URI-encode a string per RFC 3986 (as required by SigV4)
function uriEncode(str: string, encodeSlash = true): string {
  return str.split('').map(ch => {
    if ((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9') ||
        ch === '_' || ch === '-' || ch === '~' || ch === '.') {
      return ch;
    }
    if (ch === '/' && !encodeSlash) return ch;
    return '%' + ch.charCodeAt(0).toString(16).toUpperCase().padStart(2, '0');
  }).join('');
}

async function signRequest(
  method: string,
  url: string,
  headers: Record<string, string>,
  body: string,
  credentials: AwsCredentials,
  region: string,
  service: string,
): Promise<void> {
  const parsedUrl = new URL(url);
  const datetime = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
  const date = datetime.slice(0, 8);

  // Build headers to sign — use lowercase keys throughout to avoid casing mismatches
  const headersToSign: Record<string, string> = {};
  headersToSign['host'] = parsedUrl.host;
  headersToSign['x-amz-date'] = datetime;
  if (credentials.sessionToken) {
    headersToSign['x-amz-security-token'] = credentials.sessionToken;
  }

  // Build sorted signed headers string
  const signedHeaderKeys = Object.keys(headersToSign).sort();
  const signedHeaders = signedHeaderKeys.join(';');
  const canonicalHeaders = signedHeaderKeys
    .map(k => `${k}:${headersToSign[k].trim()}`)
    .join('\n') + '\n';

  // Build canonical URI — each path segment must be URI-encoded, but '/' preserved
  // parsedUrl.pathname already has the encoded ARN, but new URL() decodes %XX sequences,
  // so we need to re-encode each segment individually
  const canonicalUri = '/' + parsedUrl.pathname.slice(1).split('/').map(seg => uriEncode(seg, true)).join('/');

  // Build canonical query string — params sorted by key, each key/value URI-encoded
  const params = [...parsedUrl.searchParams.entries()].sort((a, b) => a[0].localeCompare(b[0]));
  const canonicalQueryString = params
    .map(([k, v]) => `${uriEncode(k)}=${uriEncode(v)}`)
    .join('&');

  const payloadHash = toHex(await sha256Hash(body));

  const canonicalRequest = [
    method,
    canonicalUri,
    canonicalQueryString,
    canonicalHeaders,
    signedHeaders,
    payloadHash,
  ].join('\n');

  const scope = `${date}/${region}/${service}/aws4_request`;
  const stringToSign = [
    'AWS4-HMAC-SHA256',
    datetime,
    scope,
    toHex(await sha256Hash(canonicalRequest)),
  ].join('\n');

  const enc = new TextEncoder();
  const kDate = await hmacSha256(enc.encode(`AWS4${credentials.secretAccessKey}`), date);
  const kRegion = await hmacSha256(kDate, region);
  const kService = await hmacSha256(kRegion, service);
  const kSigning = await hmacSha256(kService, 'aws4_request');
  const signature = toHex(await hmacSha256(kSigning, stringToSign));

  // Set the signing headers on the outgoing request headers object
  headers['x-amz-date'] = datetime;
  if (credentials.sessionToken) {
    headers['x-amz-security-token'] = credentials.sessionToken;
  }
  headers['Authorization'] = `AWS4-HMAC-SHA256 Credential=${credentials.accessKeyId}/${scope}, SignedHeaders=${signedHeaders}, Signature=${signature}`;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  thinkingContent?: string;
  isStreaming?: boolean;
  status?: string;
  // Fields for loop management
  previousLoops?: string[];  // Array of previous loop contents
  currentLoop?: string;      // Current active loop content
  // Fields for subagent tracking
  subagentSteps?: SubagentStep[];  // Track subagent activities
  currentSubagent?: {
    name: string;
    input: string;
    tool?: string;
    content?: string;  // Current streaming content
  };

}

export interface SubagentStep {
  agentName: string;
  input: string;
  content: string;
  tools?: string[];
  timestamp: number;
}

// Helper to check if a line should be skipped (noise from backend)
const shouldSkipLine = (line: string): boolean => {
  // Skip Python repr strings (raw Strands events with non-serializable objects)
  if (line.startsWith("\"{'") || line.startsWith("{'")) return true;
  
  // Skip control events
  if (line.includes('"init_event_loop"') || 
      line.includes('"start": true') ||
      line.includes('"start_event_loop"')) return true;
  
  return false;
};

/**
 * Invokes the agent core functionality with streaming support
 */
export const invokeAgentCore = async (
  query: string,
  userId: string,
  sessionId: string,
  setAnswers: (updater: (prev: ChatMessage[]) => ChatMessage[]) => void,
): Promise<{
  sessionId: string;
  completion: string;
}> => {
  try {
    console.log('Invoking agent core with query:', query);

    // URL encode the agent ARN
    const escapedAgentArn = encodeURIComponent(AGENT_CONFIG.AGENT_RUNTIME_ARN);
    
    // Construct the URL
    const url = `${BEDROCK_AGENT_CORE_ENDPOINT_URL}/runtimes/${escapedAgentArn}/invocations?qualifier=${AGENT_CONFIG.AGENT_ENDPOINT_NAME}`;

    // Generate a proper trace ID
    const traceId = `1-${Math.floor(Date.now() / 1000).toString(16)}-${generateId()}`;
    
    // Set up headers and sign with SigV4 using Cognito guest credentials
    const headers: Record<string, string> = {
      "X-Amzn-Trace-Id": traceId,
      "Content-Type": "application/json",
      "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": sessionId,
      "Accept": "application/json, text/event-stream",
    };

    // Create the payload
    const payload = {
      prompt: query,
      user_id: userId,
      session_id: sessionId
    };

    const bodyStr = JSON.stringify(payload);

    // Sign the request with SigV4 using Cognito guest credentials
    if (!AGENT_CONFIG.IDENTITY_POOL_ID) {
      throw new Error(
        'VITE_IDENTITY_POOL_ID is not configured. Deploy the Amplify backend first, ' +
        'then run ./scripts/setup-web-ui-env.sh --force to update your .env.local.'
      );
    }
    if (AGENT_CONFIG.IDENTITY_POOL_ID === 'REPLACE_AFTER_AMPLIFY_DEPLOY') {
      throw new Error(
        'VITE_IDENTITY_POOL_ID is still set to the placeholder value. Deploy the Amplify backend first ' +
        '(npx ampx sandbox or npx ampx deploy), then update VITE_IDENTITY_POOL_ID in web-ui/.env.local ' +
        'with the Identity Pool ID from the CloudFormation outputs.'
      );
    }
    const creds = await getGuestCredentials();
    await signRequest('POST', url, headers, bodyStr, creds, AGENT_CONFIG.AWS_REGION, 'bedrock-agentcore');

    console.log('Agent Core Payload:', payload);

    // Remove host header — browsers set this automatically and reject manual overrides
    delete headers['host'];

    // Make HTTP request with streaming
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: bodyStr,
    });

    console.log(`Response Status: ${response.status}`);
    console.log(`Response Headers:`, Object.fromEntries(response.headers.entries()));
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`❌ HTTP Error ${response.status}:`, errorText);
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    let completion = '';
    let messageInitialized = false;
    let isCompleted = false;
    
    // Loop tracking variables
    let previousLoops: string[] = [];
    
    // Thinking detection variables
    let isInThinking = false;
    let thinkingContent = '';
    let regularContent = '';
    let endTagBuffer = '';
    
    // Tool/subagent tracking
    let currentToolUse = '';
    let subagentSteps: SubagentStep[] = [];
    let currentSubagentContent = '';

    // Initialize streaming output
    console.log('------- Agent Response (Streaming) -------');

    try {
      if (response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;
            
            // Process complete lines
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';
            
            for (const line of lines) {
              if (!line.trim()) continue;
              
              try {
                // Handle Server-Sent Events format - strip "data: " prefix
                let jsonString = line;
                if (line.startsWith('data: ')) {
                  jsonString = line.substring(6);
                }
                
                // Skip [DONE] messages
                if (jsonString === '[DONE]') continue;
                
                // Skip noise (Python repr strings, control events)
                if (shouldSkipLine(jsonString)) continue;
                
                // Check for throttled delay event
                if (line.includes('event_loop_throttled_delay')) {
                  if (messageInitialized) {
                    setAnswers((prevState) => {
                      const newState = [...prevState];
                      for (let i = newState.length - 1; i >= 0; i--) {
                        if (newState[i].isStreaming) {
                          newState[i] = { ...newState[i], status: 'Server is busy' };
                          break;
                        }
                      }
                      return newState;
                    });
                  }
                  continue;
                }
                
                // Parse JSON
                let chunkData;
                try {
                  chunkData = JSON.parse(jsonString);
                } catch {
                  continue; // Skip non-JSON lines
                }
                
                // Skip if already completed
                if (isCompleted) continue;
                
                // Initialize message on first content
                if (!messageInitialized && (
                  chunkData.event?.contentBlockDelta?.delta?.text ||
                  chunkData.event?.messageStart ||
                  chunkData.event?.contentBlockStart?.start?.toolUse
                )) {
                  messageInitialized = true;
                  setAnswers((prevState) => [
                    ...prevState,
                    { 
                      id: generateId(),
                      role: 'assistant',
                      content: '', 
                      isStreaming: true,
                      status: 'Streaming...',
                      subagentSteps: []
                    },
                  ]);
                }
                
                // Handle text streaming (contentBlockDelta)
                if (chunkData.event?.contentBlockDelta?.delta?.text) {
                  const chunkText = chunkData.event.contentBlockDelta.delta.text;
                  completion += chunkText;
                  
                  // Thinking tag detection
                  if (chunkText.includes('<thinking') && !isInThinking) {
                    isInThinking = true;
                  }
                  
                  if (isInThinking) {
                    thinkingContent += chunkText;
                    endTagBuffer += chunkText;
                    if (endTagBuffer.includes('</thinking>')) {
                      isInThinking = false;
                      endTagBuffer = '';
                    }
                    if (endTagBuffer.length > 15) {
                      endTagBuffer = endTagBuffer.slice(-15);
                    }
                  } else {
                    regularContent += chunkText;
                  }
                  
                  setAnswers((prevState) => {
                    const newState = [...prevState];
                    for (let i = newState.length - 1; i >= 0; i--) {
                      if (newState[i].isStreaming) {
                        newState[i] = {
                          ...newState[i],
                          content: regularContent,
                          currentLoop: regularContent,
                          previousLoops: [...previousLoops],
                          thinkingContent: thinkingContent || undefined,
                          status: isInThinking ? 'Thinking...' : 'Streaming...'
                        };
                        break;
                      }
                    }
                    return newState;
                  });
                }
                
                // Handle tool call starting (contentBlockStart with toolUse)
                else if (chunkData.event?.contentBlockStart?.start?.toolUse) {
                  const toolUse = chunkData.event.contentBlockStart.start.toolUse;
                  currentToolUse = toolUse.name;
                  currentSubagentContent = '';
                  console.log(`Tool call starting: ${toolUse.name}`);
                  
                  setAnswers((prevState) => {
                    const newState = [...prevState];
                    for (let i = newState.length - 1; i >= 0; i--) {
                      if (newState[i].isStreaming) {
                        newState[i] = {
                          ...newState[i],
                          status: `Using ${toolUse.name}`,
                          currentSubagent: {
                            name: toolUse.name,
                            input: '',
                            content: ''
                          }
                        };
                        break;
                      }
                    }
                    return newState;
                  });
                }
                
                // Handle messageStop for loop transitions and completion
                else if (chunkData.event?.messageStop) {
                  if (chunkData.event.messageStop.stopReason !== 'end_turn') {
                    console.log('Loop transition detected - tool use cycle');
                    // Move current content to previous loops if there's content
                    if (regularContent.trim().length > 0) {
                      previousLoops.push(regularContent.trim());
                      regularContent = '';
                    }
                    
                    setAnswers((prevState) => {
                      const newState = [...prevState];
                      for (let i = newState.length - 1; i >= 0; i--) {
                        if (newState[i].isStreaming) {
                          newState[i] = {
                            ...newState[i],
                            content: regularContent,
                            currentLoop: regularContent,
                            previousLoops: [...previousLoops],
                            status: currentToolUse ? `Using ${currentToolUse}` : 'Processing...'
                          };
                          break;
                        }
                      }
                      return newState;
                    });
                  } else {
                    // Final completion
                    console.log('Message completion detected');
                    isCompleted = true;
                    
                    setAnswers((prevState) => {
                      const newState = [...prevState];
                      for (let i = newState.length - 1; i >= 0; i--) {
                        if (newState[i].isStreaming) {
                          newState[i] = {
                            ...newState[i],
                            content: regularContent,
                            currentLoop: regularContent,
                            previousLoops: [...previousLoops],
                            thinkingContent: thinkingContent || undefined,
                            subagentSteps: subagentSteps.length > 0 ? subagentSteps : undefined,
                            isStreaming: false,
                            status: 'complete'
                          };
                          break;
                        }
                      }
                      return newState;
                    });
                  }
                }
                
                // Handle tool_stream_event - subagent streaming
                else if (chunkData.tool_stream_event) {
                  const toolStreamEvent = chunkData.tool_stream_event;
                  const toolUseInfo = toolStreamEvent.tool_use;
                  const streamData = toolStreamEvent.data;
                  
                  // Update current tool if provided
                  if (toolUseInfo?.name && toolUseInfo.name !== currentToolUse) {
                    currentToolUse = toolUseInfo.name;
                  }
                  
                  // Handle streaming text from subagent
                  if (streamData?.data && typeof streamData.data === 'string') {
                    currentSubagentContent += streamData.data;
                    
                    setAnswers((prevState) => {
                      const newState = [...prevState];
                      for (let i = newState.length - 1; i >= 0; i--) {
                        if (newState[i].isStreaming) {
                          newState[i] = {
                            ...newState[i],
                            status: `${currentToolUse}: working...`,
                            currentSubagent: {
                              name: currentToolUse,
                              input: toolUseInfo?.input ? JSON.stringify(toolUseInfo.input) : '',
                              content: currentSubagentContent
                            }
                          };
                          break;
                        }
                      }
                      return newState;
                    });
                  }
                  
                  // Handle subagent result
                  if (streamData?.result) {
                    // Save completed subagent step
                    subagentSteps.push({
                      agentName: currentToolUse,
                      input: toolUseInfo?.input ? JSON.stringify(toolUseInfo.input) : '',
                      content: currentSubagentContent || String(streamData.result),
                      timestamp: Date.now()
                    });
                    
                    setAnswers((prevState) => {
                      const newState = [...prevState];
                      for (let i = newState.length - 1; i >= 0; i--) {
                        if (newState[i].isStreaming) {
                          newState[i] = {
                            ...newState[i],
                            subagentSteps: [...subagentSteps],
                            currentSubagent: undefined,
                            status: 'Processing result...'
                          };
                          break;
                        }
                      }
                      return newState;
                    });
                    
                    currentSubagentContent = '';
                  }
                }
                

                
              } catch (parseError) {
                console.error('Error parsing streaming chunk:', parseError);
              }
            }
          }
        } finally {
          reader.releaseLock();
        }
      } else {
        // Handle non-streaming response (fallback)
        const responseText = await response.text();
        completion = responseText;
        console.log('Agent Response Text (Non-streaming):', completion);

        setAnswers((prevState) => [
          ...prevState,
          { 
            id: generateId(),
            role: 'assistant',
            content: completion, 
            isStreaming: false,
            status: 'complete'
          },
        ]);
      }
    } catch (streamError) {
      console.error('Error processing agent response stream:', streamError);
      throw streamError;
    }

    // Ensure streaming is marked complete
    if (!isCompleted && messageInitialized) {
      setAnswers((prevState) => {
        const newState = [...prevState];
        for (let i = newState.length - 1; i >= 0; i--) {
          if (newState[i].isStreaming && newState[i].status !== 'complete') {
            newState[i] = {
              ...newState[i],
              isStreaming: false,
              status: 'complete'
            };
            break;
          }
        }
        return newState;
      });
    }

    console.log('------- End of Agent Response -------');
    
    return {
      sessionId: sessionId,
      completion,
    };
  } catch (error) {
    console.error('❌ Error invoking agent core:', error);
    console.error('❌ Error details:', JSON.stringify(error, Object.getOwnPropertyNames(error as object), 2));
    
    const errorMessage = error instanceof Error ? error.message : String(error);
    
    setAnswers((prevState) => [
      ...prevState,
      {
        id: generateId(),
        role: 'assistant',
        content: `Error: ${errorMessage}`,
        isStreaming: false,
      },
    ]);
    
    throw error;
  }
};

/**
 * Get current agent configuration
 */
export const getCurrentAgentConfig = () => AGENT_CONFIG;

/**
 * Update agent configuration (for runtime configuration)
 */
export const updateAgentConfig = (newConfig: Partial<typeof AGENT_CONFIG>) => {
  Object.assign(AGENT_CONFIG, newConfig);
};
