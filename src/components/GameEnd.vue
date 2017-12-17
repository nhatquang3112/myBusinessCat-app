<template>
  <div class="gameend">
  <h1>Game Over!</h1>
  <router-link to = "/">Restart</router-link>
  </div>
</template>

<script>
export default {
  name: 'GameStart',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
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
