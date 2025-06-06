import { createApp } from 'vue';
import VueAxios from 'vue-axios';
import Toasted from 'vue-toasted';
import VueCookies from 'vue-cookies';
import VueMaterial from 'vue-material';
import VueApexCharts from 'vue3-apexcharts';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';
import FloatingVue from 'floating-vue';
import 'floating-vue/dist/style.css';

import App from './App.vue';
import router from './router';
import store from './store';
import axios from './plugins/axios';
import Navigation from './components/Navigation.vue';
import './assets/theme.scss';

const app = createApp(App);
app.use(FloatingVue);
app.use(VueAxios, axios);
app.use(VueApexCharts);
app.use(VueMaterial);
app.use(VueCookies);
app.use(Toasted, {
  router,
  duration: 5000,
  type: 'success',
});
app.use(store);
app.use(router);
app.component('navigation', Navigation);
app.component('apexchart', VueApexCharts);
app.mount('#app');
