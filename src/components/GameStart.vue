<template>
  <div class="gamestart">
    <h1>The Adventure of Business Cats</h1>

    <input type="text" placeholder="Name" v-model="pendingName">
    <input type="password" placeholder="Password" v-model="pendingPassword">
    <button @click="signInUser">Login</button>
    <button @click="signUpUser">Sign Up</button>


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
      rank: '',
    }
  },

  computed: {
    pendingEmail () {
      return this.pendingName + '@gmail.com'
    }

  },

  methods: {
    toGameRoom () {
      this.$router.push(`/gameRoom/${this.uid}/${this.gameid}/${this.rank}`)
    },
    //user already exists
    signInUser () {
      firebase.auth().signInWithEmailAndPassword(this.pendingEmail, this.pendingPassword)
      .then(async (user) => {
        this.uid = user.uid
        const response = await GamesServices.fetchPosts(this.uid)
        this.gameid = response.data.gameid
        this.rank = response.data.rank
        this.toGameRoom()
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
      .then((user) => {
        this.uid = user.uid
        //write user data to database
        database.collection('users').doc(user.uid).set({
          name: user.email,
          stamina: 9, //hardcoded for testing
          uid: user.uid,
          score: 0,
          status: 'inPlay',
        })
        .then(() => {
          console.log('Write user data successful')
          this.toGameRoom()
        })
        .catch((err) => {
          console.log('Error writing user data: ', err)
        })
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
