import { useState, useEffect, useRef, useMemo } from 'react'
import { invokeAgentCore, type ChatMessage, type SubagentStep } from '../services/awsCalls'
import { type Session, createSession, saveMessage } from '../services/bedrockSessionService'
import { submitFeedback } from '../services/feedbackService'
import { showToast } from '../utils/toast'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

// Component for rendering thinking content
const ThinkingSection = ({ thinkingContent }: { thinkingContent: string }) => {
  const cleanContent = thinkingContent
    .replace(/<thinking>/g, '')
    .replace(/<\/thinking>/g, '')
    .trim()
    .replace(/\n\s*\n/g, '\n')
    .replace(/^\s+/gm, '')
    .replace(/\s+$/gm, '')

  return (
    <div className="thinking-section">
      <details className="thinking-details">
        <summary className="thinking-summary">💭 Thinking...</summary>
        <div className="thinking-content">
          <div className="thinking-text">
            {cleanContent.split('\n').filter(line => line.trim()).map((line, index) => (
              <p key={index} className="thinking-paragraph">
                {line}
              </p>
            ))}
          </div>
        </div>
      </details>
    </div>
  )
}


// Component for rendering previous loops and subagent steps
const PreviousLoopsSection = ({ 
  previousLoops, 
  subagentSteps,
  currentSubagent
}: { 
  previousLoops?: string[];
  subagentSteps?: SubagentStep[];
  currentSubagent?: {
    name: string;
    input: string;
    tool?: string;
    content?: string;
  };
}) => {
  const hasLoops = previousLoops && previousLoops.length > 0;
  const hasSubagentSteps = subagentSteps && subagentSteps.length > 0;
  const hasCurrentSubagent = currentSubagent && currentSubagent.content;
  
  if (!hasLoops && !hasSubagentSteps && !hasCurrentSubagent) return null;

  const totalSteps = (previousLoops?.length || 0) + (subagentSteps?.length || 0) + (hasCurrentSubagent ? 1 : 0);

  return (
    <div className="previous-loops-section">
      <details className="previous-loops-details">
        <summary className="previous-loops-summary">
          🔄 Previous processing steps ({totalSteps})
        </summary>
        <div className="previous-loops-content">
          {previousLoops?.map((loopContent, index) => (
            <div key={`loop-${index}`} className="previous-loop-item">
              <div className="previous-loop-header">Processing Step {index + 1}</div>
              <div className="previous-loop-content">
                <MarkdownRenderer content={loopContent} isAssistant={true} />
              </div>
            </div>
          ))}
          
          {subagentSteps?.map((step, index) => (
            <div key={`subagent-${index}`} className="previous-loop-item subagent-step">
              <div className="previous-loop-header">
                🤖 {step.agentName}
              </div>
              <div className="subagent-input">
                <strong>Input:</strong> {step.input}
              </div>
              <div className="previous-loop-content">
                <MarkdownRenderer content={step.content} isAssistant={true} />
              </div>
            </div>
          ))}
          
          {currentSubagent && currentSubagent.content && (
            <div className="previous-loop-item subagent-step current-subagent">
              <div className="previous-loop-header">
                🤖 {currentSubagent.name} (streaming...)
              </div>
              <div className="subagent-input">
                <strong>Input:</strong> {currentSubagent.input}
              </div>
              <div className="previous-loop-content">
                <MarkdownRenderer content={currentSubagent.content} isAssistant={true} />
                <span className="streaming-cursor">|</span>
              </div>
            </div>
          )}
        </div>
      </details>
    </div>
  )
}


// Enhanced markdown renderer component
const MarkdownRenderer = ({ content, isAssistant = false }: { content: string; isAssistant?: boolean }) => {
  if (!content) return null

  const processedContent = isAssistant ? content.trim() : content

  return (
    <div className="markdown-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          h1: ({ children }) => <h1 className="markdown-h1">{children}</h1>,
          h2: ({ children }) => <h2 className="markdown-h2">{children}</h2>,
          h3: ({ children }) => <h3 className="markdown-h3">{children}</h3>,
          h4: ({ children }) => <h4 className="markdown-h4">{children}</h4>,
          h5: ({ children }) => <h5 className="markdown-h5">{children}</h5>,
          h6: ({ children }) => <h6 className="markdown-h6">{children}</h6>,
          p: ({ children }) => <p className="markdown-p">{children}</p>,
          ul: ({ children }) => <ul className="markdown-ul">{children}</ul>,
          ol: ({ children }) => <ol className="markdown-ol">{children}</ol>,
          li: ({ children }) => <li className="markdown-li">{children}</li>,
          code: ({ className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || '')
            const isInline = !match
            return isInline ? (
              <code className="markdown-inline-code" {...props}>{children}</code>
            ) : (
              <pre className="markdown-pre">
                <code className={`markdown-code ${className}`} {...props}>{children}</code>
              </pre>
            )
          },
          blockquote: ({ children }) => <blockquote className="markdown-blockquote">{children}</blockquote>,
          table: ({ children }) => <table className="markdown-table">{children}</table>,
          thead: ({ children }) => <thead className="markdown-thead">{children}</thead>,
          tbody: ({ children }) => <tbody className="markdown-tbody">{children}</tbody>,
          tr: ({ children }) => <tr className="markdown-tr">{children}</tr>,
          th: ({ children }) => <th className="markdown-th">{children}</th>,
          td: ({ children }) => <td className="markdown-td">{children}</td>,
          a: ({ href, children }) => (
            <a href={href} className="markdown-link" target="_blank" rel="noopener noreferrer">{children}</a>
          ),
          strong: ({ children }) => <strong className="markdown-strong">{children}</strong>,
          em: ({ children }) => <em className="markdown-em">{children}</em>,
          hr: () => <hr className="markdown-hr" />,
        }}
      >
        {processedContent}
      </ReactMarkdown>
    </div>
  )
}


interface User {
  username: string
  email?: string
  userId: string
  name?: string
}

interface ChatProps {
  user: User
  onSignOut: () => void
  currentSession: Session | null
  sessions?: Session[]
  onSwitchSession?: (sessionId: string) => void
  getMessages: (sessionId: string) => Promise<ChatMessage[]>
  refreshSessions?: () => Promise<void>
  updateCurrentSession?: (session: Session) => void
  onMessagesUpdate?: (messages: ChatMessage[]) => void
  triggerMessage?: { message: string; timestamp: number }
  onNewChat?: () => void
  canStartNewChat?: boolean
}

const Chat = ({ user, currentSession, sessions = [], onSwitchSession, getMessages, refreshSessions, updateCurrentSession, onMessagesUpdate, onNewChat, canStartNewChat = true }: ChatProps) => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [copiedMessageId, setCopiedMessageId] = useState<string>('')
  const [showCommentBox, setShowCommentBox] = useState<string>('')
  const [feedbackComment, setFeedbackComment] = useState('')
  const [feedbackType, setFeedbackType] = useState<'up' | 'down' | null>(null)
  const [submittingFeedback, setSubmittingFeedback] = useState<string>('')
  const [messageFeedback, setMessageFeedback] = useState<Record<string, { feedback: 'up' | 'down', comment?: string }>>({})
  const [showSessionDropdown, setShowSessionDropdown] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const messagesContainerRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const sessionDropdownRef = useRef<HTMLDivElement>(null)


  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (sessionDropdownRef.current && !sessionDropdownRef.current.contains(event.target as Node)) {
        setShowSessionDropdown(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Notify parent when messages change
  useEffect(() => {
    if (onMessagesUpdate) {
      onMessagesUpdate(messages)
    }
  }, [messages, onMessagesUpdate])

  // Helper function to extract thinking content from message
  const extractThinkingContent = (content: string): { mainContent: string; thinkingContent?: string } => {
    const thinkingRegex = /<thinking>([\s\S]*?)<\/thinking>/g
    const matches = content.match(thinkingRegex)
    
    if (matches && matches.length > 0) {
      const thinkingContent = matches.join('\n')
      const mainContent = content.replace(thinkingRegex, '').trim()
      return { mainContent, thinkingContent }
    }
    
    return { mainContent: content }
  }

  // Load messages when switching sessions
  useEffect(() => {
    const loadMessages = async () => {
      if (currentSession && !currentSession.isTemporary) {
        try {
          const sessionMessages = await getMessages(currentSession.id)
          const convertedMessages: ChatMessage[] = sessionMessages.map(msg => {
            if (msg.role === 'assistant') {
              const { mainContent, thinkingContent } = extractThinkingContent(msg.content)
              return {
                id: msg.id,
                role: msg.role as 'user' | 'assistant',
                content: mainContent,
                thinkingContent: thinkingContent
              }
            }
            return {
              id: msg.id,
              role: msg.role as 'user' | 'assistant',
              content: msg.content,
            }
          })
          setMessages(convertedMessages)
          console.log(`Loaded ${convertedMessages.length} messages from session ${currentSession.id}`)
        } catch (error) {
          console.error('Error loading session messages:', error)
          setMessages([])
        }
      } else if (!currentSession || currentSession.isTemporary) {
        setMessages([])
        console.log('Cleared messages for new conversation')
      }
    }
    loadMessages()
  }, [currentSession?.id, currentSession?.isTemporary, getMessages])


  // Auto-resize textarea based on content
  const autoResizeTextarea = (textarea: HTMLTextAreaElement) => {
    textarea.style.height = 'auto'
    const lineHeight = 24
    const maxLines = 7
    const maxHeight = lineHeight * maxLines
    if (textarea.scrollHeight <= maxHeight) {
      textarea.style.height = `${textarea.scrollHeight}px`
      textarea.style.overflowY = 'hidden'
    } else {
      textarea.style.height = `${maxHeight}px`
      textarea.style.overflowY = 'auto'
    }
  }

  const copyToClipboard = async (content: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(content)
      setCopiedMessageId(messageId)
      setTimeout(() => setCopiedMessageId(''), 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  const handleFeedback = async (messageId: string, feedback: 'up' | 'down') => {
    if (submittingFeedback === messageId) return
    setSubmittingFeedback(messageId)
    try {
      await submitFeedback(messageId, feedback, user.userId)
      console.log(`✅ Feedback submitted: ${feedback} for message ${messageId}`)
      setMessageFeedback(prev => ({ ...prev, [messageId]: { feedback } }))
    } catch (error) {
      console.error('❌ Error submitting feedback:', error)
    } finally {
      setSubmittingFeedback('')
    }
  }

  const cancelFeedback = () => {
    setShowCommentBox('')
    setFeedbackComment('')
    setFeedbackType(null)
  }

  const submitFeedbackWithComment = async () => {
    const messageId = showCommentBox
    if (!messageId || !feedbackType) return
    if (submittingFeedback === messageId) return
    setSubmittingFeedback(messageId)
    try {
      await submitFeedback(messageId, feedbackType, user.userId, feedbackComment)
      console.log('✅ Feedback with comment submitted successfully')
      setMessageFeedback(prev => ({ ...prev, [messageId]: { feedback: feedbackType, comment: feedbackComment } }))
      setShowCommentBox('')
      setFeedbackComment('')
      setFeedbackType(null)
    } catch (error) {
      console.error('❌ Error submitting feedback with comment:', error)
    } finally {
      setSubmittingFeedback('')
    }
  }


  const getStatusDisplay = (status?: string) => {
    if (!status) return null
    if (status.toLowerCase().includes('preparing')) {
      return { text: status, icon: '🔄', className: 'status-preparing' }
    } else if (status.toLowerCase().includes('using tool') || status.toLowerCase().includes('using ')) {
      return { text: status, icon: '🔧', className: 'status-using-tool' }
    } else if (status.toLowerCase().includes('calling ')) {
      return { text: status, icon: '🤖', className: 'status-calling-subagent' }
    } else if (status.toLowerCase().includes('thinking')) {
      return { text: status, icon: '🧠', className: 'status-thinking' }
    } else if (status.toLowerCase() === 'complete') {
      return { text: status, icon: '✅', className: 'status-complete' }
    } else if (status.toLowerCase().includes('processing')) {
      return { text: status, icon: '⚙️', className: 'status-processing' }
    } else {
      return { text: status, icon: '⚙️', className: 'status-default' }
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(e)
    }
  }

  const handleSendMessage = (message: string) => {
    setInputMessage(message)
    setTimeout(() => {
      const form = document.querySelector('.chat-input-form') as HTMLFormElement
      if (form) form.requestSubmit()
    }, 0)
  }


  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputMessage.trim() || loading) return

    const messageText = inputMessage.trim()
    setInputMessage('')
    
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.overflowY = 'hidden'
    }

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
    }

    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    let actualSessionId = currentSession?.id
    let isNewSession = false
    let assistantMessageSaved = false

    try {
      if (!currentSession) {
        console.log('No current session found, creating new session...')
        const sessionTitle = messageText.length > 100 
          ? messageText.substring(0, 100).trim() + '...'
          : messageText.trim()
        const newSession = await createSession(user.userId, sessionTitle)
        actualSessionId = newSession.id
        isNewSession = true
        console.log('Created new session:', actualSessionId)
        if (updateCurrentSession) updateCurrentSession(newSession)
      } else if (currentSession.isTemporary) {
        console.log('Converting temporary session to permanent...')
        const sessionTitle = messageText.length > 100 
          ? messageText.substring(0, 100).trim() + '...'
          : messageText.trim()
        const newSession = await createSession(user.userId, sessionTitle)
        actualSessionId = newSession.id
        isNewSession = true
        console.log('Created permanent session:', actualSessionId)
        if (updateCurrentSession) updateCurrentSession(newSession)
      } else {
        actualSessionId = currentSession.id
        console.log('Using existing session:', actualSessionId)
      }

      if (actualSessionId) {
        try {
          await saveMessage(actualSessionId, 'user', messageText)
          console.log('Saved user message to AppSync')
        } catch (error) {
          console.error('Error saving user message:', error)
        }
      }


      const setAnswers = (updater: (prev: ChatMessage[]) => ChatMessage[]) => {
        setMessages(currentMessages => {
          const newMessages = updater(currentMessages)
          const lastMessage = newMessages[newMessages.length - 1]
          if (lastMessage && 
              lastMessage.role === 'assistant' && 
              !lastMessage.isStreaming && 
              lastMessage.status === 'complete' &&
              actualSessionId &&
              !assistantMessageSaved) {
            assistantMessageSaved = true
            saveMessage(actualSessionId, 'assistant', lastMessage.content)
              .then(() => console.log('Saved completed assistant message to AppSync'))
              .catch(error => console.error('Error saving completed assistant message:', error))
          }
          return newMessages
        })
      }

      console.log('Sending message with session ID:', actualSessionId)
      await invokeAgentCore(
        messageText,
        user.userId,
        actualSessionId || `session-${user.userId}-${Date.now()}`,
        setAnswers,
      )

      console.log('Assistant message will be saved when AgentCore signals completion')

      if (isNewSession && refreshSessions) {
        console.log('Refreshing sessions after creating new session...')
        const refreshWithRetry = async (retries = 3, delay = 1000) => {
          for (let i = 0; i < retries; i++) {
            await new Promise(resolve => setTimeout(resolve, delay))
            try {
              await refreshSessions()
              console.log(`Session refresh attempt ${i + 1} completed`)
              break
            } catch (error) {
              console.error(`Session refresh attempt ${i + 1} failed:`, error)
              if (i === retries - 1) console.error('All session refresh attempts failed')
            }
          }
        }
        refreshWithRetry()
      }

    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your message. Please try again.',
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const hasAssistantMessages = messages.some(m => m.role === 'assistant' && !m.isStreaming)

  const lastAssistantMessageId = useMemo(() => {
    const assistantMessages = messages.filter(m => m.role === 'assistant' && !m.isStreaming)
    return assistantMessages.length > 0 ? assistantMessages[assistantMessages.length - 1].id : null
  }, [messages])


  return (
    <div className="w-1/2 flex flex-col bg-white m-3 rounded-xl border border-gray-200 overflow-hidden shadow-sm">
      {/* Chat Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-gray-200 bg-[#f0f4ff]">
        <div className="relative" ref={sessionDropdownRef}>
          <button
            onClick={() => sessions.length > 0 && setShowSessionDropdown(!showSessionDropdown)}
            className={`flex items-center gap-1.5 font-medium text-gray-700 ${sessions.length > 0 ? 'hover:text-[#1668e3] cursor-pointer' : ''}`}
          >
            <span>Recent Sessions ({sessions.length})</span>
            {sessions.length > 0 && (
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ transform: showSessionDropdown ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>
                <path d="M6 9l6 6 6-6"/>
              </svg>
            )}
          </button>
          {showSessionDropdown && sessions.length > 0 && (
            <div className="absolute top-full left-0 mt-1 w-72 max-h-80 overflow-y-auto bg-white border border-gray-200 rounded-lg shadow-lg z-50">
              {sessions.map((session) => (
                <button
                  key={session.id}
                  onClick={() => {
                    onSwitchSession?.(session.id)
                    setShowSessionDropdown(false)
                  }}
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-b-0 ${
                    currentSession?.id === session.id ? 'bg-[#f0f4ff] text-[#1668e3]' : 'text-gray-700'
                  }`}
                >
                  <div className="truncate font-medium">{session.title || 'Untitled'}</div>
                  <div className="text-xs text-gray-400 mt-0.5">
                    {new Date(session.createdAt).toLocaleDateString()}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
        {onNewChat && (
          <button 
            onClick={onNewChat}
            disabled={!canStartNewChat || !hasAssistantMessages}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 hover:text-[#1668e3] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 5v14M5 12h14"/>
            </svg>
            New Session
          </button>
        )}
      </div>
      <div className="flex-1 flex flex-col overflow-hidden">
        <div 
          className="flex-1 overflow-y-auto p-4 flex flex-col gap-4" 
          ref={messagesContainerRef}
        >
          {messages.length === 0 && (
            <div className="text-center text-gray-500 italic py-8 px-4 bg-gray-50 rounded-lg mx-auto max-w-md">
              Hi {user.name || user.username}! I'm your AI assistant. Ask me anything!
            </div>
          )}
          
          {messages.map((message) => {
            const statusDisplay = message.role === 'assistant' ? getStatusDisplay(message.status) : null
            const currentFeedback = messageFeedback[message.id]
            
            return (
              <div key={message.id} className={`message-wrapper ${message.role}`}>
                {statusDisplay && statusDisplay.className !== 'status-complete' && (
                  <div className={`message-status-row ${statusDisplay.className}`}>
                    <span className="status-icon">{statusDisplay.icon}</span>
                    <span className="status-text">{statusDisplay.text}</span>
                  </div>
                )}
                
                <div className={`message ${message.role}`}>
                  <div className="message-content">
                    {message.role === 'assistant' && message.thinkingContent && (
                      <ThinkingSection thinkingContent={message.thinkingContent} />
                    )}
                    
                    {message.role === 'assistant' && ((message.previousLoops && message.previousLoops.length > 0) || (message.subagentSteps && message.subagentSteps.length > 0) || (message.currentSubagent && message.currentSubagent.content)) && (
                      <PreviousLoopsSection 
                        previousLoops={message.previousLoops} 
                        subagentSteps={message.subagentSteps}
                        currentSubagent={message.currentSubagent}
                      />
                    )}
                    
                    <div className="formatted-message">
                      <MarkdownRenderer 
                        content={message.currentLoop || message.content} 
                        isAssistant={message.role === 'assistant'} 
                      />
                      {message.isStreaming && (
                        <span className="streaming-cursor">|</span>
                      )}
                    </div>
                  </div>
                </div>

                {message.role === 'assistant' && (
                  <div className="message-actions-below">
                    <button
                      className="action-btn copy-btn"
                      onClick={() => copyToClipboard(message.content, message.id)}
                      title="Copy message"
                    >
                      {copiedMessageId === message.id ? (
                        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                          <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                        </svg>
                      ) : (
                        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12.668 10.667C12.668 9.95614 12.668 9.46258 12.6367 9.0791C12.6137 8.79732 12.5758 8.60761 12.5244 8.46387L12.4688 8.33399C12.3148 8.03193 12.0803 7.77885 11.793 7.60254L11.666 7.53125C11.508 7.45087 11.2963 7.39395 10.9209 7.36328C10.5374 7.33197 10.0439 7.33203 9.33301 7.33203H6.5C5.78896 7.33203 5.29563 7.33195 4.91211 7.36328C4.63016 7.38632 4.44065 7.42413 4.29688 7.47559L4.16699 7.53125C3.86488 7.68518 3.61186 7.9196 3.43555 8.20703L3.36524 8.33399C3.28478 8.49198 3.22795 8.70352 3.19727 9.0791C3.16595 9.46259 3.16504 9.95611 3.16504 10.667V13.5C3.16504 14.211 3.16593 14.7044 3.19727 15.0879C3.22797 15.4636 3.28473 15.675 3.36524 15.833L3.43555 15.959C3.61186 16.2466 3.86474 16.4807 4.16699 16.6348L4.29688 16.6914C4.44063 16.7428 4.63025 16.7797 4.91211 16.8027C5.29563 16.8341 5.78896 16.835 6.5 16.835H9.33301C10.0439 16.835 10.5374 16.8341 10.9209 16.8027C11.2965 16.772 11.508 16.7152 11.666 16.6348L11.793 16.5645C12.0804 16.3881 12.3148 16.1351 12.4688 15.833L12.5244 15.7031C12.5759 15.5594 12.6137 15.3698 12.6367 15.0879C12.6681 14.7044 12.668 14.211 12.668 13.5V10.667Z"></path>
                        </svg>
                      )}
                    </button>
                    
                    <button
                      className={`action-btn thumbs-up-btn ${currentFeedback?.feedback === 'up' ? 'feedback-active' : ''} ${submittingFeedback === message.id ? 'feedback-loading' : ''}`}
                      onClick={() => handleFeedback(message.id, 'up')}
                      disabled={submittingFeedback === message.id}
                      title={currentFeedback?.feedback === 'up' ? 'You liked this response' : 'Good response'}
                    >
                      {submittingFeedback === message.id ? (
                        <div className="loading-spinner-small"></div>
                      ) : (
                        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                          <path d="M10.9153 1.83987L11.2942 1.88772L11.4749 1.91507C13.2633 2.24201 14.4107 4.01717 13.9749 5.78225L13.9261 5.95901L13.3987 7.6719C13.7708 7.67575 14.0961 7.68389 14.3792 7.70608C14.8737 7.74486 15.3109 7.82759 15.7015 8.03323L15.8528 8.11819C16.5966 8.56353 17.1278 9.29625 17.3167 10.1475L17.347 10.3096C17.403 10.69 17.3647 11.0832 17.2835 11.5098C17.2375 11.7517 17.1735 12.0212 17.096 12.3233L16.8255 13.3321L16.4456 14.7276C16.2076 15.6001 16.0438 16.2356 15.7366 16.7305L15.595 16.9346C15.2989 17.318 14.9197 17.628 14.4866 17.8408L14.2982 17.9258C13.6885 18.1774 12.9785 18.1651 11.9446 18.1651H7.33331C6.64422 18.1651 6.08726 18.1657 5.63702 18.1289C5.23638 18.0962 4.87565 18.031 4.53936 17.8867L4.39679 17.8203C3.87576 17.5549 3.43916 17.151 3.13507 16.6553L3.013 16.4366C2.82119 16.0599 2.74182 15.6541 2.7044 15.1963C2.66762 14.7461 2.66827 14.1891 2.66827 13.5V11.667C2.66827 10.9349 2.66214 10.4375 2.77569 10.0137L2.83722 9.81253C3.17599 8.81768 3.99001 8.05084 5.01397 7.77639L5.17706 7.73928C5.56592 7.66435 6.02595 7.66799 6.66632 7.66799C6.9429 7.66799 7.19894 7.52038 7.33624 7.2803L10.2562 2.16995L10.3118 2.08792C10.4544 1.90739 10.6824 1.81092 10.9153 1.83987Z"></path>
                        </svg>
                      )}
                    </button>

                    <button
                      className={`action-btn thumbs-down-btn ${currentFeedback?.feedback === 'down' ? 'feedback-active' : ''} ${submittingFeedback === message.id ? 'feedback-loading' : ''}`}
                      onClick={() => handleFeedback(message.id, 'down')}
                      disabled={submittingFeedback === message.id}
                      title={currentFeedback?.feedback === 'down' ? 'You disliked this response' : 'Poor response'}
                    >
                      {submittingFeedback === message.id ? (
                        <div className="loading-spinner-small"></div>
                      ) : (
                        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" style={{transform: 'rotate(180deg)'}}>
                          <path d="M10.9153 1.83987L11.2942 1.88772L11.4749 1.91507C13.2633 2.24201 14.4107 4.01717 13.9749 5.78225L13.9261 5.95901L13.3987 7.6719C13.7708 7.67575 14.0961 7.68389 14.3792 7.70608C14.8737 7.74486 15.3109 7.82759 15.7015 8.03323L15.8528 8.11819C16.5966 8.56353 17.1278 9.29625 17.3167 10.1475L17.347 10.3096C17.403 10.69 17.3647 11.0832 17.2835 11.5098C17.2375 11.7517 17.1735 12.0212 17.096 12.3233L16.8255 13.3321L16.4456 14.7276C16.2076 15.6001 16.0438 16.2356 15.7366 16.7305L15.595 16.9346C15.2989 17.318 14.9197 17.628 14.4866 17.8408L14.2982 17.9258C13.6885 18.1774 12.9785 18.1651 11.9446 18.1651H7.33331C6.64422 18.1651 6.08726 18.1657 5.63702 18.1289C5.23638 18.0962 4.87565 18.031 4.53936 17.8867L4.39679 17.8203C3.87576 17.5549 3.43916 17.151 3.13507 16.6553L3.013 16.4366C2.82119 16.0599 2.74182 15.6541 2.7044 15.1963C2.66762 14.7461 2.66827 14.1891 2.66827 13.5V11.667C2.66827 10.9349 2.66214 10.4375 2.77569 10.0137L2.83722 9.81253C3.17599 8.81768 3.99001 8.05084 5.01397 7.77639L5.17706 7.73928C5.56592 7.66435 6.02595 7.66799 6.66632 7.66799C6.9429 7.66799 7.19894 7.52038 7.33624 7.2803L10.2562 2.16995L10.3118 2.08792C10.4544 1.90739 10.6824 1.81092 10.9153 1.83987Z"></path>
                        </svg>
                      )}
                    </button>
                    
                    {!currentFeedback && (
                      <button
                        className="action-btn comment-btn"
                        onClick={() => {
                          setShowCommentBox(message.id)
                          setFeedbackType(null)
                          setFeedbackComment('')
                        }}
                        title="Add comment with feedback"
                      >
                        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                          <path d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z"/>
                        </svg>
                      </button>
                    )}
                  </div>
                )}

                {/* Minimal comment input for feedback */}
                {showCommentBox === message.id && (
                  <div className="minimal-comment-box">
                    <div className="minimal-feedback-selector">
                      <button
                        className={`minimal-feedback-btn ${feedbackType === 'up' ? 'active' : ''}`}
                        onClick={() => setFeedbackType('up')}
                        title="Helpful"
                      >
                        <svg width="12" height="12" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                          <path d="M10.9153 1.83987L11.2942 1.88772L11.4749 1.91507C13.2633 2.24201 14.4107 4.01717 13.9749 5.78225L13.9261 5.95901L13.3987 7.6719C13.7708 7.67575 14.0961 7.68389 14.3792 7.70608C14.8737 7.74486 15.3109 7.82759 15.7015 8.03323L15.8528 8.11819C16.5966 8.56353 17.1278 9.29625 17.3167 10.1475L17.347 10.3096C17.403 10.69 17.3647 11.0832 17.2835 11.5098C17.2375 11.7517 17.1735 12.0212 17.096 12.3233L16.8255 13.3321L16.4456 14.7276C16.2076 15.6001 16.0438 16.2356 15.7366 16.7305L15.595 16.9346C15.2989 17.318 14.9197 17.628 14.4866 17.8408L14.2982 17.9258C13.6885 18.1774 12.9785 18.1651 11.9446 18.1651H7.33331C6.64422 18.1651 6.08726 18.1657 5.63702 18.1289C5.23638 18.0962 4.87565 18.031 4.53936 17.8867L4.39679 17.8203C3.87576 17.5549 3.43916 17.151 3.13507 16.6553L3.013 16.4366C2.82119 16.0599 2.74182 15.6541 2.7044 15.1963C2.66762 14.7461 2.66827 14.1891 2.66827 13.5V11.667C2.66827 10.9349 2.66214 10.4375 2.77569 10.0137L2.83722 9.81253C3.17599 8.81768 3.99001 8.05084 5.01397 7.77639L5.17706 7.73928C5.56592 7.66435 6.02595 7.66799 6.66632 7.66799C6.9429 7.66799 7.19894 7.52038 7.33624 7.2803L10.2562 2.16995L10.3118 2.08792C10.4544 1.90739 10.6824 1.81092 10.9153 1.83987Z"></path>
                        </svg>
                      </button>
                      <button
                        className={`minimal-feedback-btn ${feedbackType === 'down' ? 'active' : ''}`}
                        onClick={() => setFeedbackType('down')}
                        title="Not helpful"
                      >
                        <svg width="12" height="12" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" style={{transform: 'rotate(180deg)'}}>
                          <path d="M10.9153 1.83987L11.2942 1.88772L11.4749 1.91507C13.2633 2.24201 14.4107 4.01717 13.9749 5.78225L13.9261 5.95901L13.3987 7.6719C13.7708 7.67575 14.0961 7.68389 14.3792 7.70608C14.8737 7.74486 15.3109 7.82759 15.7015 8.03323L15.8528 8.11819C16.5966 8.56353 17.1278 9.29625 17.3167 10.1475L17.347 10.3096C17.403 10.69 17.3647 11.0832 17.2835 11.5098C17.2375 11.7517 17.1735 12.0212 17.096 12.3233L16.8255 13.3321L16.4456 14.7276C16.2076 15.6001 16.0438 16.2356 15.7366 16.7305L15.595 16.9346C15.2989 17.318 14.9197 17.628 14.4866 17.8408L14.2982 17.9258C13.6885 18.1774 12.9785 18.1651 11.9446 18.1651H7.33331C6.64422 18.1651 6.08726 18.1657 5.63702 18.1289C5.23638 18.0962 4.87565 18.031 4.53936 17.8867L4.39679 17.8203C3.87576 17.5549 3.43916 17.151 3.13507 16.6553L3.013 16.4366C2.82119 16.0599 2.74182 15.6541 2.7044 15.1963C2.66762 14.7461 2.66827 14.1891 2.66827 13.5V11.667C2.66827 10.9349 2.66214 10.4375 2.77569 10.0137L2.83722 9.81253C3.17599 8.81768 3.99001 8.05084 5.01397 7.77639L5.17706 7.73928C5.56592 7.66435 6.02595 7.66799 6.66632 7.66799C6.9429 7.66799 7.19894 7.52038 7.33624 7.2803L10.2562 2.16995L10.3118 2.08792C10.4544 1.90739 10.6824 1.81092 10.9153 1.83987Z"></path>
                        </svg>
                      </button>
                    </div>
                    <input
                      type="text"
                      value={feedbackComment}
                      onChange={(e) => setFeedbackComment(e.target.value)}
                      placeholder="Add a comment (optional)..."
                      className="minimal-comment-input"
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') submitFeedbackWithComment()
                        else if (e.key === 'Escape') cancelFeedback()
                      }}
                      autoFocus
                    />
                    <div className="minimal-comment-actions">
                      <button onClick={cancelFeedback} className="minimal-cancel-btn">✕</button>
                      <button 
                        onClick={submitFeedbackWithComment}
                        disabled={!feedbackType || submittingFeedback === message.id}
                        className="minimal-submit-btn"
                      >
                        ✓
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )
          })}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-100 bg-white">
          <form className="flex gap-3" onSubmit={sendMessage}>
            <textarea
              ref={textareaRef}
              className="flex-1 px-4 py-3 border border-gray-200 rounded-xl text-base outline-none resize-none focus:border-[#1668e3] focus:ring-2 focus:ring-[#1668e3]/10 transition-all"
              value={inputMessage}
              onChange={(e) => {
                setInputMessage(e.target.value)
                autoResizeTextarea(e.target)
              }}
              onKeyDown={handleKeyDown}
              placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
              disabled={loading}
              rows={1}
            />
            <button 
              type="submit" 
              className="p-3 bg-[#1a1f71] text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all self-end"
              disabled={!inputMessage.trim() || loading}
              title={loading ? 'Processing...' : 'Send message'}
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13"/>
                </svg>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Chat
