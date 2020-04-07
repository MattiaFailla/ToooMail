import Vue from 'vue'
import App from './App.vue'
import router from './router'

// importing UI
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);

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
