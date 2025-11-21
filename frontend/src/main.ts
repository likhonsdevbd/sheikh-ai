import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import './styles/global.css'

import App from './App.vue'
import router from './router'

// RICH paradigm - Ant Design's AI interface solution
// This represents the unified approach to AI user experiences

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)

app.mount('#app')