import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import SetupPage from '@/components/Setup/SetupPage.vue'
import SetupAddress from '@/components/Setup/SetupAddress.vue'
import SetupRole from '@/components/Setup/SetupRole.vue'
import CreateRide from '@/components/Ride/CreateRide.vue'

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
      path: '/setup/address',
      name: 'setup-address',
      component: SetupAddress,
      meta: { requiresAuth: true }
    },
    {
      path: '/setup/role',
      name: 'setup-role',
      component: SetupRole,
      meta: { requiresAuth: true }
    },
    {
      path: '/create-ride',
      name: 'create-ride',
      component: CreateRide,
      meta: { requiresAuth: true }
    }
  ]
})

export default router
