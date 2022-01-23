# Note

通过vuex中store的全局变量和一系列封装好的函数(commit、dispatch...)更新用户信息

在`main.js`中注册`import store from './store/index.js'`， 此后其他组件的`<script>`中可以通过`this.$store`进行访问

在其中设置的`mutations:`方法需要通过commit进行调用