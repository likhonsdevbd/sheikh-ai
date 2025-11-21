import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Session {
  session_id: string
  title: string
  latest_message: string
  latest_message_at: number
  status: string
  unread_message_count: number
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  metadata?: Record<string, any>
}

export const useSessionStore = defineStore('session', () => {
  const sessions = ref<Session[]>([])
  const currentSessionId = ref<string | null>(null)
  const isLoading = ref(false)

  const currentSession = computed(() => {
    return sessions.value.find(session => session.session_id === currentSessionId.value)
  })

  const unreadCount = computed(() => {
    return sessions.value.reduce((total, session) => total + session.unread_message_count, 0)
  })

  async function createSession(title = 'New Conversation') {
    try {
      isLoading.value = true
      const response = await fetch('/api/v1/sessions', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const result = await response.json()
      
      if (result.code === 0) {
        // Add new session to list
        const newSession: Session = {
          session_id: result.data.session_id,
          title,
          latest_message: '',
          latest_message_at: Date.now() / 1000,
          status: 'active',
          unread_message_count: 0
        }
        sessions.value.unshift(newSession)
        
        // Set as current session
        currentSessionId.value = newSession.session_id
        
        return result
      } else {
        throw new Error(result.msg || 'Failed to create session')
      }
    } catch (error) {
      console.error('Error creating session:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function loadSessions() {
    try {
      isLoading.value = true
      const response = await fetch('/api/v1/sessions')
      const result = await response.json()

      if (result.code === 0) {
        sessions.value = result.data.sessions || []
        
        // If no current session, set the first one
        if (!currentSessionId.value && sessions.value.length > 0) {
          currentSessionId.value = sessions.value[0].session_id
        }
        
        return result
      } else {
        throw new Error(result.msg || 'Failed to load sessions')
      }
    } catch (error) {
      console.error('Error loading sessions:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function getSession(sessionId: string) {
    try {
      const response = await fetch(`/api/v1/sessions/${sessionId}`)
      const result = await response.json()

      if (result.code === 0) {
        return result.data
      } else {
        throw new Error(result.msg || 'Failed to get session')
      }
    } catch (error) {
      console.error('Error getting session:', error)
      throw error
    }
  }

  async function selectSession(sessionId: string) {
    currentSessionId.value = sessionId
    
    // Clear unread count for this session
    const session = sessions.value.find(s => s.session_id === sessionId)
    if (session) {
      session.unread_message_count = 0
    }
  }

  async function deleteSession(sessionId: string) {
    try {
      const response = await fetch(`/api/v1/sessions/${sessionId}`, {
        method: 'DELETE'
      })
      
      const result = await response.json()
      
      if (result.code === 0) {
        // Remove from sessions list
        const index = sessions.value.findIndex(s => s.session_id === sessionId)
        if (index > -1) {
          sessions.value.splice(index, 1)
        }
        
        // If this was the current session, switch to another one
        if (currentSessionId.value === sessionId) {
          if (sessions.value.length > 0) {
            currentSessionId.value = sessions.value[0].session_id
          } else {
            currentSessionId.value = null
          }
        }
        
        return result
      } else {
        throw new Error(result.msg || 'Failed to delete session')
      }
    } catch (error) {
      console.error('Error deleting session:', error)
      throw error
    }
  }

  async function stopSession(sessionId: string) {
    try {
      const response = await fetch(`/api/v1/sessions/${sessionId}/stop`, {
        method: 'POST'
      })
      
      const result = await response.json()
      
      if (result.code === 0) {
        // Update session status
        const session = sessions.value.find(s => s.session_id === sessionId)
        if (session) {
          session.status = 'stopped'
        }
        
        return result
      } else {
        throw new Error(result.msg || 'Failed to stop session')
      }
    } catch (error) {
      console.error('Error stopping session:', error)
      throw error
    }
  }

  async function renameSession(sessionId: string, newTitle: string) {
    // This would be implemented with a rename API endpoint
    const session = sessions.value.find(s => s.session_id === sessionId)
    if (session) {
      session.title = newTitle
    }
  }

  function updateSession(sessionId: string, updates: Partial<Session>) {
    const session = sessions.value.find(s => s.session_id === sessionId)
    if (session) {
      Object.assign(session, updates)
    }
  }

  function incrementUnreadCount(sessionId: string) {
    const session = sessions.value.find(s => s.session_id === sessionId)
    if (session) {
      session.unread_message_count++
    }
  }

  function updateLatestMessage(sessionId: string, message: string, timestamp: number) {
    const session = sessions.value.find(s => s.session_id === sessionId)
    if (session) {
      session.latest_message = message
      session.latest_message_at = timestamp
    }
  }

  return {
    // State
    sessions,
    currentSessionId,
    isLoading,
    
    // Getters
    currentSession,
    unreadCount,
    
    // Actions
    createSession,
    loadSessions,
    getSession,
    selectSession,
    deleteSession,
    stopSession,
    renameSession,
    updateSession,
    incrementUnreadCount,
    updateLatestMessage
  }
})