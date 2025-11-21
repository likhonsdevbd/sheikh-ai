import { defineComponent } from 'vue'
import { Card, Button, Tabs, Empty } from 'ant-design-vue'
import { CopyOutlined, PlayCircleOutlined, DownloadOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'

export const CodePreview = defineComponent({
  name: 'CodePreview',
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const copyCode = () => {
      navigator.clipboard.writeText(props.data.code).then(() => {
        message.success('Code copied to clipboard')
      })
    }

    const runCode = () => {
      message.info('Running code...')
      // Implementation would run the code
    }

    const downloadCode = () => {
      message.info('Downloading code...')
      // Implementation would download the code file
    }

    return {
      copyCode,
      runCode,
      downloadCode
    }
  },
  template: `
    <div class="code-preview">
      <div class="code-header">
        <div class="language-info">
          <span class="language-badge">{{ data.language || 'javascript' }}</span>
          <span class="lines-count">{{ (data.code || '').split('\\n').length }} lines</span>
        </div>
        <div class="code-actions">
          <a-button size="small" @click="copyCode">
            <template #icon><CopyOutlined /></template>
            Copy
          </a-button>
          <a-button size="small" @click="runCode" type="primary">
            <template #icon><PlayCircleOutlined /></template>
            Run
          </a-button>
          <a-button size="small" @click="downloadCode">
            <template #icon><DownloadOutlined /></template>
            Download
          </a-button>
        </div>
      </div>
      
      <div class="code-content" v-if="data.code">
        <pre><code class="language-{{ data.language || 'javascript' }}">{{ data.code }}</code></pre>
      </div>
      <a-empty v-else description="No code to display" />
      
      <div class="code-footer" v-if="data.description">
        <p>{{ data.description }}</p>
      </div>
    </div>
  `
})

export default CodePreview