<template>
  <div class="container">

    <div class="userInfo">
      <p>userInfo</p>

      <div class = "userBio">
        <span>{{ userName }}</span>
        <span>Stamina: {{ userStamina }}</span>
        <!-- <span>Is end game: {{ isEndGame }}</span>
        <span>Score: {{ userScore }}</span> -->
        <span>Time:
          <span id="myProgress">
            <span id="myBar"></span>
          </span>
        </span>
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
            <span>Score: {{ user.score }}</span>
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
          <button v-if="!showPendingPropose" @click="sendPropose()">Submit</button>
          <span v-if="showPendingPropose">Cannot make propose now</span>
        </div>

        <div class="pendingPropose">
          <p>Pending propose</p>
          <span v-show="showPendingPropose">{{ this.pendingTaskName }}</span>
          <span v-show="!showPendingPropose">There is currently no propose</span>
          <a
            v-for="(pendingTarget, index) in pendingPropose"
            :key="index"
            v-show="showPendingPropose"
          >
            <span>{{ pendingTarget.name }}</span>
            <span>Share: {{ pendingTarget.share }}</span>
            <span>Response: {{ pendingTarget.response }}</span>
          </a>
          <div class="responseOption" v-show="showPendingPropose">
            <button @click="acceptPropose()" v-show="canMakeDecision && !hasDecided">Yes</button>
            <button @click="rejectPropose()" v-show="canMakeDecision && !hasDecided">No</button>
            <span v-show="!canMakeDecision">You cannot make decision</span>
            <span v-show="hasDecided">You have decided!</span>
          </div>


        </div>
      </div>

      <div class="proposeHistory">
        <p>proposeHistory</p>
        <div class="proposeHistoryList">
          <a
            v-for="(propose, index) in proposeHistory"
            :key="index"
            v-if="showProposeHistory"
            class="history"
          >
            <span>{{ propose.taskName }}</span>
            <a
              v-for="(info, index) in propose.history"
              :key="index"
            >
              <span>{{ info.name }}</span>
              <span>Share: {{ info.share }}</span>
            </a>
            <span>{{ propose.result }}</span>
          </a>
      </div>
      </div>

    </div>

  </div>
</template>

<script>
//import
import firebase from '@/config/firebase'
//Constants
const database = firebase.firestore(); //store data in firestore

//helper method for time bar
// var timeleft = 60000 //1 minute
// var downloadTimer = setInterval(function(){
//   document.getElementById("progressBar").value = 60000 - --timeleft;
//   if(timeleft <= 0) clearInterval(downloadTimer);
// },1000)
// setTimeout(console.log('End game'), 6000)

export default {
  name: 'GameRoom',
  props: ['uid'],
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      userName: '',
      userStamina: '',
      userScore: '0',
      isEndGame: false,
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

  watch: {
    pendingPropose () {
      console.log('watcher for pendingPropose called')
      if (this.pendingPropose.length > 0) {
        this.isEndGame = true
        this.pendingPropose.forEach(userInfo => {
          if (userInfo.response !== 'Yes') {
            this.isEndGame = false
          }
          if (userInfo.uid === this.uid) {
            this.userScore = userInfo.share
          }
        })
        if (!this.isEndGame) {
          this.userScore = '0'
        } else if (this.canMakeDecision) {
          this.toEndGame()
        } else {
          this.isEndGame = false
        }
      }
    }
  },

  computed: {
    showPendingPropose () {
      return this.pendingPropose.length > 0
    },
    showProposeHistory () {
      return this.proposeHistory.length > 0
    },
    canMakeDecision () {
      var ans = false
      this.pendingPropose.forEach(userInfo => {
        if (userInfo.uid === this.uid) {
          ans = true
        }
      })
      return ans
    },
    hasDecided () {
      var ans = false
      this.pendingPropose.forEach(userInfo => {
        if (userInfo.uid === this.uid && userInfo.response!=='None') {
          ans = true
        }
      })
      return ans
    }

  },

  methods: {
    startTimer () {
      var elem = document.getElementById("myBar");
      var width = 0;
      var id = setInterval(frame, 1000); //increase timer bar every 1 second
      function frame() {
        if (width < 300) { //5 minutes
          width++;
          elem.style.width = (width/3) + '%';
          elem.innerHTML = width * 1;
        }
      }
    },
    async toEndGame () {
      try {
        //update user score
        if (this.userScore !== '0') {
          await database.collection('users').doc(this.uid).update({
            score: this.userScore
          })
        }
        this.$router.push(`/gameEnd/${this.userScore}`)
      } catch (err) {
        console.log('Error update score:', err)
      }
    },
    async writeSuccessPropose () {
      try {
        var batch = database.batch()
        //write to propose History
        var currentTime = '' + new Date().getTime()
        batch.set(database.collection('proposeHistory').doc(currentTime), {
          history: this.pendingPropose,
          taskName: this.pendingPropose[0].taskName,
          result: 'Accepted',
        })
        //delete all documents in pendingPropose collection
        this.userList.forEach(user => {
          batch.delete(database.collection('pendingPropose').doc(user.uid))
        })
        //commit the batch
        await batch.commit()
        console.log('update, write propose History, delete pending propose success')
      } catch (err) {
        console.log('Error write success propose: ', err)
      }
    },
    async rejectPropose () {
      try {
        var batch = database.batch()
        //update the response status
        batch.update(database.collection('pendingPropose').doc(this.uid), {
          response: 'No'
        })
        //write to propose History
        var currentTime = '' + new Date().getTime()
        batch.set(database.collection('proposeHistory').doc(currentTime), {
          history: this.pendingPropose,
          taskName: this.pendingPropose[0].taskName,
          result: 'Rejected',
        })
        //delete all documents in pendingPropose collection
        this.userList.forEach(user => {
          batch.delete(database.collection('pendingPropose').doc(user.uid))
        })
        //commit the batch
        await batch.commit()
        console.log('update, write propose History, delete pending propose success')
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
        if (this.isEndGame) {
          this.writeSuccessPropose()
        }
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
        if (proposeTarget.share!=='0') {
          var ref = pendingProposeRef.doc(proposeTarget.uid)
          batch.set(ref, {
            name: proposeTarget.name,
            share: proposeTarget.share,
            response: 'None',
            taskName: this.currentTaskName,
            uid: proposeTarget.uid
          })
        }
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

  },

  async mounted () {
    //get list of users from database, also data observer
    var usersRef = database.collection('users')
    usersRef.onSnapshot((querySnapshot) => {
      var users = querySnapshot.docs.map(doc => ({
        name: doc.data().name,
        uid: doc.data().uid,
        stamina: doc.data().stamina,
        score: doc.data().score,
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

    //get current propose History
    var proposeHistoryRef = database.collection('proposeHistory')
    proposeHistoryRef.onSnapshot((querySnapshot) => {
      var proposeHistory = querySnapshot.docs.map(doc => ({
        history: doc.data().history,
        taskName: doc.data().taskName,
        result: doc.data().result
      }))
      this.proposeHistory = proposeHistory
      console.log(this.proposeHistory)
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

    //set time for game to end
    this.startTimer()
    setTimeout(() => { this.toEndGame() }, 300000) //5 minutes
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#myProgress {
  max-width: 100%;
  max-height: 100%;
  background-color: #ddd;
  display: flex;
  justify-content: flex-start;
}

#myBar {
  width: 0%;
  max-weight: 100%;
  max-height: 100%;
  background-color: #4CAF50;
  text-align: center;
  color: white;
}
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
.proposeHistoryList {
  display: flex;
  flex-flow: column;
  overflow-y: scroll;
}
.userBio {
  display: flex;
  flex-flow: column;
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
  flex: 1 1 10%;
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
  overflow-y: scroll;
}
.proposeHistory {
  background-color: #94e835;
  color: #ffffff;
  flex: 1 1 20%;
  display: flex;
  flex-flow: column;
}
.history {
  display: flex;
  flex-flow: column;
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
