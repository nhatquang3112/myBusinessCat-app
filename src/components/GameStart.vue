<template>
  <div class="gamestart">
    <h1>The Adventure of Business Cats</h1>
    <input type="text" placeholder="Email" v-model="pendingEmail">
    <input type="text" placeholder="Password" v-model="pendingPassword">
    <button @click="signInUser">Login</button>
    <button @click="signUpUser">Sign Up</button>


  </div>
</template>

<script>
import firebase from '@/config/firebase'

export default {
  name: 'GameStart',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      pendingEmail: '',
      pendingPassword: '',
      uid: '',
    }
  },

  methods: {
    toGameRoom () {
      this.$router.push(`/gameRoom/${this.uid}`)
    },
    signInUser () {
      firebase.auth().signInWithEmailAndPassword(this.pendingEmail, this.pendingPassword).catch((error) => {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log(errorCode + ': ' + errorMessage)
      });
    },

    signUpUser () {
      firebase.auth().createUserWithEmailAndPassword(this.pendingEmail, this.pendingPassword).catch((error) => {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log(errorCode + ': ' + errorMessage)
      });
    },
  },

  async mounted () {
    //set user data observer
    try { //sign out current user first
      await firebase.auth().signOut()
      console.log('current user signed out')
      firebase.auth().onAuthStateChanged((user) => {
        if (user) {
          this.uid = user.uid
          console.log(this.uid)
          this.toGameRoom()
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
