import Vue from 'vue';
import Vuex from 'vuex';
import VueAxios from 'vue-axios';
import Toasted from 'vue-toasted';
import VueCookies from 'vue-cookies';
import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

import App from './App.vue';
import router from './router';
import store from './store';
import axios from './plugins/axios';
import Navigation from './components/Navigation.vue';
import './assets/theme.scss';

Vue.config.productionTip = false;
Vue.use(Vuex);
Vue.use(VueAxios, axios);
Vue.use(VueMaterial);
Vue.use(VueCookies);
Vue.use(Toasted, {
  router,
  duration: 5000,
  type: 'success',
});
Vue.component('navigation', Navigation);

new Vue({ // eslint-disable-line no-new
  el: '#app',
  router,
  store,
  render: (h) => h(App),
});
