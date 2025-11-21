import { defineComponent, ref, computed, watch, onMounted, nextTick } from 'vue'
import { 
  Card, Button, Input, Progress, Tag, Spin, Avatar, Typography, 
  Tabs, Modal, Drawer, Select, Space, Row, Col, Alert, Divider,
  Upload, Tooltip, Switch, Rate, Progress as ProgressComponent
} from 'ant-design-vue'
import { 
  Brain, Code, Search, Image, FileText, Database, MessageSquare, 
  BookOpen, PlayCircle, PauseCircle, Download, Share2, Copy,
  Zap, Sparkles, Clock, CheckCircle, AlertCircle, Info,
  ChevronRight, Settings, Lightbulb, Target, Cpu, Loader
} from 'lucide-react'
import { message } from 'ant-design-vue'
import { sheikhAI, SHEIKH_AI_CAPABILITIES, SheikhAICapability, createEnhancedResponse } from '../lib/ai-ssdk'

export const EnhancedAIInterface = defineComponent({
  name: 'EnhancedAIInterface',
  props: {
    currentProvider: {
      type: String as () => 'google' | 'openai',
      default: 'google'
    }
  },
  setup(props) {
    // Reactive state following accessibility guidelines
    const loading = ref(false)
    const isThinking = ref(false)
    const thinkingLevel = ref<'low' | 'medium' | 'high'>('medium')
    const showAdvanced = ref(false)
    const streamingResponse = ref('')
    const currentResponse = ref<any>(null)
    const responseMetadata = ref<any>({})
    const selectedCapability = ref<SheikhAICapability>(SHEIKH_AI_CAPABILITIES[0])
    
    // Accessible input states
    const inputValue = ref('')
    const inputFocused = ref(false)
    const inputError = ref('')
    const canSubmit = computed(() => inputValue.value.trim().length > 0 && !loading.value)
    
    // File upload handling
    const uploadedFiles = ref<File[]>([])
    const dragOver = ref(false)
    
    // Performance tracking
    const startTime = ref<number>(0)
    const responseTime = ref<number>(0)
    
    // Capability selection
    const selectedCategory = ref<string>('all')
    const filteredCapabilities = computed(() => {
      if (selectedCategory.value === 'all') return SHEIKH_AI_CAPABILITIES
      return SHEIKH_AI_CAPABILITIES.filter(cap => cap.category === selectedCategory.value)
    })
    
    // Accessibility: Focus management
    const focusFirstError = () => {
      const errorElement = document.querySelector('.input-error') as HTMLElement
      if (errorElement) {
        errorElement.focus()
      }
    }
    
    // Streaming with accessible feedback
    const streamResponse = async (prompt: string, capability: SheikhAICapability) => {
      loading.value = true
      isThinking.value = capability.requiresThinking || false
      startTime.value = performance.now()
      streamingResponse.value = ''
      currentResponse.value = null
      
      try {
        if (capability.supportsStreaming) {
          const stream = await sheikhAI.streamWithEnhancedUI(prompt, (chunk) => {
            streamingResponse.value += chunk
          })
          
          currentResponse.value = await stream
        } else {
          const result = await createEnhancedResponse(prompt, capability, {
            thinkingLevel: thinkingLevel.value,
            context: 'enhanced-interface'
          })
          
          currentResponse.value = result
          streamingResponse.value = result.text
        }
        
        responseTime.value = performance.now() - startTime.value
        responseMetadata.value = {
          provider: props.currentProvider,
          thinkingLevel: thinkingLevel.value,
          capability: capability.id,
          responseTime: responseTime.value,
          timestamp: new Date().toISOString()
        }
        
        message.success('Response generated successfully')
      } catch (error) {
        console.error('AI Service Error:', error)
        message.error('Failed to generate response. Please try again.')
        inputError.value = 'Failed to process request. Please check your input and try again.'
        focusFirstError()
      } finally {
        loading.value = false
        isThinking.value = false
      }
    }
    
    // Accessible file upload
    const handleFileUpload = (files: File[]) => {
      uploadedFiles.value = [...uploadedFiles.value, ...files]
      message.success(`${files.length} file(s) added`)
    }
    
    const removeFile = (index: number) => {
      uploadedFiles.value.splice(index, 1)
    }
    
    // Keyboard accessibility
    const handleKeyDown = (event: KeyboardEvent) => {
      // Enter submits, unless in textarea
      if (event.key === 'Enter' && !event.shiftKey && canSubmit.value) {
        event.preventDefault()
        submitPrompt()
      }
      
      // Accessibility shortcuts
      if (event.metaKey || event.ctrlKey) {
        switch (event.key) {
          case 'Enter':
            event.preventDefault()
            submitPrompt()
            break
          case '/':
            event.preventDefault()
            // Focus search/filter
            break
        }
      }
    }
    
    // Main submission handler
    const submitPrompt = async () => {
      if (!canSubmit.value) {
        inputError.value = 'Please enter a valid prompt'
        return
      }
      
      inputError.value = ''
      await streamResponse(inputValue.value, selectedCapability.value)
    }
    
    // Copy to clipboard with accessibility
    const copyToClipboard = async (text: string) => {
      try {
        await navigator.clipboard.writeText(text)
        message.success('Copied to clipboard')
      } catch (error) {
        message.error('Failed to copy to clipboard')
      }
    }
    
    // Dynamic icon mapping
    const getCapabilityIcon = (iconName: string) => {
      const iconMap: Record<string, any> = {
        Brain, Code, Search, Image, FileText, Database, MessageSquare, BookOpen
      }
      return iconMap[iconName] || Brain
    }
    
    // Accessibility: Loading state announcements
    const announceLoadingState = (isLoading: boolean, message?: string) => {
      const liveRegion = document.getElementById('live-region')
      if (liveRegion) {
        liveRegion.textContent = isLoading ? 
          (message || 'AI is processing your request') : 
          'Response completed'
      }
    }
    
    // Mount effects
    onMounted(() => {
      // Focus management for accessibility
      const mainInput = document.getElementById('main-ai-input')
      if (mainInput) {
        mainInput.focus()
      }
    })
    
    // React to loading state changes
    watch(loading, (newLoading) => {
      announceLoadingState(newLoading)
    })
    
    return {
      // State
      loading,
      isThinking,
      thinkingLevel,
      showAdvanced,
      streamingResponse,
      currentResponse,
      responseMetadata,
      selectedCapability,
      inputValue,
      inputFocused,
      inputError,
      canSubmit,
      uploadedFiles,
      dragOver,
      startTime,
      responseTime,
      selectedCategory,
      filteredCapabilities,
      
      // Methods
      handleKeyDown,
      submitPrompt,
      handleFileUpload,
      removeFile,
      copyToClipboard,
      getCapabilityIcon
    }
  },
  template: `
    <div class="enhanced-ai-interface">
      <!-- Live region for screen readers -->
      <div id="live-region" aria-live="polite" class="sr-only"></div>
      
      <!-- Header with accessible branding -->
      <div class="ai-header">
        <div class="header-content">
          <div class="brand-info">
            <Avatar :size="40" style="background: linear-gradient(135deg, #722ed1, #531dab)">
              <template #icon><Sparkles /></template>
            </Avatar>
            <div class="brand-text">
              <Typography.Title :level="3" style="margin: 0; color: #722ed1">
                Sheikh AI Assistant
              </Typography.Title>
              <Typography.Text type="secondary">
                Powered by AI SDK & Gemini 3 Pro Preview
              </Typography.Text>
            </div>
          </div>
          
          <div class="header-controls">
            <Select
              v-model:value="thinkingLevel"
              size="small"
              :options="[
                { label: 'Fast', value: 'low' },
                { label: 'Balanced', value: 'medium' },
                { label: 'Deep', value: 'high' }
              ]"
              @change="() => message.info('Thinking level updated')"
            />
            <Button 
              @click="showAdvanced = !showAdvanced"
              :type="showAdvanced ? 'primary' : 'default'"
              size="small"
            >
              <template #icon><Settings /></template>
              Advanced
            </Button>
          </div>
        </div>
      </div>
      
      <!-- Main content area -->
      <div class="main-content">
        <!-- Capabilities selection -->
        <Card class="capabilities-section" :bordered="false">
          <div class="capabilities-header">
            <Typography.Title :level="4" style="margin: 0 0 16px 0">
              AI Capabilities
            </Typography.Title>
            <Select
              v-model:value="selectedCategory"
              size="small"
              style="width: 200px"
              :options="[
                { label: 'All Capabilities', value: 'all' },
                { label: 'Text & Analysis', value: 'text' },
                { label: 'Code', value: 'code' },
                { label: 'Search & Research', value: 'search' },
                { label: 'Images', value: 'image' },
                { label: 'Multi-modal', value: 'multimodal' }
              ]"
            />
          </div>
          
          <Row :gutter="[16, 16]" wrap>
            <Col 
              v-for="capability in filteredCapabilities"
              :key="capability.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
            >
              <Card
                :class="['capability-card', { 
                  active: selectedCapability.id === capability.id,
                  thinking: capability.requiresThinking,
                  streaming: capability.supportsStreaming
                }]"
                hoverable
                :tabindex="0"
                role="button"
                :aria-pressed="selectedCapability.id === capability.id"
                @click="selectedCapability = capability"
                @keydown.enter="selectedCapability = capability"
              >
                <div class="capability-content">
                  <div class="capability-header">
                    <component 
                      :is="getCapabilityIcon(capability.icon)" 
                      :size="24" 
                      :color="selectedCapability.id === capability.id ? '#722ed1' : '#666'"
                    />
                    <div class="capability-badges">
                      <Tag v-if="capability.requiresThinking" color="purple" size="small">
                        <Brain :size="12" /> Thinking
                      </Tag>
                      <Tag v-if="capability.supportsStreaming" color="blue" size="small">
                        <Zap :size="12" /> Stream
                      </Tag>
                      <Tag v-if="capability.supportsTools" color="green" size="small">
                        <Target :size="12" /> Tools
                      </Tag>
                    </div>
                  </div>
                  <Typography.Title :level="5" style="margin: 8px 0 4px 0">
                    {{ capability.name }}
                  </Typography.Title>
                  <Typography.Paragraph type="secondary" style="margin: 0; font-size: 12px">
                    {{ capability.description }}
                  </Typography.Paragraph>
                </div>
              </Card>
            </Col>
          </Row>
        </Card>
        
        <!-- Main interaction area -->
        <Card class="interaction-area" :bordered="false">
          <div class="selected-capability-info">
            <div class="capability-title">
              <component :is="getCapabilityIcon(selectedCapability.icon)" :size="20" color="#722ed1" />
              <span>{{ selectedCapability.name }}</span>
              <Typography.Text type="secondary" style="margin-left: 8px">
                {{ selectedCapability.description }}
              </Typography.Text>
            </div>
            
            <div class="capability-features">
              <Tag color="geekblue" v-if="thinkingLevel === 'high'">
                Deep Thinking Enabled
              </Tag>
              <Tag color="green">Provider: {{ currentProvider.toUpperCase() }}</Tag>
              <Tag color="orange">Response Time: {{ responseTime }}ms</Tag>
            </div>
          </div>
          
          <!-- Input area with accessibility -->
          <div class="input-container">
            <!-- File upload area -->
            <div 
              v-if="uploadedFiles.length > 0"
              class="file-upload-area"
              :class="{ 'drag-over': dragOver }"
            >
              <Typography.Title :level="5">Attached Files</Typography.Title>
              <div class="file-list">
                <div v-for="(file, index) in uploadedFiles" :key="index" class="file-item">
                  <component :is="FileText" :size="16" />
                  <span class="file-name">{{ file.name }}</span>
                  <span class="file-size">{{ (file.size / 1024).toFixed(1) }} KB</span>
                  <Button 
                    size="small" 
                    type="link" 
                    @click="removeFile(index)"
                    :aria-label="\`Remove file \${file.name}\`"
                  >
                    Remove
                  </Button>
                </div>
              </div>
            </div>
            
            <!-- Main input with accessibility -->
            <div class="input-wrapper">
              <Input.TextArea
                id="main-ai-input"
                v-model:value="inputValue"
                :rows="4"
                :placeholder="\`Ask Sheikh to help with \${selectedCapability.name.toLowerCase()}...\`"
                :disabled="loading"
                @focus="inputFocused = true"
                @blur="inputFocused = false"
                @keydown="handleKeyDown"
                :class="[
                  'main-input',
                  { 'focused': inputFocused, 'error': inputError }
                ]"
                aria-describedby="input-help input-error"
              />
              <div class="input-footer">
                <div class="input-help" id="input-help">
                  Press <kbd>Enter</kbd> to send, <kbd>Shift+Enter</kbd> for new line
                </div>
                <div class="input-actions">
                  <Upload
                    :before-upload="() => false"
                    :show-upload-list="false"
                    @change="(info) => handleFileUpload(info.fileList.map(f => f.originFileObj).filter(Boolean))"
                    multiple
                    accept=".pdf,.doc,.docx,.txt,.csv,.json,.png,.jpg,.jpeg"
                  >
                    <Button size="small" type="default" :disabled="loading">
                      <template #icon><FileText /></template>
                      Attach File
                    </Button>
                  </Upload>
                  
                  <Button 
                    size="small" 
                    type="primary"
                    :loading="loading"
                    :disabled="!canSubmit"
                    @click="submitPrompt"
                    :aria-describedby="inputError ? 'input-error' : undefined"
                  >
                    <template #icon>
                      <Loader v-if="loading" :size="16" />
                      <Send v-else />
                    </template>
                    {{ loading ? (isThinking ? 'Thinking...' : 'Generating...') : 'Send' }}
                  </Button>
                </div>
              </div>
              
              <div v-if="inputError" id="input-error" class="input-error" role="alert">
                {{ inputError }}
              </div>
            </div>
          </div>
          
          <!-- Advanced settings drawer -->
          <Drawer
            v-model:open="showAdvanced"
            title="Advanced Settings"
            placement="right"
            width="400"
          >
            <div class="advanced-settings">
              <div class="setting-group">
                <Typography.Title :level="5">Thinking Configuration</Typography.Title>
                <Typography.Paragraph type="secondary">
                  Configure the depth of AI reasoning for complex tasks
                </Typography.Paragraph>
                <Select
                  v-model:value="thinkingLevel"
                  style="width: 100%"
                  :options="[
                    { label: 'Fast - Quick responses, basic reasoning', value: 'low' },
                    { label: 'Balanced - Good balance of speed and depth', value: 'medium' },
                    { label: 'Deep - Maximum reasoning depth for complex problems', value: 'high' }
                  ]"
                />
              </div>
              
              <Divider />
              
              <div class="setting-group">
                <Typography.Title :level="5">Provider Settings</Typography.Title>
                <div class="provider-info">
                  <Tag color="purple">Google Gemini 3 Pro Preview</Tag>
                  <Typography.Paragraph type="secondary" style="margin-top: 8px">
                    Using Google's latest AI model with advanced reasoning capabilities
                  </Typography.Paragraph>
                </div>
              </div>
              
              <Divider />
              
              <div class="setting-group">
                <Typography.Title :level="5">Performance</Typography.Title>
                <div class="performance-metrics">
                  <div class="metric">
                    <span>Average Response Time</span>
                    <span>{{ responseTime }}ms</span>
                  </div>
                  <div class="metric">
                    <span>Model</span>
                    <span>gemini-3-pro-preview</span>
                  </div>
                  <div class="metric">
                    <span>Capabilities</span>
                    <span>{{ selectedCapability.name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </Drawer>
        </Card>
        
        <!-- Response display -->
        <div v-if="streamingResponse || currentResponse" class="response-area">
          <Card class="response-card" :bordered="false">
            <div class="response-header">
              <div class="response-info">
                <Avatar :size="32" style="background: #722ed1">
                  <template #icon><Brain /></template>
                </Avatar>
                <div class="response-meta">
                  <Typography.Title :level="5" style="margin: 0">Sheikh AI</Typography.Title>
                  <Typography.Text type="secondary" style="font-size: 12px">
                    {{ new Date().toLocaleTimeString() }} • {{ responseTime }}ms
                  </Typography.Text>
                </div>
              </div>
              
              <div class="response-actions">
                <Tooltip title="Copy response">
                  <Button size="small" @click="copyToClipboard(streamingResponse || currentResponse?.text)">
                    <template #icon><Copy /></template>
                  </Button>
                </Tooltip>
                <Tooltip title="Share">
                  <Button size="small">
                    <template #icon><Share2 /></template>
                  </Button>
                </Tooltip>
              </div>
            </div>
            
            <div class="response-content">
              <div class="streaming-text" v-if="loading">
                <div class="typing-indicator">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </div>
                {{ streamingResponse }}
              </div>
              <div v-else class="final-response">
                <div v-html="streamingResponse || currentResponse?.text" class="response-text"></div>
                
                <!-- Reasoning display -->
                <div v-if="currentResponse?.reasoning" class="reasoning-section">
                  <Alert
                    message="AI Reasoning Process"
                    type="info"
                    show-icon
                    style="margin-top: 16px"
                  >
                    <template #description>
                      <Typography.Paragraph>
                        {{ currentResponse.reasoning }}
                      </Typography.Paragraph>
                    </template>
                  </Alert>
                </div>
                
                <!-- Metadata display -->
                <div class="response-metadata">
                  <Divider />
                  <Row :gutter="16">
                    <Col :span="8">
                      <div class="metadata-item">
                        <span class="label">Provider</span>
                        <span class="value">{{ responseMetadata?.provider || 'google' }}</span>
                      </div>
                    </Col>
                    <Col :span="8">
                      <div class="metadata-item">
                        <span class="label">Thinking</span>
                        <span class="value">{{ responseMetadata?.thinking || 'disabled' }}</span>
                      </div>
                    </Col>
                    <Col :span="8">
                      <div class="metadata-item">
                        <span class="label">Capability</span>
                        <span class="value">{{ selectedCapability.name }}</span>
                      </div>
                    </Col>
                  </Row>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  `
})

export default EnhancedAIInterface