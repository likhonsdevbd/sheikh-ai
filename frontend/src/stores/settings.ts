import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export interface Settings {
  openaiApiKey: string
  openaiModel: string
  darkMode: boolean
  theme: 'light' | 'dark' | 'auto'
  fontSize: 'small' | 'medium' | 'large'
  autoSave: boolean
  maxMessages: number
  timeoutMinutes: number
  logLevel: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'
  corsOrigins: string[]
}

const defaultSettings: Settings = {
  openaiApiKey: '',
  openaiModel: 'gpt-4',
  darkMode: false,
  theme: 'light',
  fontSize: 'medium',
  autoSave: true,
  maxMessages: 1000,
  timeoutMinutes: 60,
  logLevel: 'INFO',
  corsOrigins: ['*']
}

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<Settings>({ ...defaultSettings })

  function loadSettings() {
    try {
      const stored = localStorage.getItem('sheikh-settings')
      if (stored) {
        const parsed = JSON.parse(stored)
        Object.assign(settings.value, { ...defaultSettings, ...parsed })
      }
    } catch (error) {
      console.error('Error loading settings:', error)
    }
  }

  function saveSettings() {
    try {
      localStorage.setItem('sheikh-settings', JSON.stringify(settings.value))
    } catch (error) {
      console.error('Error saving settings:', error)
    }
  }

  function resetSettings() {
    settings.value = { ...defaultSettings }
    saveSettings()
  }

  function updateSetting(key: keyof Settings, value: any) {
    (settings.value as any)[key] = value
    saveSettings()
  }

  function updateSettings(updates: Partial<Settings>) {
    Object.assign(settings.value, updates)
    saveSettings()
  }

  // Auto-save when settings change
  watch(settings, saveSettings, { deep: true })

  return {
    // State
    settings,
    
    // Actions
    loadSettings,
    saveSettings,
    resetSettings,
    updateSetting,
    updateSettings
  }
})