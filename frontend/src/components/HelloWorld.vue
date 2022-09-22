<script setup lang="ts">
import { reactive, ref } from 'vue'

interface State {
  n1: number
}

const count = ref(0)
const client_id = Date.now()
const state = reactive<State>({
  n1: 0
})

connect()

function connect() {
  var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`)
  ws.onmessage = function (event) {
    state.n1 = event.data as number
    showNotification()
  }

  ws.onclose = function(e) {
    console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    setTimeout(function() {
      connect();
    }, 5000);
  };

  ws.onerror = function(err) {
    console.error('Socket encountered error: ', err, 'Closing socket');
    ws.close();
  };

  const showNotification = () => {
    console.log("You have new notifications")
  }
}
</script>

<template>
  <h1>You have {{state.n1}} notifications</h1>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
