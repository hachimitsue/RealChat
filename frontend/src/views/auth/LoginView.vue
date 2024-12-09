<template>
  <v-responsive class="border rounded">
    <v-app :theme="theme">
      <v-app-bar class="px-3">
        <v-spacer></v-spacer>
        <v-btn
          :prepend-icon="theme === 'light' ? 'mdi-weather-sunny' : 'mdi-weather-night'"
          rounded
          @click="onClick"
        ></v-btn>
      </v-app-bar>

      <v-main>
        <v-container fluid class="d-flex justify-center align-center min-height-100vh">
          <v-card
            class="mx-auto"
            prepend-icon="mdi-account"
            subtitle="Log in to your account"
            width="400"
            elevation="10"
          >
            <template v-slot:title>
              <span class="font-weight-black">Log In to RealChat</span>
            </template>

            <v-card-text class="bg-surface-light pt-4">
              <v-form @submit.prevent="onSubmit" fast-fail>
                <v-text-field
                  v-model="email"
                  label="Email"
                  :rules="emailRules"
                  outlined
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  label="Password"
                  type="password"
                  :rules="passwordRules"
                  outlined
                ></v-text-field>

                <v-btn
                  class="mt-4"
                  type="submit"
                  block
                  :color="theme === 'light' ? 'grey lighten-2' : 'grey darken-2'"
                >
                  Log In
                </v-btn>
              </v-form>

              <div class="d-flex justify-center mt-3">
                <!-- Just text with a clickable link to the registration page -->
                <span
                  @click="router.push('/register')"
                  :style="{ color: theme === 'light' ? '#616161' : '#B0B0B0' }"
                  class="cursor-pointer"
                >
                  Don't have an account? Register
                </span>
              </div>
            </v-card-text>
          </v-card>
        </v-container>
      </v-main>

      <v-footer border app>2024 - RealChat</v-footer>
    </v-app>
  </v-responsive>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const theme = ref('light')
const email = ref('')
const password = ref('')

const emailRules = [
  (v) => !!v || 'Email is required',
  (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Invalid email format',
]

const passwordRules = [
  (v) => !!v || 'Password is required',
  (v) => v.length >= 3 || 'Password must be at least 3 characters',
]

function onSubmit() {
  console.log('Login:', { email: email.value, password: password.value })
}

function onClick() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
