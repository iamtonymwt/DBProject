<template>
  <!-- <div id="app"> -->
    <router-view></router-view>
  <!-- </div> -->
</template>

<script>
import Register from './components/Register.vue'
import Login from './components/Login.vue'
import Home from './components/Home.vue'
export default {
  name: 'App',
  components: {
    Home,
    Register,
    Login,
  } 
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
