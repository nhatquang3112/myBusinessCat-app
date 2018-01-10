<template>
  <div class="gamestart">
    <h1>This is Game Room</h1>
    <button @click="toGameEnd">Game End</button>

  </div>
</template>

<script>
import firebase from '@/config/firebase'
export default {
  name: 'GameStart',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },

  methods: {
    toGameEnd () {
      this.$router.push({
        path: '/gameEnd',
      })
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
