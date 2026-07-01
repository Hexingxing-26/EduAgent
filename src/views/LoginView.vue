<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>智学系统</h2>
          <p>基于大模型的个性化学习平台</p>
        </div>
      </template>

      <el-form
        v-if="!isRegisterMode"
        :model="loginForm"
        :rules="rules"
        ref="loginFormRef"
        label-width="80px"
        class="login-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" style="width: 100%" @click="handleLogin" :loading="loading">
            登录
          </el-button>
        </el-form-item>

        <div class="other-options">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-link type="primary" @click="switchToRegister">注册账号</el-link>
        </div>
      </el-form>

      <el-form
        v-else
        :model="registerForm"
        :rules="registerRules"
        ref="registerFormRef"
        label-width="90px"
        class="login-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" clearable />
        </el-form-item>

        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="registerForm.nickname" placeholder="请输入昵称" clearable />
        </el-form-item>

        <el-form-item label="专业" prop="major">
          <el-input v-model="registerForm.major" placeholder="请输入专业" clearable />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" style="width: 100%" @click="handleRegister" :loading="loading">
            注册
          </el-button>
        </el-form-item>

        <div class="other-options">
          <span></span>
          <el-link type="primary" @click="switchToLogin">返回登录</el-link>
        </div>
      </el-form>

      <div v-if="!isRegisterMode" class="demo-login">
        <p>演示账号：</p>
        <el-tag type="success">学生：student / 123456</el-tag>
        <el-tag type="warning">教师：teacher / 123456</el-tag>
        <el-tag type="danger">管理员：admin / 123456</el-tag>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref(null)
const registerFormRef = ref(null)
const loading = ref(false)
const rememberMe = ref(true)
const isRegisterMode = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
})

const registerForm = reactive({
  username: '',
  nickname: '',
  major: '',
  password: '',
  confirmPassword: '',
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
}

const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' },
  ],
  major: [
    { required: true, message: '请输入专业', trigger: 'blur' },
    { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
  confirmPassword: [{ validator: validateConfirmPassword, trigger: 'blur' }],
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true

      try {
        await userStore.login(loginForm)
        userStore.setLearningProfile({
          knowledgeBase: 60,
          cognitiveStyle: '视觉型',
          errorPreferences: ['概念理解', '计算错误'],
          learningGoals: '掌握人工智能基础知识',
          preferredLearningStyle: '案例学习',
          currentProgress: 30,
        })
        ElMessage.success('登录成功！')
      } catch (error) {
        ElMessage.error(error?.message || '登录失败，请检查账号密码或后端接口')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}

const switchToRegister = () => {
  isRegisterMode.value = true
}

const switchToLogin = () => {
  isRegisterMode.value = false
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true

      try {
        await userStore.register({
          username: registerForm.username,
          nickname: registerForm.nickname,
          major: registerForm.major,
          password: registerForm.password,
        })
        ElMessage.success('注册成功，请使用新账号登录')
        switchToLogin()
        loginForm.username = registerForm.username
        loginForm.password = ''
      } catch (error) {
        ElMessage.error(error?.message || '注册失败，请稍后重试')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 450px;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.card-header {
  text-align: center;
  padding: 20px 0;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #1a365d;
  font-size: 2rem;
}

.card-header p {
  margin: 0;
  color: #718096;
  font-size: 0.9rem;
}

.login-form {
  padding: 20px 40px;
}

.other-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding: 0 10px;
}

.demo-login {
  margin-top: 20px;
  padding: 15px;
  background-color: #f0f9ff;
  border-radius: 8px;
  text-align: center;
}

.demo-login p {
  margin: 0 0 10px 0;
  color: #4a5568;
  font-weight: bold;
}

.demo-login .el-tag {
  margin: 5px;
}
</style>
