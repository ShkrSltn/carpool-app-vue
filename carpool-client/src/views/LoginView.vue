<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  try {
    const response = await authApi.login({
      email: email.value,
      password: password.value
    })
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
      router.push('/rides')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка при входе'
  }
}
</script>

<template>
  <div class="login-container">
    <h2>Вход в систему</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label>Email:</label>
        <input type="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label>Пароль:</label>
        <input type="password" v-model="password" required>
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.error {
  color: red;
  margin-top: 10px;
}
</style> 