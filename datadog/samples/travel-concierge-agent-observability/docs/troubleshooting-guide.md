# Troubleshooting Guide — Datadog LLM Observability for Travel Concierge Agent

This guide walks through three real-world debugging scenarios using Datadog APM and LLM Observability to diagnose issues in the travel concierge multi-agent system.

---

## Scenario 1: Slow Flight Search

**Symptom:** A user asks *"Find flights from NYC to Tokyo next week"* and the response takes 15+ seconds instead of the expected 5–8 seconds.

### What to Look For

- A single span in the trace waterfall consuming disproportionate time
- The `travel_flight_search` MCP tool call taking longer than expected
- Possible slow external API call (SerpAPI) or an extra LLM round-trip

### Step-by-Step Diagnosis

#### 1. Open the Trace in Datadog APM

Navigate to **APM → Traces** and filter:
- `service:supervisor-agent`
- `@duration:>10s`

Click the slow trace to open the waterfall view.

#### 2. Read the Span Waterfall

The waterfall for a slow flight search typically looks like:

```
supervisor-agent                                    ████████████████████████  15.2s
├── LLM: bedrock.converse (routing)                 ██                        1.8s
├── strands.tool: travel_assistant                  ██████████████████████    13.1s
│   ├── LLM: bedrock.converse (plan)                ██                        1.5s
│   ├── MCP tool: travel_flight_search              ████████████              8.2s  ← BOTTLENECK
│   │   └── travel-mcp-server                       ████████████              8.0s
│   │       └── HTTP GET serpapi.com                 ██████████                7.5s  ← ROOT CAUSE
│   └── LLM: bedrock.converse (synthesize)          ████                      3.2s
```

In this example, the SerpAPI external call is the bottleneck at 7.5s.

#### 3. Drill Into the MCP Server Span

Click the `travel-mcp-server` span to inspect:
- **Resource:** `travel_flight_search`
- **Duration:** 8.0s
- **Tags:** `departure_id:JFK`, `arrival_id:NRT`, `outbound_date:2025-12-10`
- **Child spans:** Look for the HTTP call to the external search API

#### 4. Check for Bedrock Latency

If the bottleneck is instead on an LLM span:
- Click the `bedrock.converse` span
- Check `@meta.model_id` — confirm it's `us.anthropic.claude-sonnet-4-5-20250929-v1:0`
- Check `@meta.token_usage.output_tokens` — a very high output token count (>2000) can indicate the model is generating an overly verbose response
- Check `@duration` — Bedrock p99 latency for Claude Sonnet 4.5 is typically 3–8s depending on output length

#### 5. Resolution Steps

| Root Cause | Fix |
|-----------|-----|
| Slow SerpAPI response | Add timeout to the `travel_flight_search` tool (currently no timeout). Consider caching frequent routes. |
| High Bedrock latency on synthesis | Reduce the system prompt length in `travel_subagent.py`. The travel subagent prompt is ~800 tokens — trim unnecessary instructions. |
| Extra LLM round-trip | Check if the subagent is making multiple `bedrock.converse` calls. If the model is asking for clarification instead of calling the tool directly, tighten the system prompt. |
| Gateway routing delay | Check the `AgentCore Gateway` span. If >500ms, this may indicate a cold start on the MCP server container. |

---

## Scenario 2: High Token Usage

**Symptom:** Datadog LLM Observability shows the `travel-concierge-agent` ML app is consuming 500K+ tokens per hour, driving up Bedrock costs. You need to identify which subagent and which prompts are the most expensive.

### What to Look For

- Which subagent or tool call generates the most tokens
- Which specific LLM calls have the highest `input_tokens` + `output_tokens`
- Whether system prompts are unnecessarily large
- Whether the supervisor is making redundant routing calls

### Step-by-Step Diagnosis

#### 1. Open LLM Observability Dashboard

Navigate to **LLM Observability → Clusters** (or **LLM Observability → Traces**):
- Filter by `ml_app:travel-concierge-agent`
- Sort by **Total Tokens** (descending)

This shows the most expensive traces at the top.

#### 2. Compare Subagent Token Usage

In **LLM Observability → Traces**, group by `service`:

| Service | Avg Input Tokens | Avg Output Tokens | Avg Total | Calls/hr |
|---------|-----------------|-------------------|-----------|----------|
| `supervisor-agent` | 800 | 50 | 850 | 120 |
| `supervisor-agent` (travel_assistant) | 3,200 | 600 | 3,800 | 80 |

In this example, `travel_assistant` subagent calls are consuming the most tokens per call.

#### 3. Identify Expensive Prompts

Click into a high-token `travel_assistant` trace. In the LLM span details, examine:

- **Input tab:** Shows the full prompt sent to Bedrock. Look for:
  - System prompt size (the `TRAVEL_AGENT_PROMPT` in `travel_subagent.py`)
  - Conversation history being passed (AgentCore Memory injects prior turns)
  - Tool results being fed back (flight search results can be 2000+ tokens)

- **Output tab:** Shows the model's response. Look for:
  - Overly verbose formatting (the model may be generating markdown tables, bullet lists, etc.)
  - Repeated information from the input

#### 4. Find the Biggest Offenders

Use **LLM Observability → Analytics** to create a query:
```
@type:llm @ml_app:travel-concierge-agent
| group by @meta.model_id
| measure avg(@meta.token_usage.total_tokens), sum(@meta.token_usage.total_tokens)
```

This reveals:
- Average tokens per call by model
- Total token consumption over the selected time window

#### 5. Resolution Steps

| Root Cause | Fix |
|-----------|-----|
| Large system prompts | The `TRAVEL_AGENT_PROMPT` in `travel_subagent.py` contains detailed instructions. Trim to essentials — move examples to few-shot format or a separate retrieval step. |
| Tool results inflating context | Flight/hotel search results can return 10+ options with full details. Limit results to top 5 in the MCP tool response before returning to the agent. |
| Conversation history growth | AgentCore Memory injects all prior turns. For long sessions, token count grows linearly. Consider summarizing history after N turns. |
| Redundant supervisor routing | Each user message triggers a supervisor `bedrock.converse` call just to route. If the conversation is clearly in a travel context, consider sticky routing to avoid the extra LLM call. |
| Verbose model output | Add `"Be concise. Use bullet points."` to the system prompt. Or reduce `temperature` (currently 0.1 in `agent.py` — already low, so this is likely not the issue). |

---

## Scenario 3: Agent Error Debugging

**Symptom:** A user asks *"Find hotels in Tokyo for next week"* and receives an error: *"Sorry, I encountered an error processing your request."* You need to trace the error back to its root cause.

### What to Look For

- An error span (red) in the trace waterfall
- The error message and stack trace on the failing span
- Whether the error originated in the supervisor, a subagent, an MCP tool, or a Bedrock call
- Trace correlation between the supervisor-agent and MCP server services

### Step-by-Step Diagnosis

#### 1. Find the Error Trace

Navigate to **APM → Traces** and filter:
- `service:supervisor-agent`
- `status:error`

Or use **APM → Error Tracking** to see aggregated error patterns. Click the relevant error group to see individual traces.

#### 2. Read the Error Span Waterfall

A typical error trace for a failed hotel search:

```
supervisor-agent                                    ████████████ ERROR        6.1s
├── LLM: bedrock.converse (routing)                 ██                        1.5s
├── strands.tool: travel_assistant                  ████████ ERROR            4.2s
│   ├── LLM: bedrock.converse (plan)                ██                        1.2s
│   ├── MCP tool: travel_hotel_search               ████ ERROR                2.5s
│   │   └── travel-mcp-server                       ████ ERROR                2.3s
│   │       └── HTTP GET amadeus.com                █ ERROR                   0.1s  ← ROOT CAUSE
│   └── LLM: bedrock.converse (error handling)      ██                        0.5s
```

The error propagates upward: `HTTP GET amadeus.com` → `travel-mcp-server` → `travel_hotel_search` → `travel_assistant` → `supervisor-agent`.

#### 3. Inspect the Failing Span

Click the `travel-mcp-server` error span. In the **Error** tab:

- **Error Type:** `requests.exceptions.HTTPError`
- **Error Message:** `401 Unauthorized — Amadeus API token expired`
- **Stack Trace:** Points to `tools.py` in the travel MCP server

This tells you the travel MCP server's Amadeus API token has expired and needs to be refreshed.

#### 4. Check the MCP Tool Input

On the `travel_hotel_search` span, inspect the **Meta** tags:
- `@meta.input` — Shows what the subagent passed to the tool:
  ```json
  {
    "city_code": "TYO",
    "ratings": "4,5",
    "max_price": 500
  }
  ```
- The input parameters look valid — the issue is with the external API authentication.

#### 5. Trace the Error Origin

Walk backward through the spans:

1. **HTTP GET amadeus.com** failed with 401 Unauthorized
2. **travel-mcp-server** propagated the error without a fallback
3. **travel_assistant subagent** received the error from the MCP tool
4. **supervisor-agent** received the error and returned a generic error message to the user

#### 6. Cross-Service Trace Correlation

If the error span in `supervisor-agent` doesn't show the full MCP server details:

1. Copy the **Trace ID** from the supervisor trace
2. Go to **APM → Traces** and search by trace ID
3. The trace should show spans from both `supervisor-agent` and `travel-mcp-server` services
4. If spans are in separate traces (context propagation gap), correlate by timestamp and `user_id` tag

#### 7. Check Bedrock Error Responses

If the error is on a `bedrock.converse` span instead:

- **Error Type:** `ThrottlingException` — You've hit Bedrock rate limits. Check your account's tokens-per-minute quota.
- **Error Type:** `ModelTimeoutException` — The model took too long. This can happen with very large prompts (>100K tokens).
- **Error Type:** `ValidationException` — The prompt format is invalid. Check that the message structure matches the Converse API schema.

#### 8. Resolution Steps

| Root Cause | Fix |
|-----------|-----|
| Expired API credentials | Refresh the Amadeus API token. Consider implementing automatic token refresh in the MCP tool handler. |
| LLM not extracting required fields | Update the system prompts in subagent files to explicitly instruct the model to include required fields. |
| DynamoDB schema mismatch | Check the DynamoDB table schema in the Amplify backend (`amplify/data/resource.ts`). Ensure the model allows optional fields or has defaults. |
| Bedrock throttling | Request a quota increase for your Bedrock model in the AWS console. Or add retry logic with exponential backoff in `gateway_client.py`. |
| Context propagation gap | Ensure `ddtrace` is patching `requests` / `httpx` in both the supervisor and MCP servers. The `ddtrace-run` wrapper should handle this automatically, but verify with `DD_TRACE_DEBUG=true`. |

---

## General Debugging Tips

### Useful Datadog Filters

| What You Want | Where to Go | Filter |
|--------------|-------------|--------|
| All traces for a user session | APM → Traces | `@user.id:<user-id>` |
| Slow requests | APM → Traces | `service:supervisor-agent @duration:>10s` |
| Error traces | APM → Traces | `service:supervisor-agent status:error` |
| High-token LLM calls | LLM Observability → Traces | `@ml_app:travel-concierge-agent` sort by tokens |
| Specific MCP tool calls | APM → Traces | `resource_name:travel_flight_search` |
| Bedrock latency | APM → Traces | `service:supervisor-agent @span.type:llm` |

### Enabling Debug Logging

To get verbose `ddtrace` output for diagnosing instrumentation issues, set these environment variables in the Dockerfile:

```dockerfile
ENV DD_TRACE_DEBUG=true
ENV DD_LOG_LEVEL=DEBUG
```

Then check the container logs:
```bash
# For supervisor agent
aws logs tail /aws/bedrock-agentcore/supervisor-agent --follow

# For MCP servers
aws logs tail /aws/bedrock-agentcore/travel-mcp-server --follow
```

### Verifying Trace Propagation

To confirm traces are flowing from all services:

1. Go to **APM → Service Map**
2. Verify all three services appear: `supervisor-agent`, `travel-mcp-server`, `itinerary-mcp-server`
3. Verify edges connect `supervisor-agent` → each MCP server
4. If a service is missing, check that its container is running and `DD_API_KEY` is set correctly

### Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| No traces in Datadog | `DD_API_KEY` not set or invalid | Verify the Secrets Manager secret `datadog/aig-agent/api-key` exists and the container has `secretsmanager:GetSecretValue` permission |
| Traces appear but no LLM spans | `DD_LLMOBS_ENABLED` not set | Confirm the Dockerfile has `ENV DD_LLMOBS_ENABLED=1` |
| Duplicate or garbled traces | ADOT and ddtrace both instrumenting | Set `DISABLE_ADOT_OBSERVABILITY=true` in Dockerfiles and CDK env vars to disable AgentCore's built-in ADOT pipeline |
| Separate traces per service (no correlation) | Context propagation broken | Ensure `ddtrace-run` is the entrypoint wrapper and `botocore` + `requests` are being patched |
| LLM spans missing input/output text | Datadog plan limitation | LLM Observability prompt/completion capture requires a Datadog plan that includes LLM Observability |
| High cardinality warnings | Too many unique resource names | This is normal for LLM workloads — each unique prompt creates a resource. Use `DD_TRACE_RESOURCE_QUERY_STRING_ENABLED=false` if needed |
