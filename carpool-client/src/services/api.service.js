import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

export const apiService = {
    // Аутентификация
    register: async (userData) => {
        return await axios.post(`${API_URL}/users/`, userData)
    },

    login: async (credentials) => {
        return await axios.post(`${API_URL}/auth/login/`, credentials)
    },

    // Пользователи
    getCurrentUser: async () => {
        return await axios.get(`${API_URL}/users/me/`)
    },

    updateUser: async (userData) => {
        return await axios.put(`${API_URL}/users/me/`, userData)
    },

    // Здесь можно добавить другие методы для работы с API
} 