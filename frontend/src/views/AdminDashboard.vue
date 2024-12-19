<template>
  <v-container class="bg-surface-variant mt-5">
    <div>
      <div class="mb-5">
        <v-data-table :headers="userHeaders" :items="users" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Users</v-toolbar-title>
            </v-toolbar>
          </template>
        </v-data-table>
      </div>

      <div>
        <v-data-table :headers="messageHeaders" :items="messages" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Messages</v-toolbar-title>
            </v-toolbar>
          </template>
        </v-data-table>
      </div>
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const messages = ref([])

const userHeaders = [
  { text: 'ID', value: 'id' },
  { text: 'Username', value: 'username' },
  { text: 'Email', value: 'email' },
]

const messageHeaders = [
  { text: 'ID', value: 'id' },
  { text: 'Sender', value: 'sender.username' },
  { text: 'Receiver', value: 'receiver.username' },
  { text: 'Content', value: 'content' },
  { text: 'Timestamp', value: 'timestamp' },
]

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/accounts/users/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    users.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const fetchMessages = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/accounts/all-messages/', {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    messages.value = response.data
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchUsers()
  fetchMessages()
})
</script>

<style scoped></style>
