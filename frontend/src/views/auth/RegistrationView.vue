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
            prepend-icon="mdi-account-plus"
            subtitle="Create a new account"
            width="400"
            elevation="10"
          >
            <template v-slot:title>
              <span class="font-weight-black">Join RealChat</span>
            </template>

            <v-card-text class="bg-surface-light pt-4">
              <v-form @submit.prevent="onSubmit" fast-fail>
                <!-- Name field -->
                <v-text-field
                  v-model="name"
                  label="Name"
                  :rules="nameRules"
                  outlined
                ></v-text-field>

                <!-- Email field -->
                <v-text-field
                  v-model="email"
                  label="Email"
                  :rules="emailRules"
                  outlined
                ></v-text-field>

                <!-- Password field -->
                <v-text-field
                  v-model="password"
                  label="Password"
                  type="password"
                  :rules="passwordRules"
                  outlined
                ></v-text-field>

                <!-- Password Confirmation field -->
                <v-text-field
                  v-model="passwordConfirm"
                  label="Confirm Password"
                  type="password"
                  :rules="[passwordMatch]"
                  outlined
                ></v-text-field>

                <!-- Submit button -->
                <v-btn
                  class="mt-4"
                  type="submit"
                  block
                  :color="theme === 'light' ? 'grey lighten-2' : 'grey darken-2'"
                >
                  Register
                </v-btn>
              </v-form>

              <div class="d-flex justify-center mt-3">
                <!-- Just text with a clickable link to the login page -->
                <span
                  @click="router.push('/')"
                  :style="{ color: theme === 'light' ? '#616161' : '#B0B0B0' }"
                  class="cursor-pointer"
                >
                  Already have an account? Log In
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
const name = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')

const nameRules = [
  (v) => !!v || 'Name is required',
  (v) => v.length >= 3 || 'Name must be at least 3 characters',
]

const emailRules = [
  (v) => !!v || 'Email is required',
  (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Invalid email format',
]

const passwordRules = [
  (v) => !!v || 'Password is required',
  (v) => v.length >= 3 || 'Password must be at least 3 characters',
]

const passwordMatch = (v) => v === password.value || 'Passwords do not match'

function onSubmit() {
  console.log('Register:', { name: name.value, email: email.value, password: password.value })
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
