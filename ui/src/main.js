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

Vue.filter('date', function(value){
  if (!value) { return value; }
  value = new Date(value);
  if (!(value instanceof Date) || isNaN(value)) { return value; }
  return ((value.getDate() < 10) ? '0' : '') + value.getDate() + '/' + ((value.getMonth() < 9) ? '0' : '') + (value.getMonth() + 1) + '/' +
      value.getFullYear();
});

Vue.filter('datetime', function(value){
  if (!value) { return value; }
  value = new Date(value);
  if (!(Object.prototype.toString.call(value) === '[object Date]')) { return value; }
  if (isNaN(value)) { return value; }
  return ((value.getDate() < 10) ? '0' : '') + value.getDate() + '/' + ((value.getMonth() < 9) ? '0' : '') + (value.getMonth() + 1) + '/' +
      value.getFullYear() + ' ' + value.getHours() + ':' + value.getMinutes()+((value.getMinutes() < 10) ? '0' : '');
});

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
