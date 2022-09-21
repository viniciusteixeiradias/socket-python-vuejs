<script setup lang="ts">
import { reactive, ref } from 'vue'

defineProps<{ msg: string }>()


interface Notification {
  author: string
  message: string
}

interface State {
  notifications: Notification[]
  messages: string[]
  text: string
}

const count = ref(0)
const client_id = Date.now()
const connection = new WebSocket(`ws://localhost:8000/ws/${client_id}`)
const state = reactive<State>({
  notifications: [],
  messages: [],
  text: ""
})

connection.onmessage = function (event) {
  // const newItem = { ...JSON.parse(event.data) }
  // state.notifications.push(newItem)
  state.messages.push(event.data as string)
  showNotification()
}

const submit = () =>
  connection.send(state.text)
  state.text = ""
    // JSON.stringify({
    //   author: "Vinícius",
    //   message: "As cotações foram atualizadas"
    // })
  
const showNotification = () => {
  console.log("You have new notifications")
}
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <input v-model="state.text" type="text" id="messageText" autocomplete="off"/>
    <button type="button" @click="submit()">Submit</button>
    <ul>
      <li v-for="(message, index) in state.messages" :key="index">
        {{message}}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
