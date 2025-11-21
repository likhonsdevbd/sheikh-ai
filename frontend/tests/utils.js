// Test utilities and helpers for Sheikh AI Playwright tests

const API_BASE_URL = 'http://localhost:8000/api/v1'
const FRONTEND_URL = 'http://localhost:3000'

export const testUtils = {
  /**
   * Wait for backend health check
   */
  async waitForBackend(page) {
    try {
      const response = await page.request.get(`${API_BASE_URL}/health`)
      return response.status() === 200
    } catch (error) {
      console.log('Backend not ready:', error.message)
      return false
    }
  },

  /**
   * Create a test conversation
   */
  async createTestConversation(page, title = 'Test Conversation') {
    const response = await page.request.post(`${API_BASE_URL}/conversations`, {
      data: { title }
    })
    
    if (response.status() === 201) {
      return await response.json()
    }
    throw new Error(`Failed to create conversation: ${response.status()}`)
  },

  /**
   * Send a message and wait for response
   */
  async sendMessageAndWait(page, message, provider = 'gemini') {
    const conversation = await this.createTestConversation(page)
    const conversationId = conversation.id
    
    // Send message via API for more reliable testing
    const response = await page.request.post(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      data: { content: message, provider }
    })
    
    if (response.status() === 200) {
      return await response.json()
    }
    throw new Error(`Failed to send message: ${response.status()}`)
  },

  /**
   * Get all messages from a conversation
   */
  async getConversationMessages(page, conversationId) {
    const response = await page.request.get(`${API_BASE_URL}/conversations/${conversationId}`)
    
    if (response.status() === 200) {
      const data = await response.json()
      return data.messages || []
    }
    return []
  },

  /**
   * Wait for an element to be visible
   */
  async waitForElement(page, selector, timeout = 10000) {
    try {
      await page.waitForSelector(selector, { timeout })
      return true
    } catch (error) {
      console.log(`Element ${selector} not found within ${timeout}ms`)
      return false
    }
  },

  /**
   * Fill input and verify it's not empty
   */
  async fillInput(page, selector, text) {
    const input = page.locator(selector)
    await input.fill(text)
    
    const actualValue = await input.inputValue()
    if (actualValue !== text) {
      throw new Error(`Expected "${text}", got "${actualValue}"`)
    }
    
    return true
  },

  /**
   * Click element and handle potential navigation
   */
  async clickAndWait(page, selector, waitTime = 1000) {
    const element = page.locator(selector)
    await element.click()
    
    // Wait for any potential state changes
    if (waitTime > 0) {
      await page.waitForTimeout(waitTime)
    }
  },

  /**
   * Verify that the page has no console errors (excluding expected ones)
   */
  async verifyNoConsoleErrors(page, allowedErrors = []) {
    const messages = []
    page.on('console', msg => {
      if (msg.type() === 'error') {
        const message = msg.text()
        // Check if this error is in our allowed list
        const isAllowed = allowedErrors.some(allowed => message.includes(allowed))
        if (!isAllowed) {
          messages.push(message)
        }
      }
    })
    
    // Execute some action and wait
    await page.waitForTimeout(2000)
    
    if (messages.length > 0) {
      throw new Error(`Console errors found: ${messages.join(', ')}`)
    }
    
    return true
  },

  /**
   * Check if element has expected text content
   */
  async verifyTextContent(page, selector, expectedText, timeout = 5000) {
    const element = page.locator(selector)
    await element.waitFor({ state: 'visible', timeout })
    
    const text = await element.textContent()
    return text?.includes(expectedText) || false
  },

  /**
   * Take a screenshot and save with descriptive name
   */
  async takeScreenshot(page, name, fullPage = true) {
    const screenshot = await page.screenshot({ 
      fullPage,
      path: `test-results/screenshots/${name}.png`
    })
    return screenshot
  },

  /**
   * Check for responsive design elements
   */
  async checkResponsiveDesign(page) {
    const breakpoints = [
      { name: 'mobile', width: 375, height: 667 },
      { name: 'tablet', width: 768, height: 1024 },
      { name: 'desktop', width: 1920, height: 1080 }
    ]
    
    const results = []
    
    for (const bp of breakpoints) {
      await page.setViewportSize({ width: bp.width, height: bp.height })
      await page.waitForTimeout(500)
      
      // Check for horizontal scrolling
      const hasHorizontalScroll = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth
      })
      
      // Check if main content is visible
      const mainContentVisible = await page.locator('main, [data-testid="main"], .main').first().isVisible()
      
      results.push({
        breakpoint: bp.name,
        width: bp.width,
        hasHorizontalScroll,
        mainContentVisible
      })
    }
    
    return results
  },

  /**
   * Test accessibility features
   */
  async testAccessibility(page) {
    const issues = []
    
    // Check for proper heading hierarchy
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all()
    const headingLevels = await Promise.all(headings.map(h => h.evaluate(el => el.tagName.toLowerCase())))
    
    let currentLevel = 0
    for (const level of headingLevels) {
      const levelNum = parseInt(level.charAt(1))
      if (levelNum > currentLevel + 1) {
        issues.push(`Heading hierarchy skip: H${currentLevel} to H${levelNum}`)
      }
      currentLevel = levelNum
    }
    
    // Check for alt text on images
    const images = await page.locator('img').all()
    for (const img of images) {
      const alt = await img.getAttribute('alt')
      if (!alt) {
        issues.push('Image missing alt attribute')
      }
    }
    
    // Check for form labels
    const inputs = await page.locator('input, textarea, select').all()
    for (const input of inputs) {
      const id = await input.getAttribute('id')
      const ariaLabel = await input.getAttribute('aria-label')
      const ariaLabelledBy = await input.getAttribute('aria-labelledby')
      
      if (!id && !ariaLabel && !ariaLabelledBy) {
        issues.push('Form input missing label or aria-label')
      }
    }
    
    return issues
  },

  /**
   * Simulate slow network conditions
   */
  async simulateSlowNetwork(page) {
    await page.route('**/*', route => {
      setTimeout(() => route.continue(), 100) // Add 100ms delay
    })
  },

  /**
   * Mock API responses for testing
   */
  async mockApiResponses(page) {
    await page.route(`${API_BASE_URL}/health`, async route => {
      await route.fulfill({ status: 200, json: { status: 'healthy' } })
    })
    
    await page.route(`${API_BASE_URL}/conversations**`, async route => {
      // Mock conversation responses
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 201,
          json: { 
            id: 'test-conversation-id', 
            title: 'Test Conversation',
            messages: [],
            created_at: new Date().toISOString()
          }
        })
      } else if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          json: { 
            id: 'test-conversation-id',
            title: 'Test Conversation',
            messages: [],
            created_at: new Date().toISOString()
          }
        })
      }
    })
    
    await page.route(`${API_BASE_URL}/conversations/**/messages**`, async route => {
      // Mock message responses
      await route.fulfill({
        status: 200,
        json: {
          id: 'test-message-id',
          content: 'This is a mock AI response for testing purposes.',
          role: 'assistant',
          created_at: new Date().toISOString()
        }
      })
    })
  },

  /**
   * Clean up test data
   */
  async cleanupTestData(page) {
    // This would typically delete test conversations from the database
    // For now, we'll just navigate away to clear state
    await page.goto('about:blank')
    await page.waitForTimeout(1000)
  },

  /**
   * Get performance metrics
   */
  async getPerformanceMetrics(page) {
    const metrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType('navigation')[0]
      return {
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime || 0,
        firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
      }
    })
    
    return metrics
  }
}

// Test data fixtures
export const testData = {
  messages: [
    'Hello, how are you?',
    'What is the weather like today?',
    'Can you help me with coding?',
    'Tell me about artificial intelligence',
    'Generate a summary of this document',
    'What are the latest trends in web development?'
  ],
  
  aiProviders: ['gemini', 'openai'],
  
  fileNames: [
    'test-document.txt',
    'sample-code.js',
    'data-report.pdf',
    'presentation.pptx',
    'spreadsheet.xlsx'
  ],
  
  shellCommands: [
    'echo "Hello World"',
    'ls -la',
    'pwd',
    'date',
    'whoami'
  ],
  
  browserActions: [
    { url: 'https://example.com', action: 'navigate' },
    { url: 'https://github.com', action: 'navigate' },
    { url: 'https://stackoverflow.com', action: 'navigate' }
  ]
}

// Export for use in tests
export { API_BASE_URL, FRONTEND_URL }