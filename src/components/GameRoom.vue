<template>
  <div class="container">

    <div class="userInfo">
      <p>userInfo</p>
    </div>

    <div class="gamePlay">

      <div class="userList">
        <p>userList</p>
      </div>
      <div class="profitList">
        <p>profitList</p>
      </div>
      <div class="proposeList">
        <p>proposeList</p>
      </div>

    </div>

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
      msg: 'Welcome to Your Vue.js App',
      userList: [ //hardcoded for testing
        {name: 'Player 1',stamina: '1',score: '10',},
        {name: 'Player 1',stamina: '1',score: '10',},
        {name: 'Player 1',stamina: '1',score: '10',},
        {name: 'Player 1',stamina: '1',score: '10',},
        {name: 'Player 1',stamina: '1',score: '10',},
      ],
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
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
.userInfo {
  background-color: #4286f4;
  color: #ffffff;
}
.gamePlay {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: 100%;

}
.userList {
  background-color: #e85537;
  color: #ffffff;
}
.profitList {
  background-color: #e8d336;
  color: #ffffff;
}
.proposeList {
  background-color: #94e835;
  color: #ffffff;
}
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
