<script setup>
import { ref } from 'vue'

const theme = ref('light')

function onClick() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

// Form fields and validation rules
const email = ref('')
const emailRules = [
  (value) => (value?.length >= 3 ? true : 'Email must be at least 3 characters.'),
  (value) => (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? true : 'Invalid email format.'),
]

const password = ref('')
const passwordRules = [
  (value) => (value?.length >= 3 ? true : 'Password must be at least 3 characters.'),
]

// Form submission handler
function onSubmit() {
  console.log('Form Submitted:', { email: email.value, password: password.value })
}
</script>

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
          <v-card class="mx-auto" prepend-icon="mdi-account" elevation="10" width="500">
            <!-- Title and Subtitle -->
            <template v-slot:title>
              <span class="font-weight-black">RealChat</span>
            </template>
            <template v-slot:subtitle>
              <span class="text-muted">Log in </span>
            </template>

            <v-card-text class="bg-surface-light pt-4">
              <v-sheet>
                <v-form fast-fail @submit.prevent="onSubmit">
                  <v-text-field v-model="email" label="Email" :rules="emailRules"></v-text-field>

                  <v-text-field
                    v-model="password"
                    label="Password"
                    type="password"
                    :rules="passwordRules"
                  ></v-text-field>

                  <v-btn class="mt-2" type="submit" block>Log In</v-btn>
                </v-form>
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-container>
      </v-main>

      <v-footer border app>2024 - RealChat</v-footer>
    </v-app>
  </v-responsive>
</template>
