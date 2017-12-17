import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import GameStart from '@/components/GameStart'
import GamePlay from '@/components/GamePlay'
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
      path: '/gameplay',
      name: 'GamePlay',
      component: GamePlay
    },
    {
      path: '/gameend',
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
