<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authApi } from '@/api';

const router = useRouter();
const email = ref('');
const password = ref('');
const error = ref('');

const login = async () => {
  try {
    const response = await authApi.login({
      email: email.value,
      password: password.value,
    });

    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('userId', response.data.user_id)
      router.push('/setup')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error during login';
  }
};
</script>

<template>
  <div class="page-container">
    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="email">Email:</label>
          <input
            id="email"
            type="email"
            v-model="email"
            required
            placeholder="Enter email"
          />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input
            id="password"
            type="password"
            v-model="password"
            required
            placeholder="Enter password"
          />
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div class="form-actions">
          <button type="submit" class="login-button">Login</button>
          <p class="register-text">
            Don’t have an account?
            <router-link to="/register" class="register-link">Register</router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
body {
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: inherit;
}

.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.login-container {
  flex: 1 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

h2 {
  text-align: center;
  color: black;
  font-weight: bold;
  margin-bottom: -0.5rem;
}

.login-form {
  width: 100%;
  height: inherit;
  display: flex;
  padding: 4rem;
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
  border-color: black;
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

.login-button {
  background-color: #e8423f;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #d6362c;
}

.register-text {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}

.register-link {
  font-weight: bold;
  color: #e8423f;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}
</style>
