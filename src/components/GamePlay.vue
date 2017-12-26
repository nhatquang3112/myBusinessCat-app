<template>
  <div class="gameplay">
  <h1>This is GamePlay</h1>

  <div v-if="inLobby">
  <button @click = "createNewPlayer()">Play as Guest</button>
  <img src="https://www.iizcat.com/uploads/2017/04/kr490-bc4.jpg" alt = "Title">
  </div>

  <div v-if="!inLobby">
  <h2>Your are player {{ playerOrder }}</h2>
  <div class = "vertical-menu">
    <a v-for="player in playerList" v-if="player.ingameStatus">
      <img src="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/0b/0bc3ded6d1c690449dd74dee852f6053517749cb_full.jpg" alt = "Ava">
      <li>Player {{ player.rank }}</li>
      <li>Score: {{ player.highscore }}</li>
      <li>Stamina: {{ player.stamina }}</li>
    </a>
  </div>

  <div class = "vertical-profit">
     <h2>{{ notification }}</h2>
     <a v-for="profit in profitList">
        <img @click="startPropose(profit.Order)" src="http://chefspalate.com.au/wp-content/uploads/2016/05/6.png" alt = "Ava">
        <li>Task {{ profit.Order }}</li>
        <li>Profit: {{ profit.value }}</li>
        <li>Stamina: {{ profit.cost }}</li>
        <div v-if="profit.Order === currentPropose">
            <input type="text" placeholder = "Share for player 1" v-model="share1"></input>
            <input type="text" placeholder = "Share for player 2" v-model="share2"></input>
            <input type="text" placeholder = "Share for player 3" v-model="share3"></input>
           <button @click="propose(profit.Order)">Propose!</button>
        </div>
    </a>
  </div>

  <h2>History</h2>
  <div class = "scroll">
     <ul v-for="propose in proposeList">
        <li>Task {{ propose.number }}</li>
        <li>Player 1: {{ propose.share1 }}</li>
        <li>Player 2: {{ propose.share2 }}</li>
        <li>Player 3: {{ propose.share3 }}</li>
        <li>Result: {{ propose.result }}</li>
    </ul>
  </div>

  <h2>Pending propose</h2>
  <ul v-for="propose in pendingProposeList" v-if = "propose.show" >
     <li>Task {{ propose.number }}</li>
     <li>Share1: {{ propose.share1 }}</li>
     <li>Share2: {{ propose.share2 }}</li>
     <li>Share3: {{ propose.share3 }}</li>
     <button>Yes</button>
     <button @click = "rejectPropose()">No</button>
 </ul>


  <button @click = "logoutUser()">Log out</button>
  <router-link to = "/gameend">End the game?</router-link>
  </div>


  </div>
</template>

<script>
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
      pendingProposeList: [],

      //fill info when proposing
      currentPropose: 0,
      share1: '',
      share2: '',
      share3: '',


      //view mode
      inLobby: true,

      //user info
      playerID:'', //the name of the player
      facebookId:'', //retrieved from login to facebook
      height: 0,
      playerOrder: 0, //to classify player and get score
      playDemo: 0,

      //trivia
      notification: '',






    }
  },
  methods: {
      //move a propose from pending to history
      rejectPropose: function() {
        var newHistoryKey = firebase.database().ref().child('proposes').push().key;
        firebase.database().ref('proposes/' + newHistoryKey).set({
          number: this.pendingProposeList[0].number,
          share1: this.pendingProposeList[0].share1,
          share2: this.pendingProposeList[0].share2,
          share3: this.pendingProposeList[0].share3,
          result: 'Rejected',
        });

        firebase.database().ref('pendingPros/info').set({
           number: '',
           share1: '',
           share2: '',
           share3: '',
           show: false,
        });
      },

    //update the number of user
    updateNumPlayer: function(newValue) {
     firebase.database().ref('numPlayer').set({
        number: newValue,
     });
    },

    //make a propose to other players
    propose: function(taskOrder) {
        firebase.database().ref('pendingPros/info').set({
           number: taskOrder,
           share1: this.share1,
           share2: this.share2,
           share3: this.share3,
           show: true,
        });
        this.isProposing = false
        this.startPropose();
        this.share1 = ''
        this.share2 = ''
        this.share3 = ''
    },


     //in case we have to test with non-facebook users
     createNewPlayer: function() {
         this.height = Math.floor(Math.random() * (5 - 1 + 1)) + 1;

         //update the number of player in the database
         database.ref().child('numPlayer').once('value', (snapshot) => {
            this.playerOrder = Object.values(snapshot.val())[0];
            this.playerOrder ++;
            console.log(this.playerOrder);
            this.updateNumPlayer(this.playerOrder);
            this.writeGuestData(this.playerID, 'true', '0', this.height, this.playerOrder);

            this.inLobby = false;

         });

         ////////////////////////////////////////////////////////

     },

     writeGuestData: function(name, ingame, score, height, rank) {
       // Get a key for a new guest.
       var newGuestKey = firebase.database().ref().child('users').push().key;
       firebase.database().ref('users/' + newGuestKey).set({
         username: name,
         ingameStatus: ingame,
         stamina: height,
         score: score,
         rank: rank,
       });
     },



     //to decide which propose input to show
     startPropose: function(order) {
        if (!this.pendingProposeList[0].show) {
          if (this.currentPropose === 0) this.currentPropose = order;
          else this.currentPropose = 0;
        } else {
          this.notification = 'Please wait for the current propose to finish'
          setTimeout(()=>{ this.notification = ''; }, 2500);
        }
     },





  },

  mounted: function() {
     //this.updateUserStatus();
     //this.logoutUser()

     //the following code is for non-facebook test/////////////
     database.ref().child('users').on('value', (snapshot) => {
     this.playerList = Object.values(snapshot.val());
     });

     database.ref().child('profits').on('value', (snapshot) => {
     this.profitList = Object.values(snapshot.val());
     });

     database.ref().child('proposes').on('value', (snapshot) => {
     this.proposeList = Object.values(snapshot.val());
     });

     database.ref().child('pendingPros').on('value', (snapshot) => {
     this.pendingProposeList = Object.values(snapshot.val());
     });
     //end////////////////////////////////////////////////////
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
