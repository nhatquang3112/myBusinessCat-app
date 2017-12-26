<template>
  <div class="gameplay">
  <h1>This is GamePlay</h1>

  <div v-if="inLobby">

  <button @click="loginFacebook()">Login With Facebook</button>
  <button>Play as Guest</button>
  <img src="https://www.iizcat.com/uploads/2017/04/kr490-bc4.jpg" alt = "Title">
  </div>

  <div v-if="!inLobby">
  <div class = "vertical-menu">
    <a v-for="player in playerList" v-if="player.ingameStatus">
      <img src="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/0b/0bc3ded6d1c690449dd74dee852f6053517749cb_full.jpg" alt = "Ava">
      <li>Player: {{ player.username }}</li>
      <li>Score: {{ player.highscore }}</li>
      <li>Stamina: {{ player.stamina }}</li>
    </a>
  </div>

  <div class = "vertical-profit">
     <a v-for="profit in profitList">
        <img @click="startPropose(profit.Order)" src="http://chefspalate.com.au/wp-content/uploads/2016/05/6.png" alt = "Ava">
        <li>Task {{ profit.Order }}</li>
        <li>Profit: {{ profit.value }}</li>
        <li>Stamina: {{ profit.cost }}</li>
        <div v-if="profit.Order === currentPropose">

           <button @click="propose(profit.Order)">Propose!</button>
        </div>
    </a>
  </div>

  <div class = "scroll">
     <ul v-for="propose in proposeList">
        <li>Task {{ propose.number }}</li>
        <li>Share1: {{ propose.share1 }}</li>
        <li>Share2: {{ propose.share2 }}</li>
        <li>Share3: {{ propose.share3 }}</li>
        <button>Yes</button>
        <button>No</button>
    </ul>
  </div>
  <button @click = "logoutUser()">Log out</button>
  <router-link to = "/gameend">End the game?</router-link>
  </div>


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
const provider = new firebase.auth.FacebookAuthProvider() //for login with facebook



export default {
  name: 'GameStart',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      //the game three main list
      playerList: [],
      profitList: [],
      proposeList: [],
      pendingPropose: [],

      //fill info when proposing
      currentPropose: 0,

      //view mode
      inLobby: true,

      //user info
      playerID:'', //the name of the player
      facebookId:'', //retrieved from login to facebook
      height: 0,
      playerOrder: 0, //to classify player and get score




    }
  },
  methods: {
    //log out current user
    logoutUser() {
      firebase.auth().signOut().then(function() {
      }).catch(function(error) {
        });
      //reset everything
      this.inLobby = true
      //database.ref().child('numPlayer').on('value', (snapshot) => {
        //this.playerOrder = Object.values(snapshot.val());
      //});
      //this.playerOrder --;
      //updateNumPlayer(this.playerOrder);
    },

    //update the number of user
    updateNumPlayer: function(newValue) {
     firebase.database().ref('numPlayer').set(newValue);
    },

    //write user data to realtime database
    //userId is facebook id
    writeUserData: function(userId, ingame, height, name) {
      firebase.database().ref('users/' + userId).set({
        username: name,
        ingameStatus: ingame,
        stamina: height,
        id: userId,
      });
    },

    //make a propose to other players
    propose: function(taskOrder) {
        firebase.database().ref('proposes/' + this.playerID).set({
           number: taskOrder,
           share1: this.propose1,
           share2: this.propose2,
           share3: this.propose3,
        });
        this.isProposing = false
        this.propose1 = ''
        this.propose2 = ''
        this.propose3 = ''
    },


     createNewPlayer: function() {
         writeUserData(this.playerID, 'true', '0', this.height);
         //this.inLobby = false;
     },


     startPropose: function(order) {
        if (this.currentPropose === 0) this.currentPropose = order;
        else this.currentPropose = 0;
     },

     //users login with facebook
     loginFacebook: function() {
       this.loginMethod = 'facebook'
       firebase.auth().signInWithPopup(provider).then(result => {
       console.log(result)
       })
     },



     //check everytime user logged in or logged out
     updateUserStatus: function() {
       firebase.auth().onAuthStateChanged((user) => {
           if (user) {
             // A user is signed in
             this.inLobby = false;
             this.height = Math.floor(Math.random() * (5 - 1 + 1)) + 1;
             this.facebookId = user.providerData[0].uid;
             this.playerID = user.providerData[0].displayName;

             database.ref().child('numPlayer').on('value', (snapshot) => {
             this.playerOrder = Object.values(snapshot.val());
             });
             this.playerOrder ++;

             console.log(this.playerOrder);


             database.ref().child('users').on('value', (snapshot) => {
             this.playerList = Object.values(snapshot.val());
             });

             database.ref().child('profits').on('value', (snapshot) => {
             this.profitList = Object.values(snapshot.val());
             });

             database.ref().child('proposes').on('value', (snapshot) => {
             this.proposeList = Object.values(snapshot.val());
             });

             this.writeUserData(this.facebookId, true, this.height, this.playerID)
             this.updateNumPlayer(this.playerOrder);

           } else {
             // No user is signed in.
             // reset everything


           }
       });
     },




  },

  mounted: function() {
     this.updateUserStatus();
     this.logoutUser()
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
