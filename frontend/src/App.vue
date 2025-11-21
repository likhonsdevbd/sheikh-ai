<template>
  <div id="app" class="sheikh-app">
    <a-config-provider
      :theme="{
        token: {
          colorPrimary: '#722ed1',
          colorSuccess: '#52c41a',
          colorWarning: '#faad14',
          colorError: '#ff4d4f',
          borderRadius: 6,
          fontSize: 14,
        },
      }"
    >
      <a-layout class="app-layout">
        <!-- Header -->
        <a-layout-header class="app-header">
          <div class="header-content">
            <div class="logo">
              <a-avatar :size="32" style="background: #722ed1">
                <template #icon><RobotOutlined /></template>
              </a-avatar>
              <span class="app-title">Sheikh AI Assistant</span>
            </div>
            <div class="header-actions">
              <a-button-group>
                <a-button @click="createNewSession" type="primary" ghost>
                  <template #icon><PlusOutlined /></template>
                  New Chat
                </a-button>
                <a-button @click="showSettings = true">
                  <template #icon><SettingOutlined /></template>
                </a-button>
              </a-button-group>
            </div>
          </div>
        </a-layout-header>

        <a-layout class="main-layout">
          <!-- Sidebar with Session List -->
          <a-layout-sider
            v-model:collapsed="sidebarCollapsed"
            :width="300"
            :collapsed-width="80"
            class="sidebar"
          >
            <div class="sidebar-header">
              <a-input
                v-model:value="searchQuery"
                placeholder="Search conversations..."
                :prefix="sidebarCollapsed ? null : <SearchOutlined />"
                size="small"
              />
            </div>
            
            <div class="session-list">
              <div class="session-item" v-for="session in filteredSessions" :key="session.session_id">
                <a-card
                  :class="['session-card', { active: currentSessionId === session.session_id }]"
                  @click="selectSession(session.session_id)"
                  :hoverable="true"
                >
                  <a-card-meta :title="session.title" :description="getSessionDescription(session)">
                    <template #avatar>
                      <a-avatar size="small" style="background: #e6f7ff">
                        <template #icon><MessageOutlined /></template>
                      </a-avatar>
                    </template>
                  </a-card-meta>
                  <template #actions>
                    <a-dropdown>
                      <MoreOutlined />
                      <template #overlay>
                        <a-menu>
                          <a-menu-item key="rename" @click="renameSession(session.session_id)">
                            <EditOutlined /> Rename
                          </a-menu-item>
                          <a-menu-item key="stop" @click="stopSession(session.session_id)" :disabled="session.status === 'stopped'">
                            <PauseOutlined /> Stop
                          </a-menu-item>
                          <a-menu-item key="delete" danger @click="deleteSession(session.session_id)">
                            <DeleteOutlined /> Delete
                          </a-menu-item>
                        </a-menu>
                      </template>
                    </a-dropdown>
                  </template>
                </a-card>
              </div>
            </div>
          </a-layout-sider>

          <!-- Main Content Area -->
          <a-layout-content class="main-content">
            <div class="content-wrapper">
              <!-- Enhanced Chat with CopilotKit Integration -->
              <div class="enhanced-chat-container" v-if="useEnhancedChat">
                <!-- Toggle between traditional and enhanced chat -->
                <div class="chat-mode-toggle">
                  <a-segmented 
                    v-model:value="chatMode" 
                    :options="[
                      { label: 'Traditional Chat', value: 'traditional' },
                      { label: 'Enhanced AI', value: 'enhanced' }
                    ]"
                    @change="handleModeChange"
                  />
                </div>
                
                <!-- Traditional Chat Interface -->
                <div class="chat-area" v-if="currentSessionId && chatMode === 'traditional'">
                <div class="messages-container" ref="messagesContainer">
                  <div v-for="message in currentMessages" :key="message.id" class="message-wrapper">
                    <a-card
                      :class="['message-card', message.role === 'user' ? 'user-message' : 'assistant-message']"
                      :bordered="false"
                    >
                      <a-card-meta>
                        <template #avatar>
                          <a-avatar :style="{ background: message.role === 'user' ? '#52c41a' : '#722ed1' }">
                            <template #icon>
                              <UserOutlined v-if="message.role === 'user'" />
                              <RobotOutlined v-else />
                            </template>
                          </a-avatar>
                        </template>
                        <template #description>
                          <div class="message-content">
                            <MarkdownRenderer :content="message.content" />
                          </div>
                          <div class="message-meta">
                            <span>{{ formatTime(message.timestamp) }}</span>
                          </div>
                        </template>
                      </a-card-meta>
                    </a-card>
                  </div>
                  
                  <!-- Streaming indicator -->
                  <div v-if="isStreaming" class="streaming-indicator">
                    <a-spin size="small" />
                    <span>AI is thinking...</span>
                  </div>
                </div>

                <!-- Enhanced Chat Input with Rich Features -->
                <div class="chat-input-area">
                  <a-input
                    v-model:value="currentMessage"
                    placeholder="Type your message here..."
                    size="large"
                    :autosize="{ minRows: 1, maxRows: 4 }"
                    @keydown="handleKeyDown"
                    @input="handleInputChange"
                  />
                  <div class="input-actions">
                    <a-button-group>
                      <a-button @click="toggleToolPanel" :type="showToolPanel ? 'primary' : 'default'">
                        <template #icon><ToolOutlined /></template>
                        Tools
                      </a-button>
                      <a-button @click="toggleGenerativeUI" :type="showGenerativeUI ? 'primary' : 'default'">
                        <template #icon><AppstoreOutlined /></template>
                        Gen UI
                      </a-button>
                      <a-button @click="sendMessage" :loading="isStreaming" :disabled="!currentMessage.trim()">
                        <template #icon><SendOutlined /></template>
                        Send
                      </a-button>
                    </a-button-group>
                  </div>
                </div>
              </div>

              <!-- Enhanced AI Chat with CopilotKit -->
              <div class="enhanced-ai-chat" v-if="chatMode === 'enhanced'">
                <div class="copilot-header">
                  <h3>Enhanced AI Assistant</h3>
                  <p>Powered by CopilotKit & AG-UI Protocol</p>
                </div>
                <div class="rich-interactions">
                  <!-- Streaming Response Display -->
                  <div class="streaming-response" v-if="isStreamingEnhanced">
                    <a-spin />
                    <span>AI is processing your request...</span>
                  </div>
                  
                  <!-- Generative UI Components -->
                  <div v-if="generativeUIComponents.length > 0" class="generative-ui-section">
                    <h4>AI-Generated Interface</h4>
                    <div v-for="(component, index) in generativeUIComponents" :key="index" class="ui-component">
                      <component :is="getComponentName(component.type)" :data="component" />
                    </div>
                  </div>
                  
                  <!-- Available Actions -->
                  <div v-if="availableActions.length > 0" class="actions-section">
                    <h4>Available Actions</h4>
                    <div class="action-grid">
                      <a-card 
                        v-for="action in availableActions" 
                        :key="action.name"
                        :hoverable="true"
                        class="action-card"
                        @click="executeAction(action)"
                      >
                        <a-card-meta 
                          :title="action.name"
                          :description="action.description"
                        >
                          <template #avatar>
                            <component :is="action.icon || 'ApiOutlined'" />
                          </template>
                        </a-card-meta>
                      </a-card>
                    </div>
                  </div>
                </div>
                
                <!-- Enhanced Input -->
                <div class="enhanced-input-area">
                  <a-input
                    v-model:value="enhancedInput"
                    placeholder="Ask Sheikh to help with code, research, analysis..."
                    size="large"
                    @keydown="handleEnhancedKeyDown"
                  />
                  <div class="enhanced-input-actions">
                    <a-button-group>
                      <a-button @click="generateCode">
                        <template #icon><CodeOutlined /></template>
                        Generate Code
                      </a-button>
                      <a-button @click="performWebSearch">
                        <template #icon><SearchOutlined /></template>
                        Web Search
                      </a-button>
                      <a-button @click="analyzeData">
                        <template #icon><BarChartOutlined /></template>
                        Analyze Data
                      </a-button>
                      <a-button type="primary" @click="sendEnhancedMessage" :disabled="!enhancedInput.trim()">
                        <template #icon><SendOutlined /></template>
                        Send
                      </a-button>
                    </a-button-group>
                  </div>
                </div>
              </div>

              <!-- Welcome Screen -->
              <div v-else class="welcome-screen">
                <div class="welcome-content">
                  <a-result
                    icon={<RobotOutlined style="color: #722ed1" />}
                    title="Welcome to Sheikh AI Assistant"
                    sub-title="Your intelligent conversation partner with advanced AI capabilities"
                  >
                    <template #extra>
                      <a-button type="primary" size="large" @click="createNewSession">
                        <template #icon><PlusOutlined /></template>
                        Start New Conversation
                      </a-button>
                    </template>
                  </a-result>
                  
                  <div class="feature-showcase">
                    <a-row :gutter="[16, 16]">
                      <a-col :span="6" v-for="feature in features" :key="feature.title">
                        <a-card :hoverable="true" class="feature-card">
                          <a-card-meta>
                            <template #avatar>
                              <component :is="feature.icon" style="font-size: 24px; color: #722ed1" />
                            </template>
                            <template #title>{{ feature.title }}</template>
                            <template #description>{{ feature.description }}</template>
                          </a-card-meta>
                        </a-card>
                      </a-col>
                    </a-row>
                  </div>
                </div>
              </div>
            </div>
          </a-layout-content>

          <!-- Tool Panel -->
          <a-drawer
            v-model:open="showToolPanel"
            title="AI Tools & Environment"
            placement="right"
            :width="400"
            class="tool-panel-drawer"
          >
            <a-tabs v-model:activeKey="activeTool">
              <!-- Terminal -->
              <a-tab-pane key="terminal" tab="Terminal">
                <div class="terminal-container">
                  <div class="terminal-header">
                    <a-space>
                      <a-tag color="blue">Shell</a-tag>
                      <a-button size="small" @click="clearTerminal">
                        <template #icon><DeleteOutlined /></template>
                        Clear
                      </a-button>
                    </a-space>
                  </div>
                  <div class="terminal-output" ref="terminalOutput">
                    <div v-for="output in terminalOutputs" :key="output.id" class="terminal-line">
                      <span class="prompt">{{ output.prompt }}</span>
                      <span class="command">{{ output.command }}</span>
                      <pre class="output">{{ output.output }}</pre>
                    </div>
                  </div>
                  <div class="terminal-input">
                    <a-input
                      v-model:value="terminalCommand"
                      placeholder="Enter command..."
                      size="small"
                      @keydown="handleTerminalKeyDown"
                    />
                  </div>
                </div>
              </a-tab-pane>

              <!-- File Explorer -->
              <a-tab-pane key="files" tab="Files">
                <div class="file-explorer">
                  <div class="file-path">
                    <a-breadcrumb>
                      <a-breadcrumb-item v-for="path in currentPath" :key="path">
                        <span @click="navigateToPath(path)" style="cursor: pointer">{{ path }}</span>
                      </a-breadcrumb-item>
                    </a-breadcrumb>
                  </div>
                  <div class="file-list">
                    <div v-for="item in fileList" :key="item.path" class="file-item">
                      <a-card size="small" hoverable @click="handleFileClick(item)">
                        <a-space>
                          <component :is="item.isDirectory ? FolderOutlined : FileOutlined" />
                          <span>{{ item.name }}</span>
                        </a-space>
                      </a-card>
                    </div>
                  </div>
                </div>
              </a-tab-pane>

              <!-- Browser -->
              <a-tab-pane key="browser" tab="Browser">
                <div class="browser-container">
                  <div class="browser-controls">
                    <a-input-group compact>
                      <a-select v-model:value="browserUrl" style="width: calc(100% - 80px)">
                        <a-input
                          v-model:value="browserUrl"
                          placeholder="Enter URL..."
                          @keydown.enter="navigateBrowser"
                        />
                      </a-select>
                      <a-button @click="navigateBrowser" type="primary">
                        <template #icon><GlobalOutlined /></template>
                        Go
                      </a-button>
                    </a-input-group>
                  </div>
                  <div class="browser-frame">
                    <iframe
                      v-if="currentSessionId"
                      :src="`http://localhost:9222`"
                      width="100%"
                      height="300"
                      frameborder="0"
                    ></iframe>
                    <div v-else class="browser-placeholder">
                      <a-empty description="Open a session to use browser automation" />
                    </div>
                  </div>
                </div>
              </a-tab-pane>

              <!-- Search -->
              <a-tab-pane key="search" tab="Search">
                <div class="search-container">
                  <a-input-search
                    v-model:value="searchQuery"
                    placeholder="Search the web..."
                    size="large"
                    @search="performWebSearch"
                  />
                  <div class="search-results" v-if="searchResults.length > 0">
                    <a-list
                      :data-source="searchResults"
                      :renderItem="renderSearchResult"
                      size="small"
                    />
                  </div>
                </div>
              </a-tab-pane>
            </a-tabs>
          </a-drawer>
        </a-layout>
      </a-layout>

      <!-- Settings Modal -->
      <a-modal
        v-model:open="showSettings"
        title="Settings"
        width="600px"
        :footer="null"
      >
        <a-form :model="settings" layout="vertical">
          <a-form-item label="OpenAI API Key">
            <a-input-password v-model:value="settings.openaiApiKey" placeholder="Enter your OpenAI API key" />
          </a-form-item>
          <a-form-item label="Default Model">
            <a-select v-model:value="settings.openaiModel">
              <a-select-option value="gpt-4">GPT-4</a-select-option>
              <a-select-option value="gpt-3.5-turbo">GPT-3.5 Turbo</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="Theme">
            <a-switch v-model:checked="settings.darkMode" checked-children="Dark" un-checked-children="Light" />
          </a-form-item>
        </a-form>
      </a-modal>
    </a-config-provider>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { message, modal, notification } from 'ant-design-vue'
import {
  RobotOutlined, PlusOutlined, SettingOutlined, SearchOutlined,
  MessageOutlined, MoreOutlined, EditOutlined, PauseOutlined, DeleteOutlined,
  UserOutlined, ToolOutlined, SendOutlined, FolderOutlined, FileOutlined,
  GlobalOutlined, AppstoreOutlined, CodeOutlined, BarChartOutlined, ApiOutlined
} from '@ant-design/icons-vue'
import { useChatStore } from './stores/chat'
import { useSessionStore } from './stores/session'
import { useSettingsStore } from './stores/settings'
import MarkdownRenderer from './components/MarkdownRenderer.vue'

// Stores
const chatStore = useChatStore()
const sessionStore = useSessionStore()
const settingsStore = useSettingsStore()

// Reactive data
const sidebarCollapsed = ref(false)
const searchQuery = ref('')
const showToolPanel = ref(false)
const activeTool = ref('terminal')
const showSettings = ref(false)

// Chat interface
const currentMessage = ref('')
const isStreaming = ref(false)
const messagesContainer = ref<HTMLElement>()

// Enhanced Chat Mode
const useEnhancedChat = ref(true)
const chatMode = ref('enhanced')
const enhancedInput = ref('')
const isStreamingEnhanced = ref(false)
const showGenerativeUI = ref(false)
const generativeUIComponents = ref<any[]>([])
const availableActions = ref<any[]>([])

// Terminal
const terminalCommand = ref('')
const terminalOutputs = ref<any[]>([])

// File explorer
const currentPath = ref(['/'])
const fileList = ref<any[]>([])

// Browser
const browserUrl = ref('')

// Search
const searchQueryVal = ref('')
const searchResults = ref<any[]>([])

// Settings
const settings = ref({
  openaiApiKey: '',
  openaiModel: 'gpt-4',
  darkMode: false
})

// Computed properties
const currentSessionId = computed(() => sessionStore.currentSessionId)
const currentMessages = computed(() => chatStore.getCurrentMessages)
const sessions = computed(() => sessionStore.sessions)

const filteredSessions = computed(() => {
  if (!searchQuery.value) return sessions.value
  return sessions.value.filter(session => 
    session.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    session.latest_message?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const features = ref([
  {
    icon: 'MessageOutlined',
    title: 'Intelligent Chat',
    description: 'Advanced conversation capabilities with AI assistance'
  },
  {
    icon: 'TerminalOutlined',
    title: 'Shell Commands',
    description: 'Execute shell commands in secure sandbox environment'
  },
  {
    icon: 'FolderOutlined',
    title: 'File Operations',
    description: 'Read, write, and manage files with file system access'
  },
  {
    icon: 'GlobalOutlined',
    title: 'Browser Automation',
    description: 'Automated web browsing with Chrome DevTools integration'
  }
])

// Methods
const createNewSession = async () => {
  try {
    const result = await sessionStore.createSession()
    if (result.code === 0) {
      message.success('New conversation created')
      await loadSessions()
    }
  } catch (error) {
    message.error('Failed to create session')
  }
}

const selectSession = async (sessionId: string) => {
  try {
    await sessionStore.selectSession(sessionId)
    await loadSessionMessages(sessionId)
  } catch (error) {
    message.error('Failed to load session')
  }
}

const deleteSession = async (sessionId: string) => {
  modal.confirm({
    title: 'Delete Conversation',
    content: 'Are you sure you want to delete this conversation? This action cannot be undone.',
    onOk: async () => {
      try {
        const result = await sessionStore.deleteSession(sessionId)
        if (result.code === 0) {
          message.success('Conversation deleted')
          await loadSessions()
        }
      } catch (error) {
        message.error('Failed to delete session')
      }
    }
  })
}

const stopSession = async (sessionId: string) => {
  try {
    const result = await sessionStore.stopSession(sessionId)
    if (result.code === 0) {
      message.success('Session stopped')
      await loadSessions()
    }
  } catch (error) {
    message.error('Failed to stop session')
  }
}

const sendMessage = async () => {
  if (!currentMessage.value.trim() || !currentSessionId.value) return

  const messageText = currentMessage.value.trim()
  currentMessage.value = ''

  try {
    isStreaming.value = true
    
    // Add user message immediately
    await chatStore.addMessage(currentSessionId.value, 'user', messageText)
    
    // Stream AI response
    await chatStore.sendStreamingMessage(currentSessionId.value, messageText)
    
  } catch (error) {
    message.error('Failed to send message')
  } finally {
    isStreaming.value = false
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const handleInputChange = () => {
  // Auto-resize input if needed
}

const toggleToolPanel = () => {
  showToolPanel.value = !showToolPanel.value
}

const formatTime = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleTimeString()
}

const getSessionDescription = (session: any) => {
  return session.latest_message || 'No messages yet'
}

const loadSessions = async () => {
  await sessionStore.loadSessions()
}

const loadSessionMessages = async (sessionId: string) => {
  await chatStore.loadSessionMessages(sessionId)
}

// Terminal methods
const clearTerminal = () => {
  terminalOutputs.value = []
}

const handleTerminalKeyDown = async (event: KeyboardEvent) => {
  if (event.key === 'Enter' && terminalCommand.value.trim()) {
    const command = terminalCommand.value.trim()
    terminalCommand.value = ''
    
    // Add command to output
    terminalOutputs.value.push({
      id: Date.now(),
      prompt: '$',
      command,
      output: 'Executing command...'
    })
    
    try {
      // This would integrate with the backend terminal API
      const response = await fetch(`/api/v1/sessions/${currentSessionId.value}/shell`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ shell_session_id: 'main', command })
      })
      
      const result = await response.json()
      if (result.code === 0) {
        // Update output with actual result
        const lastOutput = terminalOutputs.value[terminalOutputs.value.length - 1]
        lastOutput.output = result.data.output || 'Command executed'
      }
    } catch (error) {
      const lastOutput = terminalOutputs.value[terminalOutputs.value.length - 1]
      lastOutput.output = 'Error executing command'
    }
  }
}

// File explorer methods
const handleFileClick = async (item: any) => {
  if (item.isDirectory) {
    currentPath.value = [...currentPath.value, item.name]
    await loadFileList()
  } else {
    // Open file
    try {
      const response = await fetch(`/api/v1/sessions/${currentSessionId.value}/file`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: [...currentPath.value, item.name].join('/') })
      })
      
      const result = await response.json()
      if (result.code === 0) {
        modal.info({
          title: `File: ${item.name}`,
          content: `<pre>${result.data.content}</pre>`,
          width: 800
        })
      }
    } catch (error) {
      message.error('Failed to open file')
    }
  }
}

const navigateToPath = (path: string) => {
  const pathIndex = currentPath.value.indexOf(path)
  currentPath.value = currentPath.value.slice(0, pathIndex + 1)
  loadFileList()
}

const loadFileList = async () => {
  // This would load the file list from the backend
  // For now, placeholder implementation
  fileList.value = []
}

// Browser methods
const navigateBrowser = () => {
  if (browserUrl.value && currentSessionId.value) {
    // This would integrate with browser automation API
    message.info('Navigating browser...')
  }
}

// Search methods
const performWebSearch = async () => {
  if (!searchQueryVal.value.trim()) return
  
  try {
    // This would integrate with search API
    searchResults.value = []
    message.info('Searching...')
  } catch (error) {
    message.error('Search failed')
  }
}

const renderSearchResult = (item: any) => {
  return (
    <a-list-item>
      <a-list-item-meta
        title={item.title}
        description={item.snippet}
      />
    </a-list-item>
  )
}

// Enhanced Chat Methods
const handleModeChange = (value: string) => {
  chatMode.value = value
  message.info(`Switched to ${value} chat mode`)
}

const toggleGenerativeUI = () => {
  showGenerativeUI.value = !showGenerativeUI.value
  if (showGenerativeUI.value) {
    // Simulate generating UI components
    generateUIComponents()
  }
}

const generateUIComponents = () => {
  generativeUIComponents.value = [
    {
      type: 'capability-showcase',
      title: 'Sheikh Capabilities',
      capabilities: [
        {
          name: 'Code Generation',
          description: 'Generate and review code in multiple languages',
          icon: 'CodeOutlined'
        },
        {
          name: 'Web Research',
          description: 'Search and analyze information from the web',
          icon: 'SearchOutlined'
        },
        {
          name: 'Data Analysis',
          description: 'Analyze datasets and generate insights',
          icon: 'BarChartOutlined'
        },
        {
          name: 'Browser Automation',
          description: 'Automate web browsing and interaction',
          icon: 'GlobalOutlined'
        }
      ]
    }
  ]
}

const sendEnhancedMessage = async () => {
  if (!enhancedInput.value.trim()) return

  const message = enhancedInput.value.trim()
  enhancedInput.value = ''
  isStreamingEnhanced.value = true

  try {
    // Simulate enhanced AI processing
    await simulateEnhancedAIResponse(message)
  } catch (error) {
    message.error('Failed to process enhanced request')
  } finally {
    isStreamingEnhanced.value = false
  }
}

const simulateEnhancedAIResponse = async (input: string) => {
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  // Determine response type based on input
  if (input.toLowerCase().includes('code')) {
    availableActions.value = [
      {
        name: 'generateCode',
        description: 'Generate code for your request',
        icon: 'CodeOutlined'
      },
      {
        name: 'reviewCode',
        description: 'Review existing code',
        icon: 'EyeOutlined'
      }
    ]
    
    generativeUIComponents.value = [
      {
        type: 'code-preview',
        language: 'javascript',
        code: `function hello() {
  console.log("Hello from Sheikh!");
  return "AI-powered code generation";
}`
      }
    ]
  } else if (input.toLowerCase().includes('search')) {
    availableActions.value = [
      {
        name: 'webSearch',
        description: 'Perform comprehensive web search',
        icon: 'SearchOutlined'
      },
      {
        name: 'extractContent',
        description: 'Extract content from web pages',
        icon: 'DownloadOutlined'
      }
    ]
  } else {
    availableActions.value = [
      {
        name: 'generalChat',
        description: 'Continue the conversation',
        icon: 'MessageOutlined'
      },
      {
        name: 'switchMode',
        description: 'Switch to different capabilities',
        icon: 'SwapOutlined'
      }
    ]
  }
}

const handleEnhancedKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendEnhancedMessage()
  }
}

const executeAction = (action: any) => {
  message.info(`Executing action: ${action.name}`)
  // Implement action execution logic
}

const getComponentName = (type: string) => {
  const componentMap: Record<string, string> = {
    'capability-showcase': 'CapabilityShowcase',
    'code-preview': 'CodePreview',
    'data-visualization': 'DataVisualization',
    'web-results': 'WebResults'
  }
  return componentMap[type] || 'div'
}

const generateCode = () => {
  enhancedInput.value = "Generate Python code for data analysis"
  sendEnhancedMessage()
}

const performWebSearch = () => {
  enhancedInput.value = "Search for latest AI research papers"
  sendEnhancedMessage()
}

const analyzeData = () => {
  enhancedInput.value = "Help me analyze this dataset"
  sendEnhancedMessage()
}

// Load initial data
onMounted(async () => {
  await loadSessions()
  
  // Load settings
  Object.assign(settings, settingsStore.settings)
})

// Watch for current messages to scroll to bottom
watch(currentMessages, async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
})
</script>

<style scoped>
.sheikh-app {
  height: 100vh;
  width: 100vw;
}

.app-layout {
  height: 100vh;
}

.app-header {
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
  padding: 0 16px;
  height: 56px;
  line-height: 56px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-title {
  font-size: 18px;
  font-weight: 600;
  color: #722ed1;
}

.main-layout {
  height: calc(100vh - 56px);
}

.sidebar {
  background: #fafafa;
  border-right: 1px solid #f0f0f0;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.session-list {
  padding: 8px;
  height: calc(100% - 73px);
  overflow-y: auto;
}

.session-item {
  margin-bottom: 8px;
}

.session-card {
  cursor: pointer;
  transition: all 0.3s;
}

.session-card.active {
  border-color: #722ed1;
  box-shadow: 0 0 0 2px rgba(114, 46, 209, 0.1);
}

.session-card:hover {
  border-color: #722ed1;
}

.main-content {
  background: #fff;
}

.content-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.welcome-screen {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-content {
  max-width: 800px;
  text-align: center;
}

.feature-showcase {
  margin-top: 40px;
}

.feature-card {
  text-align: center;
}

.chat-area {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
}

.message-wrapper {
  margin-bottom: 16px;
}

.message-card {
  border-radius: 12px;
}

.user-message {
  margin-left: 64px;
}

.assistant-message {
  margin-right: 64px;
}

.message-content {
  line-height: 1.6;
}

.message-meta {
  margin-top: 8px;
  font-size: 12px;
  color: #8c8c8c;
}

.streaming-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
  color: #722ed1;
}

.chat-input-area {
  padding: 16px;
  border-top: 1px solid #f0f0f0;
  background: #fff;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.tool-panel-drawer .ant-drawer-body {
  padding: 0;
}

.terminal-container {
  padding: 16px;
}

.terminal-header {
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.terminal-output {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px;
  border-radius: 4px;
  height: 300px;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}

.terminal-line {
  margin-bottom: 4px;
}

.prompt {
  color: #4ec9b0;
  margin-right: 8px;
}

.command {
  color: #ce9178;
  margin-right: 8px;
}

.output {
  margin: 0;
  color: #d4d4d4;
}

.terminal-input {
  margin-top: 12px;
}

.file-explorer {
  padding: 16px;
}

.file-path {
  margin-bottom: 16px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
}

.file-list {
  height: 400px;
  overflow-y: auto;
}

.file-item {
  margin-bottom: 4px;
}

.browser-container {
  padding: 16px;
}

.browser-controls {
  margin-bottom: 16px;
}

.browser-frame {
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  height: 400px;
}

.browser-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.search-container {
  padding: 16px;
}

.search-results {
  margin-top: 16px;
  max-height: 500px;
  overflow-y: auto;
}
</style>