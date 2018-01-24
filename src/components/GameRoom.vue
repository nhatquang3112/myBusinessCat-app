<template>
  <div class="container">

    <div class="userInfo">
      <div class="userBox">
        <span class="avatar">
          <img src="https://pbs.twimg.com/profile_images/706844157093027840/2Aan_aSU_400x400.jpg"
          alt="Avatar"/>
        </span>

        <div class = "userBio">
          <span>{{ userName }}</span>

          <span class="staminaBar" v-bind:style="{width: this.userStamina + '%'}">{{ userStamina }}</span>

          <div class="timer">
            <span>Timer </span>
            <span id="gameProgress">
              <span id="gameBar"></span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="gamePlay">
      <div class="userList">
        <a
          v-for="(user, index) in userList"
          :key="index"
          v-if="user.name!==userName"
        >
          <div class = "userBio">
            <div class="userBox">
              <span class="avatar">
                <img src="https://pbs.twimg.com/profile_images/706844157093027840/2Aan_aSU_400x400.jpg"
                alt="Avatar"/>
              </span>

              <div class = "userBio">
                <span>{{ user.name }}</span>
                <span class="staminaBar" v-bind:style="{width: user.stamina + '%'}">{{ user.stamina }}</span>
                <span>Score: {{ user.score }}</span>
              </div>
            </div>
          </div>
        </a>
      </div>

      <div class="profitList">
        <div class="profits">
          <a
            v-for="(profit, index) in profitList"
            :key="index"
            class="profit"
          >
            <div class="profitInfo" @click = "makePropose(profit.value, profit.stamina, profit.name)">
              <span>Value: {{ profit.value }}</span>
              <span><img src="https://d30y9cdsu7xlg0.cloudfront.net/png/53189-200.png" alt="ProfitIMG"></span>
              <span class="ladder" v-bind:style="{height: profit.stamina + '%'}">
                <span>{{ profit.stamina }}</span>
              </span>
              <span>{{ profit.name }}</span>
            </div>


            <div class="proposeWindow" v-show="currentTaskName===profit.name">
              <a
                v-for="(proposeTarget, index) in proposeWindowList"
                :key="index"
              >
              <div class="proposeWindowElement">
                <span>{{ proposeTarget.name }}</span>
                <div class="inputBox" v-show="proposeTarget.share!=='0'">
                  <span><input type="text" v-model="proposeTarget.share" placeholder="Share"></span>
                  <span class="closeButton" @click="proposeTarget.share='0'"><i class="fas fa-times-circle"></i></span>
                </div>
                <span v-show="proposeTarget.share==='0'" @click="proposeTarget.share=''"><i class="fas fa-plus-circle"></i></span>
              </div>
              </a>
              <span><button class="button"v-if="!showPendingPropose" @click="sendPropose()">Submit</button></span>
              <span v-if="showPendingPropose">Cannot make propose now</span>
            </div>
          </a>
        </div>


        <div class="pendingPropose">
          <span v-show="showPendingPropose">Time:
            <span id="proposeProgress">
              <span id="proposeBar"></span>
            </span>
          </span>
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
//global variables
var proposeTimer
var gameBar //loading bar for game timer
var proposeBar //loading bar propose timer

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
      currentTaskName: '',
      pendingTaskName: '',
      userList: [],
      proposeWindowList: [],
      profitList: [ //hardcoded for testing
        {name: 'Profit 1',stamina: 50 ,value: 10,},
        {name: 'Profit 2',stamina: 20 ,value: 20,},
        {name: 'Profit 3',stamina: 30 ,value: 30,},
      ],
      proposeHistory: [],
      pendingPropose: [],
      minStamina: 999,
      totalPlayerStamina: 0,
    }
  },

  watch: {
    userList () {
      var numPlayer = 0
      this.totalPlayerStamina = 0
      this.userList.forEach(user => {
        if (user.status === 'inPlay') {
          numPlayer++
          this.totalPlayerStamina += user.stamina
        }
      })
      if (numPlayer === 1) {
        console.log('End game because of number player = 1')
        this.toEndGame()
      }
      if (this.totalPlayerStamina < this.minStamina) {
        console.log('End game because of inefficient stamina')
        this.toEndGame()
      }
    },
    showPendingPropose () {
      if (this.showPendingPropose) {
        //start the propose bar
        this.startProposeBar()
        console.log('propose bar called')
      } else {
        //stop the propose bar
        clearInterval(proposeBar)
        console.log('propose bar stopped')
      }
    },
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
          console.log('End game because all yes')
          this.toEndGame()
        } else {
          this.isEndGame = false
        }
      } else {
        clearTimeout(proposeTimer)
        console.log('clear propose timer called')
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
    },

  },

  methods: {
    startGameBar () {
      console.log('game timer called')
      var elem = document.getElementById("gameBar");
      var width = 300;
      gameBar = setInterval(frame, 1000); //increase timer bar every 1 second
      function frame() {
        if (width > 0) { //5 minutes
          width--;
          elem.style.width = (width/3) + '%';
          elem.innerHTML = width * 1;
        }
      }
    },
    startProposeBar () {
      console.log('propose timer called')
      var elem = document.getElementById("proposeBar");
      var width = 30;
      proposeBar = setInterval(frame, 1000); //increase timer bar every 1 second
      function frame() {
        if (width > 0) { //30 seconds
          width--;
          elem.style.width = ((width*10)/3) + '%';
          elem.innerHTML = width * 1;
        }
      }
    },
    async toEndGame () {
      try {
        //update user score and in game status
        await database.collection('users').doc(this.uid).update({
          score: this.userScore,
          status: 'outPlay'
        })

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
    async sendPropose () {
      console.log(this.proposeWindowList)
      var pendingProposeRef = database.collection('pendingPropose')
      var batch = database.batch()
      this.proposeWindowList.forEach(proposeTarget => {
        if (proposeTarget.share!=='0') {
          var ref = pendingProposeRef.doc(proposeTarget.uid)
          batch.set(ref, {
            name: proposeTarget.name,
            share: Number(proposeTarget.share),
            response: 'None',
            taskName: this.currentTaskName,
            uid: proposeTarget.uid
          })
        }
      })
      try {
        batch.commit()
        console.log('batch wrote successful')
        this.setTimeToDeletePropose() //delete propose incase no response is received in 30 seconds
      } catch (err) {
        console.log('Error sending propose: ', err)
      }

      this.currentTaskName = '' //close propose window after sending the propose
    },

    setTimeToDeletePropose () {
      console.log('propose timer called')
      proposeTimer = setTimeout(async () => {
        try {
          var batch = database.batch()
          //write to propose History
          var currentTime = '' + new Date().getTime()
          batch.set(database.collection('proposeHistory').doc(currentTime), {
            history: this.pendingPropose,
            taskName: this.pendingPropose[0].taskName,
            result: 'Out of Date',
          })
          //delete all documents in pendingPropose collection
          this.userList.forEach(user => {
            batch.delete(database.collection('pendingPropose').doc(user.uid))
          })
          //commit the batch
          await batch.commit()
        } catch (err) {
          console.log('Error deleting out-of-date propose: ', err)
        }
      }, 30000) //30 seconds
    },

    //open window to start proposing
    makePropose(value, stamina, taskName) {
      // this.proposeWindowList.forEach(user => {
      //   user.share = '';
      // })
      if (this.currentTaskName===taskName) {
        this.currentTaskName = ''
      } else {
        this.currentTaskName = taskName
      }
    },

  },

  async mounted () {
    //get list of users from database, also data observer
    var usersRef = database.collection('users')
    usersRef.onSnapshot((querySnapshot) => {
      var users = querySnapshot.docs.map(doc => ({
        name: doc.data().name.substring(0, doc.data().name.lastIndexOf("@")),
        uid: doc.data().uid,
        stamina: doc.data().stamina,
        score: doc.data().score,
        status: doc.data().status,
        share: '',
      }))
      this.userList = users
      this.proposeWindowList = users
      //update minStamina
      this.profitList.forEach(profit => {
        if (this.minStamina > profit.stamina) {
          this.minStamina = profit.stamina
        }
      })
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
        this.userName = doc.data().name.substring(0, doc.data().name.lastIndexOf("@"))
        this.userStamina = doc.data().stamina
      } else {
        console.log('user info not exist')
      }
    } catch (err) {
      console.log('error gettting user info: ', err)
    }

    //set time for game to end
    this.startGameBar()
    setTimeout(() => {
      console.log('End game because of time out')
      this.toEndGame()
    }, 300000) //5 minutes
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#gameProgress {
  width: 150px;
  max-height: 100%;
  background-color: #ddd;
  display: flex;
  justify-content: flex-start;
  margin-left: 10px;
  border-radius: .3em;
}

#gameBar {
  width: 100%;
  max-weight: 100%;
  max-height: 100%;
  background-color: #4CAF50;
  text-align: center;
  color: white;
  border-radius: .3em;
}

#proposeProgress {
  max-width: 100%;
  max-height: 100%;
  background-color: #ddd;
  display: flex;
  justify-content: flex-start;
  border-radius: .3em;
}

#proposeBar {
  width: 100%;
  max-weight: 100%;
  max-height: 50%;
  background-color: #4CAF50;
  text-align: center;
  color: white;
  border-radius: .3em;
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

.timer {
  display: flex;
}
.pendingPropose {
  display: flex;
  flex-flow: column;
  background-color: #7742f4;
  flex: 1 1 33%;
  justify-content: center;
  align-items: center;
}
.staminaBar {
  display: flex;
  flex-flow: row;
  border-radius: .3em;
  background-color: #ffa621;
  justify-content: center;
  align-items: center;
}
.staminaProcess {
  display: flex;
  flex-flow: row;
}
.userInfo {
  display: flex;
  flex: 1 1 11%;
  justify-content: center;
  align-items: center;
  /* background-color: #4286f4; */
  color: #ffffff;
}
.userBox {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: .3em;
  padding: 0.5rem;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
  width: 300px;
}
.avatar img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
}
.userBio {
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  margin-left: 12px;
  color: #1aaaba;
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
  color: #ffffff;
  flex: 1 1 10%;
}
.profitList {
  color: #ffffff;
  flex: 1 1 69%;
  display: flex;
  flex-flow: column;
}
.profits {
  flex: 1 1 66%;
  display: flex;
  flex-flow: row;
}

.profit {
  flex: 1 1 33%;
}

.profitInfo {
  width: 100%;
  height: 77%;
  justify-content: flex-end;
  align-items: center;
  transition: all .2s ease-in-out;
  display: flex;
  flex-flow: column;
}

.profitInfo:hover {
  transform: scale(1.1);
}
.profit img {
  width: 100px;
  height: 100px;
}

.ladder {
  background-color: #ffa621;
  border-radius: .3em;
  width: 50px;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
}

.proposeWindow {
  height: 22%;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: .3em;
  padding: 0.5rem;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;

}

.proposeWindowElement {
  display: flex;
  flex-flow: row;
  margin: 0.3rem;
}

.button {
  background-color: #36e27e;
  border: none;
  border-radius: .2em;
  border: solid 1px #1cbc5f ;
}

.inputBox {
  display: flex;
  flex-flow: row;
  border-radius: .2em;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
}


.pendingPropose {
  flex: 1 1 11%;

}
.proposeHistory {
  background-color: #94e835;
  color: #ffffff;
  flex: 1 1 20%;
  /* display: flex; */
  display: none;
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
