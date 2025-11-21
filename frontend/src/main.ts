import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import './styles/global.css'
import './styles/enhanced-ai.css'

import App from './App.vue'
import router from './router'

// SHEIKH AI SYSTEM - Enhanced with Modern AI SDK Integration
// Features:
// - AG-UI Protocol for bi-directional agent-user communication
// - CopilotKit for enhanced AI interaction experience  
// - Google Generative AI with Gemini 3 Pro Preview
// - AI SDK Providers for multiple AI backends
// - Accessible, fast, delightful UI following WCAG guidelines

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)

app.mount('#app')