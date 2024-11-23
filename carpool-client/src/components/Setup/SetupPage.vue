<template>
  <div class="setup-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">←</button>
      <h1>Setup Profile</h1>
    </div>

    <div class="car-form">
      <h2>Please add a car</h2>
      <p class="subtitle">provided you're planning to be a driver</p>

      <form @submit.prevent="handleSubmit">
        <input
          v-model="carData.make"
          type="text"
          placeholder="Car make (e.g., Toyota)"
          class="form-input"
          required
        />
        
        <input
          v-model="carData.model"
          type="text"
          placeholder="Car model (e.g., Camry)"
          class="form-input"
          required
        />
        
        <input
          v-model="carData.year"
          type="number"
          placeholder="Year"
          class="form-input"
          required
          min="1900"
          :max="new Date().getFullYear()"
        />

        <input
          v-model="carData.plate_number"
          type="text"
          placeholder="Plate number"
          class="form-input"
          required
        />

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="next-button">Next</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '@/services/api.service'

export default {
  name: 'SetupPage',
  setup() {
    const router = useRouter()
    const error = ref('')
    const carData = ref({
      make: '',
      model: '',
      year: '',
      plate_number: ''
    })

    onMounted(() => {
      // Check if user is authenticated
      const token = localStorage.getItem('token')
      if (!token) {
        router.push('/login')
      }
    })

    const handleSubmit = async () => {
      try {
        // Validate year is a number
        carData.value.year = parseInt(carData.value.year)
        
        // Send request to backend
        await apiService.addUserCar(carData.value)
        
        // Redirect to home or next setup page
        router.push('/home')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to add car'
        if (err.response?.status === 401) {
          // If unauthorized, redirect to login
          router.push('/login')
        }
      }
    }

    return {
      carData,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.setup-page {
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.back-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.car-form {
  max-width: 500px;
  margin: 0 auto;
}

.subtitle {
  color: #666;
  margin-bottom: 30px;
}

.form-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.next-button {
  width: 100%;
  padding: 15px;
  background-color: #dd3333;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.next-button:hover {
  background-color: #cc2222;
}

.error-message {
  color: #dc3545;
  margin-bottom: 15px;
  text-align: center;
}
</style>
