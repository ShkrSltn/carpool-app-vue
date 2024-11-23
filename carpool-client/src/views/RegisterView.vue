<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authApi } from '@/api';

const router = useRouter();
const email = ref('');
const password = ref('');
const firstName = ref('');
const lastName = ref('');
const username = ref('');
const error = ref('');

const register = async () => {
  try {
    const response = await authApi.register({
    email: email.value,
    username: username.value,
    password: password.value,
    name: firstName.value,   // Map firstName to name
    surname: lastName.value  // Map lastName to surname
  });

    if (response.data) {
      router.push('/login');
    }
  } catch (err) {
    error.value =
      err.response?.data?.detail ||
      (Array.isArray(err.response?.data)
        ? err.response.data[0]?.msg
        : 'Error during registration');
  }
};
</script>

<template>
  <div class="page-container">
    <div class="register-container">
      <h2>Registration</h2>
      <form @submit.prevent="register" class="register-form">
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
          <label for="username">Username:</label>
          <input
            id="username"
            type="text"
            v-model="username"
            required
            placeholder="Enter username"
          />
        </div>

        <div class="form-group">
          <label for="firstName">First Name:</label>
          <input
            id="firstName"
            type="text"
            v-model="firstName"
            required
            placeholder="Enter first name"
          />
        </div>

        <div class="form-group">
          <label for="lastName">Last Name:</label>
          <input
            id="lastName"
            type="text"
            v-model="lastName"
            required
            placeholder="Enter last name"
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

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-actions">
          <button type="submit" class="register-button">Register</button>
        </div>
      </form>
    </div>
    <p class="login-text">
      Already have an account? 
      <router-link to="/login" class="login-link">Login</router-link>
    </p>
  </div>
</template>

<style scoped>
body {
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  min-height: inherit;
}

.page-container {
  display: flex;
  flex-direction: column;
  height: inherit;
}

.register-container {
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

.register-form {
  width: 100%;
  height: inherit;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
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

.register-button {
  background-color: #e8423f;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-button:hover {
  background-color: #d6362c;
}

.login-text {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}

.login-link {
  font-weight: bold;
  color: #e8423f;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}
</style>