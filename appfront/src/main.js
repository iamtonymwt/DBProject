// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App'
import router from './router/index.js'
import store from './store/index.js'
import VChars from 'v-charts'
import  qs from 'qs'

var axios = require('axios')
axios.defaults.baseURL = 'http://localhost:8000/'
// 全局注册，之后可在其他组件中通过 this.$axios 发送数据
Vue.prototype.$axios = axios
Vue.config.productionTip = false
Vue.prototype.$qs = qs

Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.use(VChars);

/* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   store,
//   components: { App },
//   template: '<App/>'
// })

var date = new Date()
Vue.prototype.getMyTime = function () {
  return (date.getFullYear() + "-" +
      ((date.getMonth() + 1 >= 10) ? (date.getMonth() + 1) : ("0" + (date.getMonth() + 1))) + "-" +
      ((date.getDate() >= 10) ? (date.getDate()) : ("0" + date.getDate())) + " " +
      ((date.getHours() >= 10) ? (date.getHours()) : ("0" + date.getHours())) + ":" +
      ((date.getMonth() >= 10) ? (date.getMonth()) : ("0" + date.getMonth())) + ":" +
      ((date.getSeconds() >= 10) ? (date.getSeconds()) : ("0" + date.getSeconds())))
}

new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
  components: { App },
  template: '<App/>',
}).$mount('#app')
