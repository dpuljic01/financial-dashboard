import Vue from 'vue';
import Vuex from 'vuex';
import VueToast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-default.css';
import {
  MdApp,
  MdButton,
  MdContent,
  MdDrawer,
  MdEmptyState,
  MdTabs,
  MdIcon,
  MdMenu,
  MdList,
  MdToolbar,
} from 'vue-material/dist/components';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/black-green-light.css';

import App from './App.vue';
import router from './router';
import GlobalComponents from './globalComponents';

Vue.config.productionTip = false;
Vue.use(GlobalComponents);
Vue.use(Vuex);
Vue.use(MdApp);
Vue.use(MdButton);
Vue.use(MdContent);
Vue.use(MdDrawer);
Vue.use(MdEmptyState);
Vue.use(MdTabs);
Vue.use(MdIcon);
Vue.use(MdMenu);
Vue.use(MdList);
Vue.use(MdToolbar);
Vue.use(VueToast);

new Vue({ // eslint-disable-line no-new
  el: '#app',
  router,
  render: (h) => h(App),
});
