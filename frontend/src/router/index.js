import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import Dashboard from '@/views/Dashboard.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAdmin: true },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAdmin)) {
    const token = localStorage.getItem('token')
    if (!token) {
      next({ name: 'login' })
    } else {
      try {
        const response = await axios.get('http://127.0.0.1:8000/accounts/check-admin/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        })
        if (response.data.is_admin) {
          next()
        } else {
          alert('Only admin can access the dashboard')
          next({ name: 'login' })
        }
      } catch (error) {
        console.error(error)
        next({ name: 'login' })
      }
    }
  } else {
    next()
  }
})

export default router
