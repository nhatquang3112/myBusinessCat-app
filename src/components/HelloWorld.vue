<template>
  <div class="hello-vue">
  <p><strong>{{ gameid }}</strong></p>


</div>
</template>

<script>
import GamesServices from '@/services/GamesServices'
export default {
  name: 'game',
  data () {
    return {
      gameid: []
    }
  },
  mounted () {
    this.getPosts()
  },
  methods: {
    async getPosts () {
      const response = await GamesServices.fetchPosts('9')
      this.gameid = response.data
    }
  }
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
