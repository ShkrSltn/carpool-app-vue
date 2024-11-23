import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import RideMap from '../components/Map/RideMap.vue'
import GoogleMap from '../components/Map/GoogleMap.vue'
import SetupPage from '@/components/Setup/SetupPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/setup',
      name: 'setup',
      component: SetupPage,
      meta: { requiresAuth: true }
    },
    {
      path: '/map',
      name: 'map',
      component: RideMap
    },
    {
      path: '/google-map',
      name: 'google-map',
      component: GoogleMap
    }
  ]
})

export default router
