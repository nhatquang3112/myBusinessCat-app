<template>

  <div class="gameplay">
  <h1>This is GamePlay</h1>
  <h2 v-if="isHappening">Let's get down to business!</h2>
  <h2 v-else>Waiting for other players...</h2>

  <div v-if="inLobby">
  <input type="text" placeholder = "What is your cat name?" v-model="playerID"></input>
  <button v-on:click="createNewPlayer()">Go!</button>
  </div>
  
  <img v-if="inLobby" src="https://www.iizcat.com/uploads/2017/04/kr490-bc4.jpg" alt = "Title">


  <div class = "vertical-menu" v-else>
    <a v-for="player in playerList">
      <img src="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/0b/0bc3ded6d1c690449dd74dee852f6053517749cb_full.jpg" alt = "Ava">
      <li>Player: {{ player.username }}</li>
      <li>Score: {{ player.highscore }}</li>
      <li>Stamina: {{ player.strength }}</li>
    </a>
  </div>

  <div class = "vertical-profit" v-if="inLobby === false">
     <a v-for="profit in profitList" v-on:click="startPropose()">
        <img src="http://chefspalate.com.au/wp-content/uploads/2016/05/6.png" alt = "Ava">
        <li>Task {{ profit.Order }}</li>
        <li>Profit: {{ profit.value }}</li>
        <li>Stamina: {{ profit.cost }}</li>
    </a>
  </div>
  <div v-if="isProposing">
     <input type="text" placeholder = "Which task?" v-model="task_order"></input>
     <input type="text" placeholder = "Player 1: Share" v-model="propose1"></input>
     <input type="text" placeholder = "Player 2: Share" v-model="propose2"></input>
     <input type="text" placeholder = "Player 3: Share" v-model="propose3"></input>
     <button v-on:click="propose()">Propose!</button>
  </div>

  <div class = "scroll" v-if="inLobby==false">
     <ul v-for="propose in proposeList" v-on:click="startPropose()">
        <li>Task {{ propose.number }}</li>
        <li>Share1: {{ propose.share1 }}</li>
        <li>Share2: {{ propose.share2 }}</li>
        <li>Share3: {{ propose.share3 }}</li>
        <button>Yes</button>
        <button>No</button>
    </ul>
  </div>








  <router-link to = "/gameend" v-if="inLobby==false">End the game?</router-link>
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

var proposeRef = database.ref().child('proposes');
proposeRef.on('value', (snapshot) => {
    this.proposeList = Object.values(snapshot.val());
    console.log(Object.values(snapshot.val()));
});

export default {
  name: 'GameStart',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      playerList: [],
      profitList: [],
      proposeList: [],
      isHappening: true,
      playerID:'',
      inLobby: true,
      height: 0,
      isProposing: false,
      task_order: '',
      propose1: '',
      propose2: '',
      propose3: '',

    }
  },
  methods: {
    propose: function() {
        firebase.database().ref('proposes/' + this.playerID).set({
           number: this.task_order,
           share1: this.propose1,
           share2: this.propose2,
           share3: this.propose3,
        });
        this.isProposing = false
        this.task_order =  ''
        this.propose1 = ''
        this.propose2 = ''
        this.propose3 = ''
    },


     createNewPlayer: function() {
         writeUserData(this.playerID, 'true', '0', this.height);
         this.inLobby = false;
     },

     byPass: function() {
         this.inLobby = false;
     },

     startPropose: function() {
         this.isProposing = !this.isProposing;
     },




  },

  mounted: function() {
     database.ref().child('users').on('value', (snapshot) => {
     this.playerList = Object.values(snapshot.val());
     this.height = Math.floor(Math.random() * (5 - 1 + 1)) + 1;
     });

     database.ref().child('profits').on('value', (snapshot) => {
     this.profitList = Object.values(snapshot.val());
     });

     database.ref().child('proposes').on('value', (snapshot) => {
     this.proposeList = Object.values(snapshot.val());
     });


  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.vertical-menu {
    width: 250px; /* Set a width if you like */
    padding: 12px;
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

.vertical-menu a img {
    width: 50px; /* you can use % */
    height: auto;
    float: left;
}

.vertical-profit {
    width: 500px; /* Set a width if you like */
    padding: 12px;
}

.vertical-profit a {
    background-color: #eee; /* Grey background color */
    color: black; /* Black text color */
    display: block; /* Make the links appear below each other */
    padding: 12px; /* Add some padding */
    text-decoration: none; /* Remove underline from links */
}

.vertical-profit a:hover {
    background-color: #ccc; /* Dark grey background on mouse-over */
}

.vertical-profit a:hover img {
    transform: scale(1.5);
}


.vertical-profit a.active {
    background-color: #4CAF50; /* Add a green color to the "active/current" link */
    color: white;
}

.vertical-profit a img {
    width: 100px; /* you can use % */
    height: auto;
    float: left;
}

.scroll {
    width: 600px;
    height: 100px;
    overflow: scroll;
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
