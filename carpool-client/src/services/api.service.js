import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

// Create axios instance with default config
const axiosInstance = axios.create({
    baseURL: API_URL
})

// Add request interceptor to add auth header
axiosInstance.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export const apiService = {
    // Authentication
    register: async (userData) => {
        return await axiosInstance.post('/users/', userData)
    },

    login: async (credentials) => {
        const response = await axiosInstance.post('/users/login', credentials)
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token)
            localStorage.setItem('userId', response.data.user_id.toString())
        }
        return response.data
    },

    // Users
    getCurrentUser: async () => {
        return await axiosInstance.get('/users/me/')
    },

    updateUser: async (userData) => {
        return await axiosInstance.put('/users/me/', userData)
    },

    // Cars
    addUserCar: async (carData) => {
        return await axiosInstance.post('/users/me/cars', carData)
    },

    updateUserAddress: async (userId, data) => {
        return await axiosInstance.post(`/favourite-places/user/${userId}`, {
            name: 'Home',
            address: data.address,
            latitude: data.latitude || 0,
            longitude: data.longitude || 0
        })
    }
} 