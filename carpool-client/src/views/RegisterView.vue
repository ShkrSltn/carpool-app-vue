<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usersApi } from '@/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const name = ref('')
const surname = ref('')
const username = ref('')
const error = ref('')

const register = async () => {
  try {
    const response = await usersApi.register({
      email: email.value,
      username: username.value,
      password: password.value,
      name: name.value,
      surname: surname.value,
      car: {}
    })
    
    if (response.data) {
      localStorage.setItem('userId', response.data.user_id)
      router.push('/login')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 
                  (Array.isArray(err.response?.data) ? err.response.data[0]?.msg : 'Ошибка при регистрации')
  }
}
</script>

<template>
  <div class="register-container">
    <h2>Регистрация</h2>
    <form @submit.prevent="register" class="register-form">
      <div class="form-group">
        <label for="email">Email:</label>
        <input 
          id="email"
          type="email" 
          v-model="email" 
          required
          placeholder="Введите email"
        >
      </div>

      <div class="form-group">
        <label for="username">Имя пользователя:</label>
        <input 
          id="username"
          type="text" 
          v-model="username" 
          required
          placeholder="Введите имя пользователя"
        >
      </div>

      <div class="form-group">
        <label for="name">Имя:</label>
        <input 
          id="name"
          type="text" 
          v-model="name" 
          required
          placeholder="Введите имя"
        >
      </div>

      <div class="form-group">
        <label for="surname">Фамилия:</label>
        <input 
          id="surname"
          type="text" 
          v-model="surname" 
          required
          placeholder="Введите фамилию"
        >
      </div>

      <div class="form-group">
        <label for="password">Пароль:</label>
        <input 
          id="password"
          type="password" 
          v-model="password" 
          required
          placeholder="Введите пароль"
        >
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div class="form-actions">
        <button type="submit" class="register-button">Зарегистрироваться</button>
        <router-link to="/login" class="login-link">Уже есть аккаунт? Войти</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.9rem;
  color: #666;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #42b983;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  text-align: center;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.register-button {
  background-color: #42b983;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-button:hover {
  background-color: #3aa876;
}

.login-link {
  text-align: center;
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
}

.login-link:hover {
  color: #42b983;
}
</style> 