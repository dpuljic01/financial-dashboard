import Vue from 'vue';
import Vuex from 'vuex';
import VueAxios from 'vue-axios';
import Toasted from 'vue-toasted';
import VueCookies from 'vue-cookies';
// import {
//   MdApp,
//   MdButton,
//   MdCard,
//   MdSnackbar,
//   MdCheckbox,
//   MdContent,
//   MdDrawer,
//   MdEmptyState,
//   MdField,
//   MdIcon,
//   MdLayout,
//   MdList,
//   MdMenu,
//   MdProgress,
//   MdTabs,
//   MdToolbar,
// } from 'vue-material/dist/components';
import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

import App from './App.vue';
import router from './router';
import store from './store';
import axios from './plugins/axios';
import './theme.scss';

Vue.config.productionTip = false;
Vue.use(Vuex);
Vue.use(VueAxios, axios);
Vue.use(VueMaterial);
Vue.use(VueCookies);
// Vue.use(MdApp);
// Vue.use(MdLayout);
// Vue.use(MdButton);
// Vue.use(MdCheckbox);
// Vue.use(MdContent);
// Vue.use(MdCard);
// Vue.use(MdSnackbar);
// Vue.use(MdDrawer);
// Vue.use(MdEmptyState);
// Vue.use(MdField);
// Vue.use(MdTabs);
// Vue.use(MdIcon);
// Vue.use(MdMenu);
// Vue.use(MdProgress);
// Vue.use(MdList);
// Vue.use(MdToolbar);
Vue.use(Toasted, { duration: 4000, theme: 'bubble', type: 'success' });

new Vue({ // eslint-disable-line no-new
  el: '#app',
  router,
  store,
  render: (h) => h(App),
});
