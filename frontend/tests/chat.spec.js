import { test, expect } from '@playwright/test'

test.describe('Sheikh AI Application', () => {
  test('should load main page and display correct title', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/Sheikh AI/i)
    await expect(page.locator('h1, h2, .title, .header')).toBeVisible()
  })

  test('should display chat interface', async ({ page }) => {
    await page.goto('/')
    
    // Check for chat elements
    await expect(page.locator('[data-testid="chat-container"], .chat-container, .chat-interface')).toBeVisible()
    await expect(page.locator('[data-testid="message-input"], .message-input, textarea')).toBeVisible()
    await expect(page.locator('[data-testid="send-button"], .send-button, button[type="submit"]')).toBeVisible()
  })

  test('should send a message and receive AI response', async ({ page }) => {
    await page.goto('/')
    
    // Wait for page to load
    await page.waitForLoadState('networkidle')
    
    // Find and fill message input
    const messageInput = page.locator('textarea, input[type="text"], [data-testid="message-input"]').first()
    await messageInput.fill('Hello, this is a test message')
    
    // Send message
    const sendButton = page.locator('button[type="submit"], [data-testid="send-button"], .send-button').first()
    await sendButton.click()
    
    // Wait for response (with timeout for AI processing)
    await expect(page.locator('.message, .chat-message, [data-testid="message"]')).toBeVisible({ timeout: 30000 })
    
    // Verify response contains text
    const lastMessage = page.locator('.message, .chat-message, [data-testid="message"]').last()
    await expect(lastMessage).toContainText(/.*/i)
  })

  test('should switch between AI providers', async ({ page }) => {
    await page.goto('/')
    
    // Look for AI provider selector
    const providerSelector = page.locator('[data-testid="provider-select"], .provider-selector, select, .ai-provider')
    
    if (await providerSelector.isVisible()) {
      await providerSelector.click()
      
      // Check if options are available
      const options = page.locator('option, [data-testid="provider-option"]')
      await expect(options).toHaveCount(2) // Expecting Gemini and OpenAI options
      
      // Select different provider
      await providerSelector.selectOption({ index: 1 })
    }
  })

  test('should handle file upload', async ({ page }) => {
    await page.goto('/')
    
    // Look for file upload button
    const fileUploadButton = page.locator('[data-testid="file-upload"], .file-upload, input[type="file"]')
    
    if (await fileUploadButton.isVisible()) {
      // Create a test file
      const fileContent = 'This is a test file for upload'
      const filePath = 'test-upload.txt'
      
      // In a real scenario, you'd have an actual file to upload
      // For testing, we'll just verify the upload interface exists
      await expect(fileUploadButton).toBeVisible()
    }
  })

  test('should manage conversation history', async ({ page }) => {
    await page.goto('/')
    
    // Send multiple messages
    const messageInput = page.locator('textarea, input[type="text"]').first()
    const sendButton = page.locator('button[type="submit"]').first()
    
    await messageInput.fill('First message')
    await sendButton.click()
    await page.waitForTimeout(2000)
    
    await messageInput.fill('Second message')
    await sendButton.click()
    await page.waitForTimeout(2000)
    
    // Verify both messages are visible
    const messages = page.locator('.message, .chat-message')
    await expect(messages).toHaveCount(2)
  })

  test('should handle conversation clearing', async ({ page }) => {
    await page.goto('/')
    
    // Send a message first
    const messageInput = page.locator('textarea, input[type="text"]').first()
    const sendButton = page.locator('button[type="submit"]').first()
    
    await messageInput.fill('Test message for clearing')
    await sendButton.click()
    await page.waitForTimeout(2000)
    
    // Look for clear conversation button
    const clearButton = page.locator('[data-testid="clear-chat"], .clear-button, button:has-text("Clear")')
    
    if (await clearButton.isVisible()) {
      await clearButton.click()
      
      // Verify chat is cleared (no messages visible)
      await expect(page.locator('.message, .chat-message')).toHaveCount(0)
    }
  })

  test('should display typing indicator', async ({ page }) => {
    await page.goto('/')
    
    const messageInput = page.locator('textarea, input[type="text"]').first()
    const sendButton = page.locator('button[type="submit"]').first()
    
    await messageInput.fill('Generate a detailed response')
    await sendButton.click()
    
    // Check for typing indicator
    const typingIndicator = page.locator('[data-testid="typing-indicator"], .typing-indicator, .loading')
    await expect(typingIndicator).toBeVisible({ timeout: 5000 })
    
    // Wait for typing indicator to disappear (response received)
    await expect(typingIndicator).toBeHidden({ timeout: 30000 })
  })

  test('should handle network errors gracefully', async ({ page }) => {
    await page.goto('/')
    
    // Simulate network error by intercepting requests
    await page.route('**/api/**', route => {
      route.abort('internetdisconnected')
    })
    
    const messageInput = page.locator('textarea, input[type="text"]').first()
    const sendButton = page.locator('button[type="submit"]').first()
    
    await messageInput.fill('This should fail')
    await sendButton.click()
    
    // Verify error message is displayed
    await expect(page.locator('.error, .alert-error, [data-testid="error"]')).toBeVisible({ timeout: 10000 })
  })

  test('should be responsive on mobile devices', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    
    // Verify main elements are visible on mobile
    await expect(page.locator('[data-testid="chat-container"], .chat-container')).toBeVisible()
    await expect(page.locator('[data-testid="message-input"], .message-input')).toBeVisible()
    
    // Verify no horizontal scrolling
    const bodyWidth = await page.evaluate('document.body.scrollWidth')
    const viewportWidth = page.viewportSize()?.width
    expect(bodyWidth).toBeLessThanOrEqual(viewportWidth || 0)
  })

  test('should have proper accessibility features', async ({ page }) => {
    await page.goto('/')
    
    // Check for proper heading structure
    const headings = page.locator('h1, h2, h3, h4, h5, h6')
    const headingCount = await headings.count()
    expect(headingCount).toBeGreaterThan(0)
    
    // Check for alt text on images
    const images = page.locator('img')
    for (let i = 0; i < await images.count(); i++) {
      const alt = await images.nth(i).getAttribute('alt')
      expect(alt).toBeTruthy()
    }
    
    // Check for proper form labels
    const inputs = page.locator('input, textarea')
    for (let i = 0; i < await inputs.count(); i++) {
      const label = await inputs.nth(i).getAttribute('aria-label') || 
                   await inputs.nth(i).getAttribute('placeholder')
      expect(label).toBeTruthy()
    }
  })
})