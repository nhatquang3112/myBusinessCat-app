<template>

  <div class="gameplay">
  <h1>This is GamePlay</h1>
  <h2 v-if="isHappening">Let's get down to business!</h2>
  <h2 v-else>Waiting for other players...</h2>
  <div v-if="inLobby">
  <input type="text" placeholder = "What is your cat name?" v-model="playerID"></input>
  <button v-on:click="createNewPlayer()">Go!</button>
  </div>

  <div class = "vertical-menu" v-else>
    <a v-for="player in playerList">
      <img src="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/0b/0bc3ded6d1c690449dd74dee852f6053517749cb_full.jpg" alt = "Ava">
      <li>Player: {{ player.username }}</li>
      <li>Score: {{ player.highscore }}</li>
      <li>Height: {{ player.strength }}</li>
    </a>
  </div>






  <router-link to = "/gameend">End the game?</router-link>
  </div>
</template>

<script>
const axios = require('axios');
import * as firebase from "firebase";
var config = {
  apiKey: "AIzaSyBEHPA-ti-TC5m5L5aZD4ZwwOZaNtZo-lk",
  authDomain: "cat-app-a1391.firebaseapp.com",
  databaseURL: "https://cat-app-a1391.firebaseio.com",
  projectId: "cat-app-a1391",
  storageBucket: "",
  messagingSenderId: "1067089159725"
};
firebase.initializeApp(config);
const database = firebase.database();

//helper functions
function writeUserData(userId, ingame, score, height) {
  firebase.database().ref('users/' + userId).set({
    username: userId,
    ingameStatus: ingame,
    highscore: score,
    strength: height,
  });
}

//real time update
var userRef = database.ref().child('users');
userRef.on('value', (snapshot) => {
    this.playerList = Object.values(snapshot.val());
    console.log(Object.values(snapshot.val()));
});

export default {
  name: 'GameStart',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      playerList: [],
      isHappening: true,
      playerID:'',
      inLobby: true,
      height: 0,

    }
  },
  methods: {
     createNewPlayer: function() {
         writeUserData(this.playerID, 'true', '0', this.height);
         this.inLobby = false;
     },




  },

  mounted: function() {
     database.ref().child('users').on('value', (snapshot) => {
     this.playerList = Object.values(snapshot.val());
     this.height = Math.floor(Math.random() * (5 - 1 + 1)) + 1;
  });


  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.vertical-menu {
    width: 250px; /* Set a width if you like */
}

.vertical-menu a {
    background-color: #eee; /* Grey background color */
    color: black; /* Black text color */
    display: block; /* Make the links appear below each other */
    padding: 12px; /* Add some padding */
    text-decoration: none; /* Remove underline from links */
}

.vertical-menu a:hover {
    background-color: #ccc; /* Dark grey background on mouse-over */
}

.vertical-menu a.active {
    background-color: #4CAF50; /* Add a green color to the "active/current" link */
    color: white;
}

img {
    width: 50px; /* you can use % */
    height: auto;
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
