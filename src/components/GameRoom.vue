<template>
  <div class="container">
    <div class="waitingScreen" v-show="isWaitingForPLayer">

      <div class="loaderSection">
        <span class="loader"></span>
      </div>

      <img src="../assets/LoadingCat.png"
      width="250px"
      alt="Avatar"/>

      <div class="messageSection">
        <span class="watingMessage">
          Waiting for {{ numPlayerWaitingFor }} more to do business
        </span>
        <span class="watingMessage">
          Please be patient, meow
        </span>
      </div>


    </div>

    <div class="userInfo" v-show="!isWaitingForPLayer && !isNewUi">
      <div class="mainUserBox">
        <span class="avatar">
          <img v-if="userName === 'Red Cat'" src="../assets/RedCat.png" alt="Avatar"/>
          <img v-if="userName === 'Blue Cat'" src="../assets/BlueCat.png" alt="Avatar"/>
          <img v-if="userName === 'Brown Cat'" src="../assets/BrownCat.png" alt="Avatar"/>
          <img v-if="userName === 'Yellow Cat'" src="../assets/YellowCat.png" alt="Avatar"/>
          <img v-if="userName === 'Green Cat'" src="../assets/GreenCat.png" alt="Avatar"/>
        </span>

        <div class = "userBio">
          <span>{{ userName }}</span>
          <!-- <span>{{ gameid }}</span>
          <span>{{ rank }}</span> -->


          <span class="staminaBar" v-bind:style="{width: this.userStamina + '%'}">{{ userStamina }}</span>

          <div class="gameTimer">
            <span>Time</span>
            <span id="gameProgress">
              <span id="gameBar"></span>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="gamePlay" v-show="!isWaitingForPLayer && !isNewUi">
      <div class="userList">
        <div
          v-for="(user, index) in userList"
          :key="index"
          v-if="user.name!==userName"
          class = "userBox"
        >
          <span class="avatar">
            <img v-if="user.name === 'Red Cat'" src="../assets/RedCat.png" alt="Avatar"/>
            <img v-if="user.name === 'Blue Cat'" src="../assets/BlueCat.png" alt="Avatar"/>
            <img v-if="user.name === 'Brown Cat'" src="../assets/BrownCat.png" alt="Avatar"/>
            <img v-if="user.name === 'Yellow Cat'" src="../assets/YellowCat.png" alt="Avatar"/>
            <img v-if="user.name === 'Green Cat'" src="../assets/GreenCat.png" alt="Avatar"/>
          </span>

          <div class = "userBio">
            <span>{{ user.name }}</span>
            <span class="staminaBar" v-bind:style="{width: user.stamina + '%'}">{{ user.stamina }}</span>
            <span>Score: {{ user.score }}</span>
          </div>
        </div>
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
              <span><img src="../assets/Fish.png" alt="ProfitIMG"></span>
              <span class="ladder" v-bind:style="{height: profit.stamina + '%'}">
                <span>{{ profit.stamina }}</span>
              </span>
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
              <span><button class="button"v-if="!showPendingPropose" @click="checkPropose()">Submit</button></span>
              <span>{{ errorMessage }}</span>
              <span v-if="showPendingPropose">Cannot make propose now</span>
            </div>
          </a>
        </div>


        <div class="pendingPropose">
          <!-- <span v-show="showPendingPropose">
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
          </div> -->
          <div class="pendingProposeInfo" v-show="showPendingPropose">
            <div class="taskNameAndTimer">
              <span class="taskName">{{ pendingTaskName }}</span>
              <span class="clockIcon"><i class="far fa-clock"></i></span>
              <span class="timer">
                <span id="proposeProgress">
                  <!-- <span id="proposeBar"></span> -->
                </span>
            </span>
            </div>

            <div class="infoColumns">
              <span class="nameColumn">
                <span
                  v-for="(pendingTarget, index) in pendingPropose"
                  :key="index"
                  class="itemInColumn"
                  >
                  {{ pendingTarget.name }}
                </span>
              </span>
              <span class="shareColumn">
                <span
                  v-for="(pendingTarget, index) in pendingPropose"
                  :key="index"
                  class="shareBar"
                  v-bind:style="{width: pendingTarget.share + '%'}"
                  >
                  {{ pendingTarget.share }}
                </span>
              </span>
              <span class="responseColumn">
                <span
                  v-for="(pendingTarget, index) in pendingPropose"
                  :key="index"
                  class="itemInColumn"
                  >
                  <span v-show="pendingTarget.response==='Yes'"><i class="fas fa-check"></i></span>
                  <span v-show="pendingTarget.response==='None'">Waiting for response</span>
                </span>
              </span>
            </div>

            <div class="responseOption">
              <span v-show="canMakeDecision && !hasDecided"><button class="button" @click="acceptPropose()">Yes</button></span>
              <span v-show="canMakeDecision && !hasDecided"><button class="button" @click="rejectPropose()">No</button></span>
              <span v-show="!canMakeDecision">You cannot make decision</span>
              <span v-show="hasDecided">You have decided!</span>
            </div>
          </div>

          <span class="pendingProposePlaceHolder" v-show="!showPendingPropose">
            There is currently no proposal
          </span>
        </div>
      </div>

      <div class="proposeHistory">
        <div class="proposeHistoryBar">
          <span>Proposal History</span>
          <span v-show="!isHistoryHidden" @click="toggleHistoryVisibility()"><i class="fas fa-chevron-up"></i></span>
          <span v-show="isHistoryHidden" @click="toggleHistoryVisibility()"><i class="fas fa-chevron-down"></i></span>
        </div>
        <div id="proposeHistoryList" v-show="!isHistoryHidden">
          <span
            v-for="(propose, index) in proposeHistory"
            :key="index"
            v-if="showProposeHistory"
            class="history"
          >
            <span>{{ propose.taskName }}</span>
            <span
              v-for="(info, index) in propose.history"
              :key="index"
            >
              <span>{{ info.name }}</span>
              <span>Share: {{ info.share }}</span>
            </span>
            <span>{{ propose.result }}</span>
          </span>
      </div>
      </div>

    </div>

    <div class="catListAndFishList" v-show="!isWaitingForPLayer && isNewUi">
      <div class="catList">
        <div class="catYou">
          <img class="catIcon" v-if="userName === 'Red Cat'" src="../assets/catRed.png" alt="Avatar"/>
          <img class="catIcon" v-if="userName === 'Blue Cat'" src="../assets/catBlue.png" alt="Avatar"/>
          <img class="catIcon" v-if="userName === 'Brown Cat'" src="../assets/catBrown.png" alt="Avatar"/>
          <img class="catIcon" v-if="userName === 'Yellow Cat'" src="../assets/catYellow.png" alt="Avatar"/>
          <img class="catIcon" v-if="userName === 'Green Cat'" src="../assets/catGreen.png" alt="Avatar"/>
          <div class="catInfo">
            <div class="catName" style="color: white; font-size: 1vw">{{ userName }} (You)</div>
            <div class="catClimbInfo">
              <span style="color: black; font-size: 1vw">Can climb</span>
              <span class="ladderIcon"></span>
              <span style="color: white; font-size: 2vw">{{ userStamina }}</span>
            </div>
          </div>
        </div>
        <div class="catOther"
          v-for="(user, index) in userList"
          :key="index"
          v-if="user.name!==userName">
          <img class="catIcon" v-if="user.name === 'Red Cat'" src="../assets/catRed.png" alt="Avatar"/>
          <img class="catIcon" v-if="user.name === 'Blue Cat'" src="../assets/catBlue.png" alt="Avatar"/>
          <img class="catIcon" v-if="user.name === 'Brown Cat'" src="../assets/catBrown.png" alt="Avatar"/>
          <img class="catIcon" v-if="user.name === 'Yellow Cat'" src="../assets/catYellow.png" alt="Avatar"/>
          <img class="catIcon" v-if="user.name === 'Green Cat'" src="../assets/catGreen.png" alt="Avatar"/>
          <div class="catInfo">
            <div class="catName" style="color: white; font-size: 1vw">{{ user.name }}</div>
            <div class="catClimbInfo">
              <span style="color: black; font-size: 1vw">Can climb</span>
              <span class="ladderIcon"></span>
              <span style="color: white; font-size: 1.5vw">{{ user.stamina }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="fishList">
        <div class="fishSection"
          v-for="(profit, index) in profitList"
          :key="index">
          <div v-bind:class="{ 'fishSize0': profit.rank===0, 'fishSize1': profit.rank===1, 'fishSize2': profit.rank===2, 'fishSize3': profit.rank===3, 'fishSize4': profit.rank===4}"
            @click = "makePropose(profit.value, profit.stamina, profit.name)">
            <span style="color: #6D4620; font-size: 2.5vw; font-family: Impact, Charcoal, sans-serif">{{ profit.value }}</span>
          </div>
          <span class="ladderFish" @click = "makePropose(profit.value, profit.stamina, profit.name)"></span>
          <span style="color: #6D4620; font-size: 2vw; font-family: Impact, Charcoal, sans-serif">{{ profit.stamina }}</span>
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
            <span><button class="button"v-if="!showPendingPropose" @click="checkPropose()">Submit</button></span>
            <span>{{ errorMessage }}</span>
            <span v-if="showPendingPropose">Cannot make propose now</span>
          </div>
        </div>
      </div>
    </div>
    <div class="clockAndProposalHistoryBox" v-show="!isWaitingForPLayer && isNewUi">
      <div class="clock">
        <div class="watch"></div>
        <!-- <div class="ldBar label-center" data-type="fill" data-img="https://orig00.deviantart.net/1378/f/2012/281/5/5/8_bit_kirby_sprite_by_toshirofrog-d5h7rpp.png"></div> -->
        <!-- <div
          class="ldBar label-center"
          style="width:50%;height:50%;margin:auto"
          data-value="50"
          data-preset="circle"
          data-type="fill"
          data-img="../assets/clock.png"
          data-fill-dir="ttb"
        ></div> -->
        <div class="watchInfo">
          <span style="color: black; font-size: 5vw; font-family: Impact, Charcoal, sans-serif">300</span>
          <span style="color: black; font-size: 2.5vw; font-family: Impact, Charcoal, sans-serif">seconds</span>
          <span style="color: black; font-size: 1.5vw; font-family: Impact, Charcoal, sans-serif">left for business</span>
        </div>
      </div>
      <div class="proposalHistoryBox">
        <div class="currentProposalLabelBox">
          <div class="currentProposalLabel">
          </div>
        </div>
        <div class="historyBox">
          <div class="historyBoxName">
            <span style="color: white">Proposal History</span>
          </div>
          <div class="historyBoxHistory" v-chat-scroll>
            <span style="color: #808080" v-show="!this.isThereAnyHistory">Empty History</span>
            <div
              v-for="(propose, index) in proposeHistory"
              :key="index"
              v-if="showProposeHistory"
              class="proposeHistoryItem"
            >
              <div class="totalShare">
                <span style="color: #CCCCCC; font-size: 1vw; font-family: Impact, Charcoal, sans-serif">Total share</span>
                <span style="color: #CCCCCC; font-size: 2vw; font-family: Impact, Charcoal, sans-serif">{{propose.taskName}}</span>
              </div>

              <div class="listOfEachShare">
                <div class="eachShare"
                  v-for="(target, index) in propose.history"
                  :key="index"
                >
                  <img v-if="target.name === 'Red Cat'" src="../assets/catRed.png" alt="Avatar" width="50%" height="70%"/>
                  <img v-if="target.name === 'Blue Cat'" src="../assets/catBlue.png" alt="Avatar" width="50%" height="70%"/>
                  <img v-if="target.name === 'Yellow Cat'" src="../assets/catYellow.png" alt="Avatar" width="50%" height="70%"/>
                  <img v-if="target.name === 'Brown Cat'" src="../assets/catBrown.png" alt="Avatar" width="50%" height="70%"/>
                  <img v-if="target.name === 'Green Cat'" src="../assets/catGreen.png" alt="Avatar" width="50%" height="70%"/>
                  <span style="color: #CCCCCC; font-size: 2vw; font-family: Impact, Charcoal, sans-serif">{{ target.share }}</span>
                  <span class="responseStatus" width="40%" height="70%">
                    <i class="far fa-question-circle" v-show="target.response==='None'" color=black></i>
                    <i class="far fa-check-circle" v-show="target.response==='Yes'" color=black></i>
                    <i class="far fa-times-circle" v-show="target.response==='No'" color=black></i>
                  </span>
                </div>
              </div>

              <div class="selectionButton">
                <span style="color: #CCCCCC;">{{ propose.result }}</span>
              </div>
            </div>
          </div>

          <div class="historyBoxPendingPropose">
            <span style="color: white" v-show="!showPendingPropose">There is no pending proposal. Let's do business!</span>

            <div class="totalShare" v-show="showPendingPropose">
              <span style="color: white; font-size: 1.5vw; font-family: Impact, Charcoal, sans-serif">Total share</span>
              <span style="color: #CCCCCC; font-size: 2.5vw; font-family: Impact, Charcoal, sans-serif">{{ pendingTaskName }}</span>
            </div>

            <div class="listOfEachShare" v-show="showPendingPropose">
              <div class="eachShare"
                v-for="(pendingTarget, index) in pendingPropose"
                :key="index"
              >
                <img v-if="pendingTarget.name === 'Red Cat'" src="../assets/catRed.png" alt="Avatar" width="50%" height="70%"/>
                <img v-if="pendingTarget.name === 'Blue Cat'" src="../assets/catBlue.png" alt="Avatar" width="50%" height="70%"/>
                <img v-if="pendingTarget.name === 'Yellow Cat'" src="../assets/catYellow.png" alt="Avatar" width="50%" height="70%"/>
                <img v-if="pendingTarget.name === 'Brown Cat'" src="../assets/catBrown.png" alt="Avatar" width="50%" height="70%"/>
                <img v-if="pendingTarget.name === 'Green Cat'" src="../assets/catGreen.png" alt="Avatar" width="50%" height="70%"/>
                <span style="color: #CCCCCC; font-size: 2.5vw; font-family: Impact, Charcoal, sans-serif">{{ pendingTarget.share }}</span>
                <span class="responseStatus" width="40%" height="70%">
                  <i class="far fa-question-circle" v-show="pendingTarget.response==='None'" color=grey></i>
                  <i class="far fa-check-circle" v-show="pendingTarget.response==='Yes'" color=green></i>
                  <i class="far fa-times-circle" v-show="pendingTarget.response==='No'" color=red></i>
                </span>
              </div>
            </div>

            <div class="selectionButton" v-show="showPendingPropose">
              <span v-show="canMakeDecision && !hasDecided" class="yesButton" @click="acceptPropose()"></span>
              <span v-show="canMakeDecision && !hasDecided" class="noButton" @click="rejectPropose(userName)"></span>
              <span v-show="!canMakeDecision">You cannot make decision</span>
              <span v-show="hasDecided">You have decided!</span>
            </div>
          </div>
          <div class="pendingProposeTimer" v-show="showPendingPropose">
            <span class="clockIcon"><i class="far fa-clock"></i></span>
            <span class="timer">
              <span id="proposeProgress">
                <span id="proposeBar"></span>
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
//import
import Vue from 'vue'
import firebase from '@/config/firebase'
import VueChatScroll from 'vue-chat-scroll'
//Constants
const database = firebase.firestore(); //store data in firestore
//global variables
var proposeTimer
var gameBar //loading bar for game timer
var proposeBar //loading bar propose timer

Vue.use(VueChatScroll)

export default {
  name: 'GameRoom',
  props: ['uid', 'gameid', 'weight'],
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
      profitList: [],
      proposeHistory: [],
      pendingPropose: [],
      minStamina: 999,
      totalPlayerStamina: 0,
      isHistoryHidden: true,
      errorMessage: '',
      isWaitingForPLayer: true,
      gameStartTime: '',
      rank: '',
      totalNumPlayer: 0,
      isNewUi: true,
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
      // if (numPlayer === 1) {
      //   console.log('End game because of number player = 1')
      //   this.toEndGame()
      // }
      // if (this.totalPlayerStamina < this.minStamina) {
      //   console.log('End game because of inefficient stamina')
      //   this.toEndGame()
      // }
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
    numPlayerWaitingFor () {
      return this.totalNumPlayer - this.userList.length
    },
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
    isThereAnyHistory() {
      return this.proposeHistory.length > 0
    },

  },

  methods: {
    checkPropose () {
      var value = 0
      var neededStamina = 0
      var originalValue = 0
      this.profitList.forEach(profit => {
        if (profit.name === this.currentTaskName) {
          value = profit.value
          neededStamina = profit.stamina
          originalValue = value
        }
      })
      this.proposeWindowList.forEach(element => {
        if (!isNaN(element.share)) {
          value = value - Number(element.share)
          if (Number(element.share) !== 0) {
            neededStamina = neededStamina - Number(element.stamina)
          }
        }
      })
      if (value !== 0) {
        this.errorMessage = 'Incorrect share value!'
      } else if (neededStamina > 0) {
        this.errorMessage = 'Inefficient stamina!'
      } else {
        this.errorMessage = ''
        this.sendPropose(originalValue)
      }
    },
    toggleHistoryVisibility () {
      var proposeHistoryClass = document.getElementById('proposeHistoryList')
      if (proposeHistoryClass.style.visibility === 'hidden') {
        proposeHistoryClass.style.visibility = 'visible'
        this.isHistoryHidden = false
      } else {
        proposeHistoryClass.style.visibility = 'hidden'
        this.isHistoryHidden = true
      }
    },
    startGameBar () {
      console.log('game timer called')
      var elem = document.getElementById("gameBar");
      var currentTime = Number(new Date().getTime());
      var timeCreated = Number(this.gameStartTime);
      var width = 300 - Math.round(((currentTime - timeCreated)/1000));

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
      console.log('propose timer bar called')
      var elem = document.getElementById("proposeBar");
      var currentTime = Number(new Date().getTime())
      var timeCreated = Number(this.pendingPropose[0].timeCreated);
      var width = 30 - Math.round(((currentTime - timeCreated)/1000));
      console.log('currentTime:', currentTime)
      console.log('timeCreated:', timeCreated)
      proposeBar = setInterval(frame, 1000); //increase timer bar every 1 second
      function frame() {
        if (width > 0) { //30 seconds
          width--;
          elem.style.width = ((width*10)/3) + '%';
          // elem.innerHTML = width * 1;
        }
      }
    },
    async toEndGame () {
      try {
        //update user score and in game status
        await database.collection('games').doc(this.gameid).collection('users').doc(this.uid).update({
          score: this.userScore,
          status: 'outPlay'
        })

        this.$router.push(`/gameEnd/${this.userScore}/${this.uid}`)
      } catch (err) {
        console.log('Error update score:', err)
      }
    },

    async writeSuccessPropose () {
      try {
        var batch = database.batch()
        //write to propose History
        var currentTime = '' + new Date().getTime()
        batch.set(database.collection('games').doc(this.gameid).collection('proposeHistory').doc(currentTime), {
          history: this.pendingPropose,
          taskName: this.pendingPropose[0].taskName,
          result: 'Accepted',
        })
        //delete all documents in pendingPropose collection
        this.userList.forEach(user => {
          batch.delete(database.collection('games').doc(this.gameid).collection('pendingPropose').doc(user.uid))
        })
        //commit the batch
        await batch.commit()
        console.log('update, write propose History, delete pending propose success')
      } catch (err) {
        console.log('Error write success propose: ', err)
      }
    },
    async rejectPropose (nameOfRefuseOne) {
      try {
        //update the response status locally
        for (var i = 0; i < this.pendingPropose.length; i++) {
          if (this.pendingPropose[i].name === nameOfRefuseOne) {
            this.pendingPropose[i].response = 'No'
          }
        }
        var batch = database.batch()
        //write to propose History
        var currentTime = '' + new Date().getTime()
        batch.set(database.collection('games').doc(this.gameid).collection('proposeHistory').doc(currentTime), {
          history: this.pendingPropose,
          taskName: this.pendingPropose[0].taskName,
          result: 'Rejected',
        })
        //delete all documents in pendingPropose collection
        this.userList.forEach(user => {
          batch.delete(database.collection('games').doc(this.gameid).collection('pendingPropose').doc(user.uid))
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
        await database.collection('games').doc(this.gameid).collection('pendingPropose').doc(this.uid).update({
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
    async sendPropose (taskValue) {
      console.log(this.proposeWindowList)
      var pendingProposeRef = database.collection('games').doc(this.gameid).collection('pendingPropose')
      var batch = database.batch()
      var timeCreated = '' + new Date().getTime()
      this.proposeWindowList.forEach(proposeTarget => {
        if (proposeTarget.share!=='0') {
          var ref = pendingProposeRef.doc(proposeTarget.uid)
          if (proposeTarget.name === this.userName) {
            batch.set(ref, {
              name: proposeTarget.name,
              share: Number(proposeTarget.share),
              response: 'Yes',
              taskName: taskValue + '',
              uid: proposeTarget.uid,
              timeCreated: timeCreated
            })
          } else {
            batch.set(ref, {
              name: proposeTarget.name,
              share: Number(proposeTarget.share),
              response: 'None',
              taskName: taskValue + '',
              uid: proposeTarget.uid,
              timeCreated: timeCreated
            })
          }
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
          batch.set(database.collection('games').doc(this.gameid).collection('proposeHistory').doc(currentTime), {
            history: this.pendingPropose,
            taskName: this.pendingPropose[0].taskName,
            result: 'Out of Date',
          })
          //delete all documents in pendingPropose collection
          this.userList.forEach(user => {
            batch.delete(database.collection('games').doc(this.gameid).collection('pendingPropose').doc(user.uid))
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
    try {
      //set listner on the status of the assigned game
      var gameRef = database.collection('games').doc(this.gameid)
      gameRef.onSnapshot((doc) => {
        if (doc.exists) {
          if (doc.data().status === 'waiting') {
            this.isWaitingForPLayer = true;
          } else {
            this.isWaitingForPLayer = false;
            this.gameStartTime = doc.data().timeStart;
            //set time for game to end
            this.startGameBar()
            // setTimeout(() => {a
            //   console.log('End game because of time out')
            //   this.toEndGame()
            // }, 300000) //5 minutes
          }
        } else {
          console.log('game do not exists')
        }
      })
    } catch (err) {
      console.log('error gettting game info: ', err)
    }

    //get current pending propose
    var pendingProposeRef = database.collection('games').doc(this.gameid).collection('pendingPropose')
    pendingProposeRef.onSnapshot((querySnapshot) => {
      var pendingPropose = querySnapshot.docs.map(doc => ({
        name: doc.data().name,
        uid: doc.data().uid,
        share: doc.data().share,
        response: doc.data().response,
        taskName: doc.data().taskName,
        timeCreated: doc.data().timeCreated,
      }))
      try {
        this.pendingPropose = pendingPropose
        this.pendingTaskName = this.pendingPropose[0].taskName
        console.log(this.pendingPropose)
      } catch (error) {
        console.log('Error retrieving pending propose: ', error)
      }
    })

    //get profitList for the game
    try {
      var gameInfoRef = database.collection('games').doc(this.gameid)
      var doc = await gameInfoRef.get()
      if (doc.exists) {
        console.log('profit list exits');
        var thresholds = doc.data().thresholds
        var values = doc.data().values
        var weights = doc.data().weights

        this.totalNumPlayer = weights.length
        //get the actual profit list from database
        for (var i = 0; i < thresholds.length; i++) {
          this.profitList[i] = {
            name: 'Profit ' + i,
            stamina: thresholds[i],
            value: values[i],
          }
        }
        //decide the value rank of each profit
        values.sort()

        for (var i = 0; i < this.profitList.length; i++) {
          this.profitList[i].rank = values.indexOf(this.profitList[i].value)
        }

        //indentify the rank of the current player
        for (var j = 0; j < weights.length; j++) {
          var currentWeight = weights[j] + ''
          console.log(this.weight + ' vs ' + currentWeight)
          if (this.weight === currentWeight) {
            this.rank = j;
            break;
          }
        }
        console.log('Rank ',this.rank)

      } else {
        console.log('game info not exist')
      }
    } catch (err) {
      console.log('error gettting game info: ', err)
    }

    //get list of users from database, also data observer
    var usersRef = database.collection('games').doc(this.gameid).collection('users')
    usersRef.onSnapshot((querySnapshot) => {
      var users = querySnapshot.docs.map(doc => ({
        //name: doc.data().name.substring(0, doc.data().name.lastIndexOf("@"),
        name: doc.data().nickname,
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

    //get current propose History
    var proposeHistoryRef = database.collection('games').doc(this.gameid).collection('proposeHistory')
    proposeHistoryRef.onSnapshot((querySnapshot) => {
      var proposeHistory = querySnapshot.docs.map(doc => ({
        history: doc.data().history,
        taskName: doc.data().taskName,
        result: doc.data().result
      }))
      this.proposeHistory = proposeHistory
      console.log(this.proposeHistory)
    })

    //decide the userName of player based on rank
    if (this.rank === 0) {
      this.userName = 'Red Cat'
    }
    if (this.rank === 1) {
      this.userName = 'Blue Cat'
    }
    if (this.rank === 2) {
      this.userName = 'Green Cat'
    }
    if (this.rank === 3) {
      this.userName = 'Yellow Cat'
    }
    if (this.rank === 4) {
      this.userName = 'Brown Cat'
    }

    //userStamina = weight
    this.userStamina = this.weight + ''

    // try {
    //   //get info of current logged in user
    //   var userInfoRef = database.collection('games').doc(this.gameid).collection('users').doc(this.uid)
    //   var doc = await userInfoRef.get()
    //   if (doc.exists) {
    //     this.userName = doc.data().name.substring(0, doc.data().name.lastIndexOf("@"))
    //     this.userStamina = doc.data().stamina
    //   } else {
    //     console.log('user info not exist')
    //   }
    // } catch (err) {
    //   console.log('error gettting user info: ', err)
    // }
  }
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

input {
  border: transparent;
}

body::-webkit-scrollbar-thumb {
  background-color: darkgrey;
  outline: 1px solid slategrey;
}

/* start new Ui */
.catListAndFishList {
  display: flex;
  width: 100%;
  height: 65%;
  flex-direction: row;
}

.catList {
  display: flex;
  width: 25%;
  height: 100%;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.catYou {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 75%;
  height: 20%;
  background-image: url("../assets/catBox.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin: 2px;
}

.catIcon {
  width: 28%;
  height: 66%;
}

.catInfo {
  width: 55%;
  height: 66%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  margin-left: 5%;
}

.catName {
  color: white;
}

.catClimbInfo {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 75%;
}

.ladderIcon {
  width: 20%;
  background-image: url("../assets/ladderIcon.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}

.catOther {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 55%;
  height: 14.6%;
  background-image: url("../assets/catBox.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin: 2px;
}

.fishList {
  display: flex;
  width: 75%;
  height: 100%;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.fishSection {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  width: 15%;
  height: 100%;
  margin: 7px;
  transition: all .2s ease-in-out;
}

.fishSection:hover {
  transform: scale(1.1);
}

.fishSize4 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 30%;
  background-image: url("../assets/fishPlate.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
.fishSize3 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 85%;
  height: 25%;
  background-image: url("../assets/fishPlate.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
.fishSize2 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 70%;
  height: 23%;
  background-image: url("../assets/fishPlate.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
.fishSize1 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 60%;
  height: 20%;
  background-image: url("../assets/fishPlate.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
.fishSize0 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 40%;
  height: 13%;
  background-image: url("../assets/fishPlate.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
.ladderFish {
  width: 50%;
  height: 40%;
  background-image: url("../assets/ladder.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}

.clockAndProposalHistoryBox {
  display: flex;
  width: 100%;
  height: 35%;
  flex-direction: row;
}

.clock {
  display: flex;
  width: 20%;
  height: 100%;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.watch {
  width: 50%;
  height: 90%;
  background-image: url("../assets/clock.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}

.watchInfo {
  width: 50%;
  height: 90%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.currentProposalLabelBox {
  width: 10%;
  height: 65%;
  display: flex;
  flex-flow: column;
  justify-content: flex-end;
}

.currentProposalLabel {
  width: 100%;
  height: 55%;
  background-image: url("../assets/currentProposalLabel.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}

.proposalHistoryBox {
  display: flex;
  width: 90%;
  height: 100%;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.historyBox {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  width: 85%;
  height: 90%;
  background-image: url("../assets/historyBox.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}

.historyBoxName {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 25px;
  background: #333333;
  width: 95%;
  height: 10%;
  margin: 1%;
}

.historyBoxHistory {
  /* display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; */
  border-radius: 15px;
  background: #333333;
  width: 95%;
  height: 45%;
  overflow-y: scroll
}

.proposeHistoryItem {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-radius: 15px;
  background: #808080;
  width: 99%;
  height: 40%;
  margin: 0.5%;
}

.historyBoxPendingPropose {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-radius: 15px;
  background: #333333;
  width: 95%;
  height: 20%;
  margin: 0.5%;
}

.totalShare {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 15%;
  height: 100%;
}

.listOfEachShare {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 70%;
  height: 100%;
}

.eachShare {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 15%;
  height: 100%;
}

.selectionButton {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 15%;
  height: 100%;
}

.yesButton {
  background-image: url("../assets/yesButton.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  width: 40%;
  height: 90%;
  margin: 2%;
}

.noButton {
  background-image: url("../assets/noButton.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  width: 40%;
  height: 90%;
  margin: 2%;
}

.pendingProposeTimer {
  width: 95%;
  height: 5%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.timer {
  width: 95%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
/* end  new Ui */

.waitingScreen {
  display: flex;
  weight: 100%;
  height: 100%;
  flex-direction: column;
  justify-content: center;
  align-items: center;

}

.loaderSection {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width:500px;
  height:100px;
}

.messageSection {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width:500px;
  height:100px;
}

.watingMessage {
  font-size: 19px;
  color: #22b573;
  font-family: "Comic Sans MS", cursive, sans-serif;
}

.loader {
    border: 4px solid #f3f3f3; /* Light grey */
    border-top: 4px solid #22b573; /* Purple */
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

#gameProgress {
  width: 90%;
  height: 90%;
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
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
.gameTimer {
  display: flex;
  width: 100%;
  height: 33%;
  justify-content: flex-start;
  align-items: center;
}
.staminaBar {
  display: flex;
  border-radius: .3em;
  background-color: #ffa621;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 33%;
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
  width: 100%;
  height: 10%;
}
.mainUserBox {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: .3em;
  padding: 0.5rem;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
  width: 20%;
  height: 85%;
}
.avatar img {
  width: 60px;
  height: 60px;
}
.userBio {
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  margin-left: 4%;
  color: #1aaaba;
  width: 50%;
  height: 90%;
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
  height: 100%;
  width: 20%;
  display: flex;
  flex-flow: column;
  color: #ffffff;
  flex: 1 1 10%;
}
.profitList {
  color: #ffffff;
  height: 100%;
  width: 60%;
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
  width: 150px;
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
  background-color: #22b573;
  border: none;
  border-radius: .2em;
  border: solid 1px #1609;
  color: #ffffff;
}
.inputBox {
  display: flex;
  flex-flow: row;
  border-radius: .2em;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
}

.pendingPropose {
  display: flex;
  flex: 1 1 11%;
  justify-content: center;
  align-items: center;
}
.pendingProposeInfo {
  width: 80%;
  height: 100%;
  display: flex;
  flex-flow: column;
  border-radius: .2em;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
}
.taskNameAndTimer {
  width: 100%;
  height: 15%;
  display: flex;
}
.taskName {
  width: 30%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.clockIcon {
  width: 5%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #333333;
}

#proposeProgress {
  width: 100%;
  height: 70%;
  background-color: #ddd;
  display: flex;
  justify-content: flex-start;
  border-radius: .3em;
}

#proposeBar {
  width: 100%;
  height: 100%;
  background-color: #4CAF50;
  text-align: center;
  color: white;
  border-radius: .3em;
}

.infoColumns {
  width: 100%;
  height: 70%;
  display: flex;
}

.nameColumn {
  width: 31%;
  height: 100%;
  padding-left: 1%;
  padding-right: 1%;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: flex-start;
}

.shareColumn {
  width: 31%;
  height: 100%;
  padding-left: 1%;
  padding-right: 1%;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: flex-start;
}

.shareBar {
  width: 100%;
  height: 18%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: .3em;
  background-color: #ffb711;
  margin-top: 1%;
  margin-bottom: 1%;
}

.itemInColumn {
  width: 100%;
  height: 18%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-top: 1%;
  margin-bottom: 1%;
}
.responseColumn {
  width: 31%;
  height: 100%;
  padding-left: 1%;
  padding-right: 1%;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: flex-start;
}

.responseOption {
  width: 98%;
  height: 13%;
  margin: 1%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.proposeHistory {
  color: #ffffff;
  height: 100%;
  width: 20%;
  display: flex;
  /* display: none; */
  flex-flow: column;
}

#proposeHistoryList {
  display: flex;
  flex-flow: column;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
  border-radius: .3em;
  width: 100%;
  height: 94%;
  overflow-y: scroll;
  align-items: center;
  visibility: visible;

}

.proposeHistoryBar {
  display: flex;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
  border-radius: .3em;
  width: 100%;
  height: 5%;
  justify-content: center;
  align-items: center;
}

.history {
  display: flex;
  flex-flow: column;
  width: 90%;
  height: 200px;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.06);
  border: solid 1px #e0e0e0;
  border-radius: .3em;
  background-color: #ffffff;
  overflow-y: scroll;
  align-items: flex-start;
  margin: 1px;
  padding: 3px;
  color: #ffffff;
}

::-webkit-scrollbar-thumb
{
	border-radius: 10px;
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
	background-color: #d8d8d8;
}
::-webkit-scrollbar
{
	width: 12px;
	background-color: #F5F5F5;
}
::-webkit-scrollbar-track
{
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
	border-radius: 10px;
	background-color: #F5F5F5;
}

@media screen and (max-width: 531px) {
  .proposeHistory {
    display: none;
  }
  .gamePlay {
    flex-direction: column;
    justify-content: center;
    align-items: center;

  }
  .userList {
    flex-direction: row;
  }
  .profitList {
    background-color: red;
    width: 100%;
  }
  .userList {
    background-color: green;
    width: 100%;
    overflow-x: scroll;
  }
  .pendingPropose {
    background-color: purple;
  }
  .avatar img {
    width: 40px;
    height: 40px;
  }
  .mainUserBox {
    width: 90%;
  }
  .userBox {
    height: 100%;
  }

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
span {
  color: #22b573;
}
</style>
