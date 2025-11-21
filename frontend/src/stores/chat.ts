import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Message } from './session'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Record<string, Message[]>>({})
  const streamingMessages = ref<Record<string, boolean>>({})

  const getCurrentMessages = computed(() => {
    const sessionId = useSessionStore().currentSessionId
    return sessionId ? messages.value[sessionId] || [] : []
  })

  function getMessages(sessionId: string): Message[] {
    return messages.value[sessionId] || []
  }

  function addMessage(sessionId: string, role: 'user' | 'assistant', content: string, metadata?: Record<string, any>) {
    const message: Message = {
      id: generateMessageId(),
      role,
      content,
      timestamp: Date.now() / 1000,
      metadata
    }

    if (!messages.value[sessionId]) {
      messages.value[sessionId] = []
    }

    messages.value[sessionId].push(message)
    return message
  }

  async function sendMessage(sessionId: string, content: string) {
    try {
      // Add user message
      addMessage(sessionId, 'user', content)
      
      // Get AI response
      const response = await fetch(`/api/v1/sessions/${sessionId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: content,
          timestamp: Date.now() / 1000,
          event_id: generateMessageId()
        })
      })

      const result = await response.json()
      
      if (result.code === 0) {
        addMessage(sessionId, 'assistant', result.data.response)
      } else {
        addMessage(sessionId, 'assistant', `Error: ${result.msg}`)
      }
      
      return result
    } catch (error) {
      console.error('Error sending message:', error)
      addMessage(sessionId, 'assistant', 'Sorry, there was an error processing your message.')
      throw error
    }
  }

  async function sendStreamingMessage(sessionId: string, content: string) {
    try {
      streamingMessages.value[sessionId] = true
      
      // Add user message
      const userMessage = addMessage(sessionId, 'user', content)
      
      // Create assistant message placeholder for streaming
      const assistantMessage = addMessage(sessionId, 'assistant', '', { streaming: true })
      
      // Set up SSE connection
      const eventSource = new EventSource(`/api/v1/sessions/${sessionId}/chat`, {
        method: 'POST',
        body: JSON.stringify({
          message: content,
          timestamp: Date.now() / 1000,
          event_id: userMessage.id
        })
      })

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          
          if (data.content) {
            // Update assistant message content
            assistantMessage.content += data.content
          }
        } catch (error) {
          console.error('Error parsing SSE data:', error)
        }
      }

      eventSource.addEventListener('done', (event) => {
        // Stream completed
        streamingMessages.value[sessionId] = false
        eventSource.close()
        delete assistantMessage.metadata?.streaming
      })

      eventSource.addEventListener('error', (event) => {
        console.error('SSE error:', event)
        streamingMessages.value[sessionId] = false
        eventSource.close()
        assistantMessage.content = 'Sorry, there was an error streaming the response.'
        delete assistantMessage.metadata?.streaming
      })

    } catch (error) {
      streamingMessages.value[sessionId] = false
      console.error('Error sending streaming message:', error)
      addMessage(sessionId, 'assistant', 'Sorry, there was an error processing your message.')
      throw error
    }
  }

  async function loadSessionMessages(sessionId: string) {
    try {
      const response = await fetch(`/api/v1/sessions/${sessionId}`)
      const result = await response.json()

      if (result.code === 0) {
        const session = result.data
        messages.value[sessionId] = []
        
        // Extract messages from events
        session.events?.forEach((event: any) => {
          if (event.event_type === 'message_received' || event.event_type === 'message_sent') {
            const role = event.event_type === 'message_received' ? 'user' : 'assistant'
            const content = event.data.content || ''
            const timestamp = new Date(event.timestamp).getTime() / 1000
            
            addMessage(sessionId, role, content, { event_id: event.event_id })
          }
        })
        
        return messages.value[sessionId]
      } else {
        throw new Error(result.msg || 'Failed to load messages')
      }
    } catch (error) {
      console.error('Error loading session messages:', error)
      throw error
    }
  }

  function clearMessages(sessionId: string) {
    delete messages.value[sessionId]
  }

  function updateMessage(sessionId: string, messageId: string, updates: Partial<Message>) {
    const sessionMessages = messages.value[sessionId]
    if (sessionMessages) {
      const message = sessionMessages.find(m => m.id === messageId)
      if (message) {
        Object.assign(message, updates)
      }
    }
  }

  function deleteMessage(sessionId: string, messageId: string) {
    const sessionMessages = messages.value[sessionId]
    if (sessionMessages) {
      const index = sessionMessages.findIndex(m => m.id === messageId)
      if (index > -1) {
        sessionMessages.splice(index, 1)
      }
    }
  }

  function isStreaming(sessionId: string): boolean {
    return streamingMessages.value[sessionId] || false
  }

  function generateMessageId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  return {
    // State
    messages,
    streamingMessages,
    
    // Getters
    getCurrentMessages,
    
    // Actions
    getMessages,
    addMessage,
    sendMessage,
    sendStreamingMessage,
    loadSessionMessages,
    clearMessages,
    updateMessage,
    deleteMessage,
    isStreaming,
    generateMessageId
  }
})