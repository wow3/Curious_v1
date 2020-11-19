import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import {InfiniteScroll} from 'element-ui'
import VCharts from 'v-charts'


import './assets/css/global.css'

Vue.config.productionTip = false

Vue.use(ElementUI);
Vue.use(InfiniteScroll);
Vue.use(VCharts)

Vue.prototype.$http = axios

// 每个Vue实例可以用$http调用axios

axios.defaults.baseURL = 'http://127.0.0.1:5000/'
// axios.interceptors.request.use(config => {
//   config.headers.Authorizatioin = localStorage.getItem('token');
//   return config;
// })
axios.defaults.withCredentials=true;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
