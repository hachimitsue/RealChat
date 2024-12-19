<template>
  <div>
    <v-card class="mx-auto pa-12 pb-8 mt-15" elevation="8" max-width="448" rounded="lg">
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>

      <v-text-field
        density="compact"
        placeholder="Email address"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
        v-model="username"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Password

        <a
          class="text-caption text-decoration-none text-blue"
          href="#"
          rel="noopener noreferrer"
          target="_blank"
        >
          Forgot login password?</a
        >
      </div>

      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
        v-model="password"
      ></v-text-field>

      <v-card class="mb-12" color="surface-variant" variant="tonal">
        <v-card-text class="text-medium-emphasis text-caption">
          Warning: After 3 consecutive failed login attempts, you account will be temporarily locked
          for three hours. If you must login now, you can also click "Forgot login password?" below
          to reset the login password.
        </v-card-text>
      </v-card>

      <v-btn class="mb-8" color="blue" size="large" variant="tonal" block @click="login">
        Log In
      </v-btn>

      <v-card-text class="text-center">
        <RouterLink class="text-blue text-decoration-none" to="/register">
          Register now <v-icon icon="mdi-chevron-right"></v-icon>
        </RouterLink>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const visible = ref(false)
const router = useRouter()

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/accounts/login/', {
      username: username.value,
      password: password.value,
    })
    const token = response.data.token
    localStorage.setItem('token', token)
    const userResponse = await axios.get('http://127.0.0.1:8000/accounts/protected/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    if (userResponse.data.is_admin) {
      router.push('/dashboard')
    } else {
      alert('Only admin can access the dashboard')
    }
  } catch (error) {
    console.error(error)
    alert('Login failed')
  }
}
</script>

<style>
/* html {
  overflow-y: hidden !important;
} */
</style>
