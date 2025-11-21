<template>
  <div class="markdown-renderer" v-html="renderedHtml"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

// Configure marked
marked.setOptions({
  highlight: function(code: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (error) {
        console.error('Highlight error:', error)
      }
    }
    return hljs.highlightAuto(code).value
  },
  langPrefix: 'hljs language-',
  breaks: true,
  gfm: true
})

interface Props {
  content: string
}

const props = defineProps<Props>()

const renderedHtml = computed(() => {
  if (!props.content) return ''
  
  try {
    return marked(props.content)
  } catch (error) {
    console.error('Markdown rendering error:', error)
    return `<pre>${props.content}</pre>`
  }
})
</script>

<style scoped>
.markdown-renderer {
  line-height: 1.6;
}

.markdown-renderer :deep(pre) {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0;
}

.markdown-renderer :deep(code) {
  background: #f6f8fa;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 85%;
  font-family: 'Courier New', Courier, monospace;
}

.markdown-renderer :deep(pre code) {
  background: none;
  padding: 0;
  border-radius: 0;
  font-size: inherit;
}

.markdown-renderer :deep(p) {
  margin: 16px 0;
}

.markdown-renderer :deep(h1),
.markdown-renderer :deep(h2),
.markdown-renderer :deep(h3),
.markdown-renderer :deep(h4),
.markdown-renderer :deep(h5),
.markdown-renderer :deep(h6) {
  margin: 24px 0 16px 0;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-renderer :deep(h1) {
  font-size: 2em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-renderer :deep(h2) {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-renderer :deep(h3) {
  font-size: 1.25em;
}

.markdown-renderer :deep(ul),
.markdown-renderer :deep(ol) {
  margin: 16px 0;
  padding-left: 2em;
}

.markdown-renderer :deep(li) {
  margin: 4px 0;
}

.markdown-renderer :deep(blockquote) {
  margin: 16px 0;
  padding: 0 1em;
  color: #6a737d;
  border-left: 4px solid #dfe2e5;
}

.markdown-renderer :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
}

.markdown-renderer :deep(table),
.markdown-renderer :deep(th),
.markdown-renderer :deep(td) {
  border: 1px solid #dfe2e5;
}

.markdown-renderer :deep(th),
.markdown-renderer :deep(td) {
  padding: 6px 13px;
}

.markdown-renderer :deep(th) {
  background: #f6f8fa;
  font-weight: 600;
}

.markdown-renderer :deep(img) {
  max-width: 100%;
  height: auto;
  margin: 16px 0;
  border-radius: 6px;
}

.markdown-renderer :deep(a) {
  color: #0366d6;
  text-decoration: none;
}

.markdown-renderer :deep(a:hover) {
  text-decoration: underline;
}

.markdown-renderer :deep(hr) {
  border: none;
  border-top: 1px solid #dfe2e5;
  margin: 24px 0;
}

/* Dark mode styles */
:global(.ant-theme-dark) .markdown-renderer :deep(pre) {
  background: #1e1e1e;
  border-color: #3e3e3e;
}

:global(.ant-theme-dark) .markdown-renderer :deep(code) {
  background: #1e1e1e;
  color: #d4d4d4;
}

:global(.ant-theme-dark) .markdown-renderer :deep(blockquote) {
  color: #808080;
  border-left-color: #3e3e3e;
}

:global(.ant-theme-dark) .markdown-renderer :deep(table),
:global(.ant-theme-dark) .markdown-renderer :deep(th),
:global(.ant-theme-dark) .markdown-renderer :deep(td) {
  border-color: #3e3e3e;
}

:global(.ant-theme-dark) .markdown-renderer :deep(th) {
  background: #2d2d30;
}

/* Code highlighting theme for dark mode */
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs) {
  background: #1e1e1e;
  color: #d4d4d4;
}

:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-keyword),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-selector-tag),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-literal),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-title),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-section),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-doctag),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-name) {
  color: #569cd6;
}

:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-attribute),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-attr),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-bullet),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-code),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-deletion),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-meta),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-name),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-selector-tag),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-subst),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-symbol),
:global(.ant-theme-dark) .markdown-renderer :deep(.hljs-variable) {
  color: #9cdcfe;
}
</style>