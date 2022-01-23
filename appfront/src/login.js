import Vue from 'vue'
import login from './login.vue'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#login',
  render: h => h(login)
})
