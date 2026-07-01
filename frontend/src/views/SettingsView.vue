<template>
  <div class="settings-container">
    <el-card header="AI 服务配置" class="settings-card">
      <el-alert
        title="支持所有 OpenAI 兼容接口，包括 DeepSeek、OpenCode、硅基流动等。"
        type="info"
        :closable="false"
        show-icon
        class="settings-alert"
      />

      <el-form
        :model="settingsForm"
        label-width="100px"
        class="settings-form"
        v-loading="settingsStore.loading || settingsStore.saving"
      >
        <el-form-item label="API 地址">
          <el-input
            v-model="settingsForm.llm_base_url"
            placeholder="https://api.openai.com/v1"
            clearable
          />
        </el-form-item>

        <el-form-item label="API Key">
          <el-input
            v-model="settingsForm.llm_api_key"
            type="password"
            show-password
            placeholder="请输入 API Key"
            clearable
          />
        </el-form-item>

        <el-form-item label="模型名称">
          <el-input
            v-model="settingsForm.llm_model"
            placeholder="gpt-4o"
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="settingsStore.saving" @click="handleSave">
            保存配置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { ElMessage } from 'element-plus'

const settingsStore = useSettingsStore()

const settingsForm = reactive({
  llm_base_url: '',
  llm_api_key: '',
  llm_model: '',
})

const syncFormFromStore = () => {
  settingsForm.llm_base_url = settingsStore.llmBaseUrl || ''
  settingsForm.llm_api_key = settingsStore.llmApiKey || ''
  settingsForm.llm_model = settingsStore.llmModel || ''
}

const handleSave = async () => {
  try {
    const ok = await settingsStore.saveSettings({
      llm_base_url: settingsForm.llm_base_url,
      llm_api_key: settingsForm.llm_api_key,
      llm_model: settingsForm.llm_model,
    })
    if (ok) {
      ElMessage.success('AI 服务配置已保存')
    }
  } catch (err) {
    console.error('保存 AI 服务配置失败：', err)
    ElMessage.error(err?.message || '保存 AI 服务配置失败，请稍后重试')
  }
}

onMounted(async () => {
  try {
    await settingsStore.fetchSettings()
    syncFormFromStore()
  } catch (err) {
    console.warn('拉取 AI 服务配置失败：', err?.message || err)
  }
})
</script>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.settings-card {
  border-radius: 12px;
}

.settings-alert {
  margin-bottom: 20px;
}

.settings-form {
  max-width: 600px;
}
</style>
