<template>
  <div class="container">
    <img src="../assets/gameLogo.png"
    width="500px"

    alt="Avatar"/>

    <span class="notification">{{ message }}</span>
    <div class="loaderSection">
      <span class="loader"></span>
    </div>

    <div class="userInput">
      <input class="customInputBox" type="text" placeholder="Username" v-model="pendingName">
      <input class="customInputBox" type="password" placeholder="Password" v-model="pendingPassword">
    </div>

    <div class="userButton">
      <span class="customButton" @click="signInUser">Login</span>
      <span class="customButton" @click="signUpUser">Sign Up</span>
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
      message: 'It is like doing business, but with cats!',
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
      document.getElementsByClassName('loaderSection')[0].style.visibility = 'visible';
      document.getElementsByClassName('notification')[0].style.visibility = 'hidden';

      var _this = this;
      firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION)
      .then(() => {
        firebase.auth().signInWithEmailAndPassword(_this.pendingEmail, _this.pendingPassword)
        .then(async (user) => {
          _this.uid = user.uid
          const response = await GamesServices.fetchPosts(_this.uid)
          _this.gameid = response.data.gameid
          _this.weight = response.data.weight
          console.log(response.data)
          _this.toGameRoom()
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
          document.getElementsByClassName('loaderSection')[0].style.visibility = 'hidden';
          // Handle Errors here.
          var errorCode = error.code;
          var errorMessage = error.message;
          console.log(errorCode + ': ' + errorMessage);
          if (errorMessage === 'The password is invalid or the user does not have a password.') {
            this.message = 'Wrong password, meow';
          } else if (errorMessage === 'There is no user record corresponding to this identifier. The user may have been deleted.') {
            this.message = 'No such user, meow. Sign up first!';
          }
          document.getElementsByClassName('notification')[0].style.visibility = 'visible';
        })
      })
      .catch((error) => {
        document.getElementsByClassName('loaderSection')[0].style.visibility = 'hidden'
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log(errorCode + ': ' + errorMessage)
        if (errorMessage === 'The password is invalid or the user does not have a password.') {
          this.message = 'Wrong password, meow';
        } else if (errorMessage === 'There is no user record corresponding to this identifier. The user may have been deleted.') {
          this.message = 'No such user, meow. Sign up first!';
        }
        document.getElementsByClassName('notification')[0].style.visibility = 'visible';

      });
    },
    //user has not existed
    async signUpUser () {
      document.getElementsByClassName('loaderSection')[0].style.visibility = 'visible';
      document.getElementsByClassName('notification')[0].style.visibility = 'hidden';

      var _this = this;
      firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION)
      .then(() => {
        firebase.auth().createUserWithEmailAndPassword(_this.pendingEmail, _this.pendingPassword)
        .then(async (user) => {
          _this.uid = user.uid
          const response = await GamesServices.fetchPosts(_this.uid)
          _this.gameid = response.data.gameid
          _this.weight = response.data.weight
          _this.toGameRoom();
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
          document.getElementsByClassName('loaderSection')[0].style.visibility = 'hidden';
          // Handle Errors here.
          var errorCode = error.code;
          var errorMessage = error.message;
          console.log(errorCode + ': ' + errorMessage)
          if (errorMessage === 'The email address is already in use by another account.') {
            this.message = 'Username already taken, meow';
          } else if (errorMessage === 'Password should be at least 6 characters') {
            this.message = 'Password should be at least 6 characters, meow';
          }
          document.getElementsByClassName('notification')[0].style.visibility = 'visible';

        })
      })
      .catch((error) => {
        document.getElementsByClassName('loaderSection')[0].style.visibility = 'hidden';
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log(errorCode + ': ' + errorMessage)
        if (errorMessage === 'The email address is already in use by another account.') {
          this.message = 'Username already taken, meow';
        } else if (errorMessage === 'Password should be at least 6 characters') {
          this.message = 'Password should be at least 6 characters, meow';
        }
        document.getElementsByClassName('notification')[0].style.visibility = 'visible';

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
/* Disable blue border focus in all basic form elements */
input:focus,
select:focus,
textarea:focus,
button:focus {
    outline: none;
}

input[type="text"] {
    font-size: 19px;
}
input[type="password"] {
    font-size: 19px;
}

.loader {
    border: 4px solid #f3f3f3; /* Light grey */
    border-top: 4px solid #22b573; /* Blue */
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
  /* background-color: #b876cc;  */
}

.loaderSection {
  visibility: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.notification {
  display:flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  width: 500px;
  height: 30px;
  font-size: 15px;
  font-family: "Comic Sans MS", cursive, sans-serif;
  font-weight: bold;
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
  height: 100px;
  align-items: flex-start;
  justify-content: center;


}
.customInputBox {
  border-radius: 25px;
  border: 2px solid #22b573;
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
  /* -webkit-border-radius: 28; */
  /* -moz-border-radius: 28; */
  border-radius: 28px;
  font-family: Arial;
  color: #ffffff;
  font-size: 20px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
  margin-left: 5px;
  margin-right: 5px;
  width: 75px;
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
  color: #000000;
}
</style>
