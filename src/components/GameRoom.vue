<template>
  <div class="gamestart">
    <h1>This is Game Room</h1>
    <button @click="toGameEnd">Game End</button>
    <button @click="writeData">Write Test</button>
    <i class="fas fa-home"></i>

  </div>
</template>

<script>
//import
import firebase from '@/config/firebase'
//Constants
const database = firebase.firestore(); //store data in firestore

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
    async writeData () {
      var data = {
        content: 'hello world'
      }
      var usersRef = database.collection('users');
      try {
        await usersRef.add(data);
        console.log('send data done')
      } catch (err) {
        console.log('Error sending data: ', err);
      }
    }
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
