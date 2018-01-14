<template>
  <div class="container">

    <div class="userInfo">
      <p>userInfo</p>
      <div class = "userBio">
        <span>{{ userName }}</span>
        <span>{{ userStamina }}</span>
      </div>
    </div>

    <div class="gamePlay">
      <div class="userList">
        <p>userList</p>
        <a
          v-for="(user, index) in userList"
          :key="index"
          class = "user"
          v-if="user.name!==userName"
        >
          <span class = "userProfilePic"></span>
          <div class = "userBio">
            <span>{{ user.name }}</span>
            <span>Stamina: {{ user.stamina }}</span>
          </div>
        </a>
      </div>

      <div class="profitList">
        <p>profitList</p>
        <div class="profits">
          <a
            v-for="(profit, index) in profitList"
            :key="index"
            class = "profit"
          >
            <span class = "profitPic"></span>
            <div class = "profitBio">
              <span>Name: {{ profit.name }}</span>
              <span>Value: {{ profit.value }}</span>
              <span>Need: {{ profit.stamina }}</span>
              <button @click = "makePropose(profit.value, profit.stamina, profit.name)">Propose</button>
            </div>
          </a>
        </div>

        <div class="proposeWindow" v-show="showProposeWindow">
          <span>{{ currentTaskName }}</span>
          <a
            v-for="(proposeTarget, index) in proposeWindowList"
            :key="index"
          >
          <span>{{ proposeTarget.name }}</span>
          <span>Share: <input type="text" v-model="proposeTarget.share"></span>
          </a>
          <button @click="sendPropose()">Submit</button>
        </div>

        <div class="pendingPropose">
          <p>Pending propose: {{ this.pendingTaskName }}</p>
          <a
            v-for="(pendingTarget, index) in pendingPropose"
            :key="index"
            v-show="showPendingPropose"
          >
          <span>{{ pendingTarget.name }}</span>
          <span>Share: {{ pendingTarget.share }}</span>
          <span>Response: {{ pendingTarget.response }}</span>
          </a>
          <div class="responseOption">
            <button @click="acceptPropose()">Yes</button>
            <button @click="rejectPropose()">No</button>
          </div>


        </div>
      </div>

      <div class="proposeHistory">
        <p>proposeHistory</p>
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
  props: ['uid'],
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      userName: 'Player 1',
      userStamina: '1',
      userScore: '0',
      showProposeWindow: false,
      currentTaskName: '',
      pendingTaskName: '',
      userList: [],
      proposeWindowList: [],
      profitList: [ //hardcoded for testing
        {name: 'Profit 1',stamina: '10',value: '10',},
        {name: 'Profit 2',stamina: '20',value: '20',},
        {name: 'Profit 3',stamina: '30',value: '30',},
      ],
      proposeHistory: [],
      pendingPropose: [],

    }
  },

  computed: {
    showPendingPropose () {
      return this.pendingPropose.length > 0
    }
  },

  methods: {
    async rejectPropose () {
      try {
        //change the response status
        await database.collection('pendingPropose').doc(this.uid).update({
          response: 'No'
        })
        console.log('reject propose success')
        //write to propose History
        var currentTime = new Date().getTime()
        database.collection('proposeHistory').doc(currentTime).set({
          taskName: this.pendingPropose[0].taskName,

        })


      } catch (err) {
        console.log('Error rejecting propose: ', err)
      }
    },

    async acceptPropose () {
      try {
        await database.collection('pendingPropose').doc(this.uid).update({
          response: 'Yes'
        })
        console.log('accept propose success')
      } catch (err) {
        console.log('Error accepting propose: ', err)
      }
    },
    //send propose info to database to become pending propose
    sendPropose () {
      console.log(this.proposeWindowList)
      var pendingProposeRef = database.collection('pendingPropose')
      var batch = database.batch()
      this.proposeWindowList.forEach(proposeTarget => {
        console.log(proposeTarget)
        var ref = pendingProposeRef.doc(proposeTarget.uid)
        batch.set(ref, {
          name: proposeTarget.name,
          share: proposeTarget.share,
          response: 'None',
          taskName: this.currentTaskName,
          uid: proposeTarget.uid
        })
      })
      batch.commit()
      console.log('batch wrote successful')
      this.showProposeWindow = !this.showProposeWindow
    },

    //open window to start proposing
    makePropose(value, stamina, taskName) {
      this.currentTaskName = taskName
      this.showProposeWindow = !this.showProposeWindow
    },
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

  async mounted () {
    //get list of users from database, also and observer
    var usersRef = database.collection('users')
    usersRef.onSnapshot((querySnapshot) => {
      var users = querySnapshot.docs.map(doc => ({
        name: doc.data().name,
        uid: doc.data().uid,
        stamina: doc.data().stamina,
      }))
      this.userList = users
      this.proposeWindowList = users
    })

    //get current pending propose
    var pendingProposeRef = database.collection('pendingPropose')
    pendingProposeRef.onSnapshot((querySnapshot) => {
      var pendingPropose = querySnapshot.docs.map(doc => ({
        name: doc.data().name,
        uid: doc.data().uid,
        share: doc.data().share,
        response: doc.data().response,
        taskName: doc.data().taskName,
      }))
      this.pendingPropose = pendingPropose
      this.pendingTaskName = this.pendingPropose[0].taskName
      console.log(this.pendingPropose)
    })

    try {
      //get info of current logged in user
      var userInfoRef = database.collection('users').doc(this.uid)
      var doc = await userInfoRef.get()
      if (doc.exists) {
        this.userName = doc.data().name
        this.userStamina = doc.data().stamina
      } else {
        console.log('user info not exist')
      }
    } catch (err) {
      console.log('error gettting user info: ', err)
    }




  }
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
.class {
  display: flex;
}
.pendingPropose {
  display: flex;
  flex-flow: column;
  background-color: #7742f4;
  flex: 1 1 33%;
}
.userInfo {
  display: flex;
  flex: 1 1 11%;
  justify-content: center;
  background-color: #4286f4;
  color: #ffffff;
}
.gamePlay {
  display: flex;
  flex: 1 1 88%;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: 100%;

}
.userList {
  background-color: #e85537;
  color: #ffffff;
  flex: 1 1 15%;
}
.profitList {
  background-color: #e8d336;
  color: #ffffff;
  flex: 1 1 69%;
  display: flex;
  flex-flow: column;
}
.profits {
  flex: 1 1 66%;
}
.pendingPropose {
  flex: 1 1 11%;
}
.proposeHistory {
  background-color: #94e835;
  color: #ffffff;
  flex: 1 1 15%;
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
