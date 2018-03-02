<template>
  <div class="container">
    <img src="../assets/gameLogo.png"
    width="500px"

    alt="Avatar"/>

    <div class="userInput">
      <input class="customInputBox" type="text" placeholder="Name" v-model="pendingName">
      <input class="customInputBox" type="password" placeholder="Password" v-model="pendingPassword">
    </div>

    <div class="userButton">
      <button class="customButton" @click="signInUser">Login</button>
      <button class="customButton" @click="signUpUser">Sign Up</button>
    </div>


  </div>
</template>

<script>
import firebase from '@/config/firebase'
import GamesServices from '@/services/GamesServices'

// Constants
const database = firebase.firestore() // firestore

export default {
  name: 'GameStart',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      pendingName: '',
      pendingPassword: '',
      uid: '',
      gameid: '',
      weight: '',
    }
  },

  computed: {
    pendingEmail () {
      return this.pendingName + '@gmail.com'
    }

  },

  methods: {
    toGameRoom () {
      this.$router.push(`/gameRoom/${this.uid}/${this.gameid}/${this.weight}`)
    },
    //user already exists
    signInUser () {
      firebase.auth().signInWithEmailAndPassword(this.pendingEmail, this.pendingPassword)
      .then(async (user) => {
        this.uid = user.uid
        const response = await GamesServices.fetchPosts(this.uid)
        this.gameid = response.data.gameid
        this.weight = response.data.weight
        console.log(response.data)
        this.toGameRoom()
        //write user data to database
        // database.collection('games').doc(this.gameid).collection('users').doc(user.uid).set({
        //   name: user.email,
        //   stamina: this.weight,
        //   uid: user.uid,
        //   score: 0,
        //   status: 'inPlay',
        // })
        // .then(() => {
        //   console.log('Write user data successful')
        //   this.toGameRoom()
        // })
        // .catch((err) => {
        //   console.log('Error writing user data: ', err)
        // })
      })
      .catch((error) => {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log(errorCode + ': ' + errorMessage)
      });
    },
    //user has not existed
    async signUpUser () {
      firebase.auth().createUserWithEmailAndPassword(this.pendingEmail, this.pendingPassword)
      .then(async (user) => {
        this.uid = user.uid
        const response = await GamesServices.fetchPosts(this.uid)
        this.gameid = response.data.gameid
        this.weight = response.data.weight
        this.toGameRoom();
        //write user data to database
        // database.collection('games').doc(this.gameid).collection('users').doc(user.uid).set({
        //   name: user.email,
        //   stamina: this.weight,
        //   uid: user.uid,
        //   score: 0,
        //   status: 'inPlay',
        // })
        // .then(() => {
        //   console.log('Write user data successful')
        //   this.toGameRoom()
        // })
        // .catch((err) => {
        //   console.log('Error writing user data: ', err)
        // })
      })
      .catch((error) => {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log(errorCode + ': ' + errorMessage)
      });


    },
  },

  async mounted () {
    try {
      //sign out current user first
      await firebase.auth().signOut()
      console.log('current user signed out')
      //set user data observer
      firebase.auth().onAuthStateChanged((user) => {
        if (user) {
          this.uid = user.uid
        } else {
          console.log('No user currently signed in')
        }
      });
    } catch (err) {
      console.log('Error signing out user: ', err)
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
  justify-content: center;
  align-items: center;
}
.userInput {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  width: 500px;
  height: 200px
}
.userButton {
  display: flex;
  width: 500px;
  height: 200px;
  align-items: flex-start;
  justify-content: center;


}
.customInputBox {
  border-radius: 25px;
  border: 2px solid #609;
  margin: 5px;

  padding: 20px;
  width: 200px;
  height: 15px;
}

.customButton {
  background: #cb34d9;
  background-image: -webkit-linear-gradient(top, #cb34d9, #662bb8);
  background-image: -moz-linear-gradient(top, #cb34d9, #662bb8);
  background-image: -ms-linear-gradient(top, #cb34d9, #662bb8);
  background-image: -o-linear-gradient(top, #cb34d9, #662bb8);
  background-image: linear-gradient(to bottom, #cb34d9, #662bb8);
  -webkit-border-radius: 28;
  -moz-border-radius: 28;
  border-radius: 28px;
  font-family: Arial;
  color: #ffffff;
  font-size: 20px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
}

.customButton:hover {
  background: #c43cfa;
  text-decoration: none;
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
