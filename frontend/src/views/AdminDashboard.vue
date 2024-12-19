<!-- eslint-disable vue/valid-v-slot -->
<template>
  <v-container class="bg-surface-variant">
    <div>
      <div class="mb-5">
        <v-data-table :headers="userHeaders" :items="users" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Users</v-toolbar-title>
            </v-toolbar>
          </template>
          <template v-slot:header.id="{ column }">
            <v-icon left>mdi-card-account-details</v-icon>
            {{ column.text }}
          </template>
          <template v-slot:header.username="{ column }">
            <v-icon left>mdi-account</v-icon>
            {{ column.text }}
          </template>
          <template v-slot:header.email="{ column }">
            <v-icon left>mdi-email</v-icon>
            {{ column.text }}
          </template>
          <template v-slot:header.actions="{ column }">
            <v-icon left>mdi-tools</v-icon>
            {{ column.text }}
          </template>
          <template v-slot:item.actions="{ item }">
            <v-btn icon small @click="editUser(item)" class="mr-2" color="blue">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon small @click="deleteUser(item.id)" color="error">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
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
          <template v-slot:header.sender_username="{ column }">
            <v-icon left>mdi-account-arrow-right</v-icon>
            {{ column.text }}
          </template>
          <template v-slot:header.receiver_username="{ column }">
            <v-icon left>mdi-account-arrow-left</v-icon>
            {{ column.text }}
          </template>
          <template v-slot:header.content="{ column }">
            <v-icon left>mdi-message-text</v-icon>
            {{ column.text }}
          </template>
          <template v-slot:header.timestamp="{ column }">
            <v-icon left>mdi-calendar-clock</v-icon>
            {{ column.text }}
          </template>
        </v-data-table>
      </div>
    </div>

    <!-- Edit User Dialog -->
    <v-dialog v-model="editDialog" max-width="500px">
      <v-card>
        <v-card-title>Edit User</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field v-model="editedUser.username" label="Username"></v-text-field>
            <v-text-field v-model="editedUser.email" label="Email"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="gray darken-1" text @click="closeEditDialog">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="saveUser">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const messages = ref([])
const editDialog = ref(false)
const editedUser = ref({})

const userHeaders = [
  { text: 'ID', value: 'id' },
  { text: 'Username', value: 'username' },
  { text: 'Email', value: 'email' },
  { text: 'Actions', value: 'actions', sortable: false },
]

const messageHeaders = [
  { text: 'Sender', value: 'sender_username' },
  { text: 'Receiver', value: 'receiver_username' },
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

const editUser = (user) => {
  editedUser.value = { ...user }
  editDialog.value = true
}

const deleteUser = async (userId) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/accounts/users/${userId}/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    fetchUsers()
  } catch (error) {
    console.error(error)
  }
}

const closeEditDialog = () => {
  editDialog.value = false
}

const saveUser = async () => {
  try {
    const token = localStorage.getItem('token')
    const data = {
      username: editedUser.value.username,
      email: editedUser.value.email,
    }
    await axios.put(`http://127.0.0.1:8000/accounts/users/${editedUser.value.id}/`, data, {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    fetchUsers()
    closeEditDialog()
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
