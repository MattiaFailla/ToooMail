import Vue from 'vue'
import App from './App.vue'
import router from './router'

// handling cookies
import VueCookies from 'vue-cookies';
Vue.use(VueCookies);

Vue.config.productionTip = false

import Toasted from 'vue-toasted';

Vue.use(Toasted)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
