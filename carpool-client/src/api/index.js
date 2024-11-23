import axios from "axios";

const API_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for handling auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (credentials) => {
    return await api.post("/users/login", {
      email: credentials.email,
      password: credentials.password
    });
  },
  register: async (userData) => {
    return await api.post("/users", userData);
  },
  logout: () => {
    localStorage.removeItem('token');
  },
  getCurrentUser: () => api.get("/users/me"),
};

export const usersApi = {
  getCurrentUser: () => api.get("/users/me"),
  updateProfile: (userData) => api.put("/users/me", userData)
};

export const ridesApi = {
  getAll: () => api.get("/rides"),
  getById: (id) => api.get(`/rides/${id}`),
  create: (data) => api.post("/rides", data),
  delete: (id) => api.delete(`/rides/${id}`),
};

export default api;