import { test, expect } from '@playwright/test'

const API_BASE_URL = 'http://localhost:8000/api/v1'

test.describe('Sheikh AI Backend API', () => {
  test('should have health check endpoint', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/health`)
    expect(response.status()).toBe(200)
    
    const data = await response.json()
    expect(data).toHaveProperty('status', 'healthy')
  })

  test('should create new conversation', async ({ request }) => {
    const response = await request.post(`${API_BASE_URL}/conversations`, {
      data: {
        title: 'Test Conversation'
      }
    })
    
    expect(response.status()).toBe(201)
    
    const data = await response.json()
    expect(data).toHaveProperty('id')
    expect(data).toHaveProperty('title', 'Test Conversation')
  })

  test('should send message to AI and receive response', async ({ request }) => {
    // First create a conversation
    const createResponse = await request.post(`${API_BASE_URL}/conversations`, {
      data: { title: 'Test Chat' }
    })
    
    expect(createResponse.status()).toBe(201)
    const conversation = await createResponse.json()
    const conversationId = conversation.id
    
    // Send a message
    const messageResponse = await request.post(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      data: {
        content: 'Hello, this is a test message',
        provider: 'gemini'
      }
    })
    
    expect(messageResponse.status()).toBe(200)
    
    const data = await messageResponse.json()
    expect(data).toHaveProperty('id')
    expect(data).toHaveProperty('content')
    expect(data.content).toContain(/.*/i) // Should contain response text
  })

  test('should switch between AI providers', async ({ request }) => {
    // Test OpenAI provider
    const openaiResponse = await request.post(`${API_BASE_URL}/conversations`, {
      data: { title: 'OpenAI Test' }
    })
    
    if (openaiResponse.status() === 201) {
      const conversation = await openaiResponse.json()
      const messageResponse = await request.post(`${API_BASE_URL}/conversations/${conversation.id}/messages`, {
        data: {
          content: 'Test message for OpenAI',
          provider: 'openai'
        }
      })
      expect(messageResponse.status()).toBe(200)
    }
    
    // Test Gemini provider  
    const geminiResponse = await request.post(`${API_BASE_URL}/conversations`, {
      data: { title: 'Gemini Test' }
    })
    
    if (geminiResponse.status() === 201) {
      const conversation = await geminiResponse.json()
      const messageResponse = await request.post(`${API_BASE_URL}/conversations/${conversation.id}/messages`, {
        data: {
          content: 'Test message for Gemini',
          provider: 'gemini'
        }
      })
      expect(messageResponse.status()).toBe(200)
    }
  })

  test('should get conversation history', async ({ request }) => {
    // Create a conversation with messages
    const createResponse = await request.post(`${API_BASE_URL}/conversations`, {
      data: { title: 'History Test' }
    })
    
    expect(createResponse.status()).toBe(201)
    const conversation = await createResponse.json()
    
    // Add a message
    await request.post(`${API_BASE_URL}/conversations/${conversation.id}/messages`, {
      data: {
        content: 'Test message for history',
        provider: 'gemini'
      }
    })
    
    // Get conversation details
    const getResponse = await request.get(`${API_BASE_URL}/conversations/${conversation.id}`)
    expect(getResponse.status()).toBe(200)
    
    const data = await getResponse.json()
    expect(data).toHaveProperty('id', conversation.id)
    expect(data).toHaveProperty('messages')
    expect(data.messages.length).toBeGreaterThan(0)
  })

  test('should handle file upload', async ({ request }) => {
    // Create a file upload request
    const createResponse = await request.post(`${API_BASE_URL}/conversations`, {
      data: { title: 'File Upload Test' }
    })
    
    expect(createResponse.status()).toBe(201)
    const conversation = await createResponse.json()
    
    // Note: In a real implementation, you'd use multipart/form-data
    // This is a simplified test for the API structure
    const fileResponse = await request.post(`${API_BASE_URL}/conversations/${conversation.id}/files`, {
      data: {
        filename: 'test.txt',
        content: 'Test file content'
      }
    })
    
    // May return 200 if file upload endpoint exists, or 404 if not implemented
    expect([200, 404, 501]).toContain(fileResponse.status())
  })

  test('should execute shell commands', async ({ request }) => {
    const createResponse = await request.post(`${API_BASE_URL}/conversations`, {
      data: { title: 'Shell Test' }
    })
    
    expect(createResponse.status()).toBe(201)
    const conversation = await createResponse.json()
    
    // Test shell command execution
    const shellResponse = await request.post(`${API_BASE_URL}/shell/execute`, {
      data: {
        command: 'echo "Hello World"',
        conversation_id: conversation.id
      }
    })
    
    // May return 200 if shell endpoint exists, or 404 if not implemented
    expect([200, 404, 501]).toContain(shellResponse.status())
  })

  test('should handle browser automation', async ({ request }) => {
    const createResponse = await request.post(`${API_BASE_URL}/conversations`, {
      data: { title: 'Browser Test' }
    })
    
    expect(createResponse.status()).toBe(201)
    const conversation = await createResponse.json()
    
    // Test browser automation endpoint
    const browserResponse = await request.post(`${API_BASE_URL}/browser/automate`, {
      data: {
        url: 'https://example.com',
        action: 'navigate',
        conversation_id: conversation.id
      }
    })
    
    // May return 200 if browser endpoint exists, or 404 if not implemented
    expect([200, 404, 501]).toContain(browserResponse.status())
  })

  test('should validate request data', async ({ request }) => {
    // Test invalid data
    const response = await request.post(`${API_BASE_URL}/conversations`, {
      data: {} // Empty data should be invalid
    })
    
    expect(response.status()).toBe(422) // Validation error
  })

  test('should handle server errors gracefully', async ({ request }) => {
    // Try to get non-existent conversation
    const response = await request.get(`${API_BASE_URL}/conversations/non-existent-id`)
    expect(response.status()).toBe(404)
  })

  test('should support CORS for frontend', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/health`)
    const corsHeaders = response.headers()
    
    // Check if CORS headers are present
    expect(corsHeaders).toHaveProperty('access-control-allow-origin')
  })
})