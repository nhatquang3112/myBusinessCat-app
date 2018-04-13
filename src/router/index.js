import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import GameStart from '@/components/GameStart'
import GameRoom from '@/components/GameRoom'
import GameEnd from '@/components/GameEnd'
import HelloWorld from '@/components/HelloWorld'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'GameStart',
      component: GameStart
    },
    {
      path: '/gameRoom/:uid/:gameid/:weight',
      name: 'GameRoom',
      component: GameRoom,
      props: true
    },
    {
      path: '/gameEnd/:score/:uid',
      name: 'GameEnd',
      component: GameEnd,
      props: true
    },
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },

  ]
})
