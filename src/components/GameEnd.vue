<template>
  <div class="gameEnd">
    <span style="color: #000000; font-size: 3.5vw; font-family: Impact, Charcoal, sans-serif">Game Over!</span>
    <div class="catIcon">
      <span style="color: #6D4620; font-size: 3.5vw; font-family: Impact, Charcoal, sans-serif; margin-bottom: 10px">{{ score }}</span>
    </div>
    <span style="color: #000000; font-size: 1.5vw; font-family: Impact, Charcoal, sans-serif">Your fish score is {{ score }}</span>
    <span class="playAgainButton" @click="playAgain()"></span>
    <div class="loaderSection">
      <span class="loader"></span>
    </div>
  </div>
</template>

<script>
import GamesServices from '@/services/GamesServices'

export default {
  name: 'GameEnd',
  props: ['score', 'uid'],
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      gameid: '',
      weight: '',
    }
  },

  methods: {
    toGameRoom () {
      this.$router.push(`/gameRoom/${this.uid}/${this.gameid}/${this.weight}`)
    },
    async playAgain () {
      document.getElementsByClassName('loaderSection')[0].style.visibility = 'visible';
      const response = await GamesServices.fetchPosts(this.uid)
      this.gameid = response.data.gameid
      this.weight = response.data.weight
      this.toGameRoom();
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loader {
  border: 4px solid #f3f3f3; /* Light grey */
  border-top: 4px solid #609; /* Blue */
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 2s linear infinite;
}

.loaderSection {
  visibility: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.gameEnd {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
}

.playAgainButton {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 150px;
  height: 60px;
  background-image: url("../assets/playAgainButton.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin-top: 50px;
  margin-bottom: 10px;
}

.catIcon {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  width: 220px;
  height: 300px;
  background-image: url("../assets/gameOverCatIcon.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  margin-top: 50px;
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
