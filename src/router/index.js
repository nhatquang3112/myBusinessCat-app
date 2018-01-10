import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import GameStart from '@/components/GameStart'
import GameRoom from '@/components/GameRoom'
import GameEnd from '@/components/GameEnd'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'GameStart',
      component: GameStart
    },
    {
      path: '/gameRoom',
      name: 'GameRoom',
      component: GameRoom
    },
    {
      path: '/gameEnd',
      name: 'GameEnd',
      component: GameEnd
    },
    // {
    //   path: '/',
    //   name: 'HelloWorld',
    //   component: HelloWorld
    // },

  ]
})
