<template>
  <div class="gameend">
    <h1>Game Over!</h1>
    <h2>Your score is {{ score }}!</h2>

    <button @click="playAgain()">Play Again</button>
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
