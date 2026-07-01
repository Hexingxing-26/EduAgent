import { defineStore } from 'pinia'
import { fetchSettings, saveSettings } from '@/api/api'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    llmApiKey: '',
    llmBaseUrl: '',
    llmModel: '',
    loading: false,
    saving: false,
  }),

  actions: {
    async fetchSettings() {
      this.loading = true
      try {
        const res = await fetchSettings()
        if (res.data && res.data.llm_api_key !== undefined) {
          this.llmApiKey = res.data.llm_api_key
          this.llmBaseUrl = res.data.llm_base_url
          this.llmModel = res.data.llm_model
        }
      } finally {
        this.loading = false
      }
    },

    async saveSettings(data) {
      this.saving = true
      try {
        await saveSettings(data)
        this.llmApiKey = data.llm_api_key
        this.llmBaseUrl = data.llm_base_url
        this.llmModel = data.llm_model
        return true
      } finally {
        this.saving = false
      }
    },
  },
})
