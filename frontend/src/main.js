import Vue from 'vue';
import Vuex from 'vuex';
import VueToast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-default.css';
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
import GlobalComponents from './globalComponents';
import './theme.scss';

Vue.config.productionTip = false;
Vue.use(GlobalComponents);
Vue.use(Vuex);
Vue.use(VueMaterial);
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
Vue.use(VueToast);

new Vue({ // eslint-disable-line no-new
  el: '#app',
  router,
  store,
  render: (h) => h(App),
});
