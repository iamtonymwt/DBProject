import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/components/home/Home.vue'
import Mainpage from "@/components/home/MainPage";
import Header from "@/components/home/Header";
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Map from '@/components/Map.vue'
import UserCenter from '@/components/user/UserCenter.vue'
import hotel from '@/components/hotel/hotel.vue'
import LeaveMessage from '@/components/hotel/LeaveMessage.vue'
import ReplyMessage from '@/components/hotel/ReplyMessage.vue'
import Message from '@/components/hotel/Message.vue'
import Graph from '@/components/hotel/Graph.vue'
import Commodities from '@/components/home/Hotel.vue'
import RankAll from '@/components/home/SideMenu.vue'

/*懒加载方式，当路由被访问的时候才加载对应的组件*/
/*const Login = resolve => require(['@/components/Login'], resolve)*/

Vue.use(Router)//注册vue-router

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register
    },
    {
      path: '/Map',
      name: 'map',
      component: Map
    },
    {
      path: '/home', name: 'Home', component: Home, redirect: '/mainpage',
      children: [
        { path: '/header', name: 'Header', component: Header, meta: { requireAuto: false } },
        { path: '/mainpage', name: 'MainPage', component: Mainpage, meta: { requireAuto: false, title: '酒店信息网' } },
        //{path:'/recommend',name:'Recommend',component:Recommend, meta: {requireAuto: false}},
        {path:'/rankAll', name:'rankAll',component:RankAll, meta:{requireAuto: false}},
        {path:'/hotels', name:'Hotels', component:Commodities, meta:{requireAuto: false}},
        { path: '/userCenter', name: 'UserCenter', component: UserCenter, meta: { requireAuto: false } }
      ]
    },

    {
      path: '/HotelInfo', name: 'HotelInfo', component: hotel, meta: { requireAuto: false, title: '酒店详细信息' },
      children: [
        {
          path: '/message', name: 'Message', component: Message, meta: { requireAuto: false },
          children: [
            // { path: 'leavemessage', name: 'LeaveMessage', component: LeaveMessage, meta: { requireAuto: false } },
            // { path: 'replymessage', name: 'ReplyMessage', component: ReplyMessage, meta: { requireAuto: false } },
            // { path: '/graph', name: 'Graph', component: Graph, meta: { requireAuto: false } },
          ]
        },

      ]
    },
  ]
})