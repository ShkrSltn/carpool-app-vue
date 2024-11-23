<template>
    <div class="setup-page">
      <div class="header">
        <button class="back-button" @click="$router.go(-1)">←</button>
        <h1>Setup</h1>
      </div>
  
      <div class="role-selection">
        <div class="success-icon">
          <svg viewBox="0 0 24 24" width="48" height="48">
            <path 
              fill="#4CAF50"
              d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"
            />
          </svg>
        </div>
        
        <h2>You're all set!</h2>
        <p class="subtitle">Select the role</p>
        <p class="hint">You can change it later</p>
  
        <div class="role-buttons">
          <button 
            class="role-button driver"
            :class="{ active: selectedRole === 'driver' }"
            @click="selectRole('driver')"
          >
            Driver
          </button>
          <button 
            class="role-button passenger"
            :class="{ active: selectedRole === 'passenger' }"
            @click="selectRole('passenger')"
          >
            Passenger
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { apiService } from '@/services/api.service'
  
  export default {
    name: 'SetupRole',
    setup() {
      const router = useRouter()
      const selectedRole = ref(null)
      const error = ref('')
  
      const selectRole = async (role) => {
        try {
          selectedRole.value = role
          const userId = localStorage.getItem('userId')
          
          if (!userId) {
            router.push('/login')
            return
          }
  
          await apiService.post(`/api/users/${userId}/role`, { role })
          router.push('/home')
        } catch (err) {
          error.value = err.response?.data?.detail || 'Failed to update role'
          if (err.response?.status === 401) {
            router.push('/login')
          }
        }
      }
  
      return {
        selectedRole,
        selectRole,
        error
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
  
  .role-selection {
    max-width: 500px;
    margin: 0 auto;
    text-align: center;
  }
  
  .success-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 20px;
    background-color: #E8F5E9;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  h2 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  .subtitle {
    font-size: 18px;
    color: #333;
    margin-bottom: 5px;
  }
  
  .hint {
    color: #666;
    font-size: 14px;
    margin-bottom: 30px;
  }
  
  .role-buttons {
    display: flex;
    gap: 15px;
    justify-content: center;
  }
  
  .role-button {
    padding: 12px 30px;
    border-radius: 25px;
    border: 2px solid #ddd;
    background: white;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .role-button:hover {
    border-color: #dd3333;
    color: #dd3333;
  }
  
  .role-button.active {
    background-color: #dd3333;
    border-color: #dd3333;
    color: white;
  }
  
  .error-message {
    color: #dc3545;
    margin-top: 15px;
    text-align: center;
  }
  
  @media screen and (max-width: 768px) {
    .setup-page {
      padding: 15px;
    }
  
    .header h1 {
      font-size: 24px;
    }
  
    .role-selection {
      max-width: 100%;
    }
  
    .success-icon {
      width: 60px;
      height: 60px;
    }
  
    h2 {
      font-size: 20px;
    }
  
    .subtitle {
      font-size: 16px;
    }
  
    .role-button {
      padding: 10px 25px;
      font-size: 14px;
    }
  }
  </style>