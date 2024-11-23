import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

export const authService = {
    async login(email, password) {
        const response = await axios.post(`${API_URL}/users/login`, {
            email: email,
            password: password
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token)
        }
        return response.data
    },

    async register(userData) {
        const response = await axios.post(`${API_URL}/users/`, userData, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        return response.data
    },

    async getCurrentUser() {
        const token = localStorage.getItem('token')
        if (!token) return null

        const response = await axios.get(`${API_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        return response.data
    },

    async updateProfile(userData) {
        const token = localStorage.getItem('token')
        const response = await axios.put(`${API_URL}/users/me`, userData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        return response.data
    },

    logout() {
        localStorage.removeItem('token')
    }
} 