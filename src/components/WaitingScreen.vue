<template>
  <div class="waitingScreen" v-show="isWaiting" v-model='numPlayers'>

    <div class="loaderSection">
      <span class="loader"></span>
    </div>

    <img src="../assets/LoadingCat.png"
    width="250px"
    alt="Avatar"/>

    <div class="messageSection">
      <span class="watingMessage">
        Waiting for {{ numPlayers }} more to do business
      </span>
      <span class="watingMessage">
        Please be patient, meow
      </span>
    </div>


  </div>
</template>
<script>
   export default{
       props:['isWaiting', 'numPlayers']
   }
</script>
<style scoped>

</style>
