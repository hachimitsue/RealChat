<template>
  <div>
    <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
      <div class="text-subtitle-1 text-medium-emphasis">Account</div>

      <v-text-field
        density="compact"
        placeholder="Email address"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
        v-model="email"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis">Contact</div>

      <v-text-field
        density="compact"
        placeholder="639512200000"
        prepend-inner-icon="mdi-phone-outline"
        variant="outlined"
        v-model="phone_number"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
        Password
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

      <v-btn class="mb-8" color="blue" size="large" variant="tonal" block @click="register">
        Register
      </v-btn>

      <v-card-text class="text-center">
        <RouterLink class="text-blue text-decoration-none" to="/">
          Log in now <v-icon icon="mdi-chevron-right"></v-icon>
        </RouterLink>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const password = ref('')
const phone_number = ref('')

const register = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('email', email.value)
    formData.append('password', password.value)
    formData.append('phone_number', phone_number.value)

    const response = await axios.post('http://127.0.0.1:8000/sms/register/', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    console.log(response.data)
  } catch (error) {
    console.error(error)
  }
}
</script>
<style></style>
