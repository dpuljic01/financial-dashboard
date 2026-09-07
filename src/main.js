import { createApp, configureCompat } from 'vue';
import VueAxios from 'vue-axios';
import VueCookies from 'vue-cookies';
import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.min.css';
import FloatingVue from 'floating-vue';
import 'floating-vue/dist/style.css';
import 'vue-sonner/style.css';

import App from './App.vue';
import router from './router';
import store from './store';
import axios from './plugins/axios';
import Navigation from './components/Navigation.vue';
// Precompiled by `npm run build:theme` (see package.json) rather than
// imported as .scss - see that script for why.
import './assets/theme.css';

// vue-material was built for Vue 2 and is unmaintained - it relies on
// several legacy APIs that the Vue 3 compat build still supports (per this
// app's global MODE: 3 compat config, see vue.config.js) but logs a
// deprecation warning for on every render. The behavior these flags control
// is unchanged either way; this only silences the console noise. A handful
// of other vue-material warnings (e.g. "Property 'attrs' was accessed...")
// aren't compat deprecation flags at all - just how the library's Options
// API components are structured - so there's no config switch for those;
// fixing them for real would mean patching or replacing vue-material.
configureCompat({
  WATCH_ARRAY: 'suppress-warning',
  COMPONENT_V_MODEL: 'suppress-warning',
  RENDER_FUNCTION: 'suppress-warning',
  INSTANCE_SCOPED_SLOTS: 'suppress-warning',
  INSTANCE_LISTENERS: 'suppress-warning',
  OPTIONS_BEFORE_DESTROY: 'suppress-warning',
  // vue-material bootstraps its own internal Vue 2-style app context
  // (calls the Vue2()/createCompatApp global mount API, reads Vue.util,
  // reads Vue.prototype) as part of installing itself - none of that is our
  // code calling deprecated APIs, just the library's own install step.
  GLOBAL_MOUNT: 'suppress-warning',
  GLOBAL_PRIVATE_UTIL: 'suppress-warning',
  GLOBAL_PROTOTYPE: 'suppress-warning',
});

const app = createApp(App);
app.use(FloatingVue);
app.use(VueAxios, axios);
app.use(VueMaterial);
app.use(VueCookies);
app.use(store);
app.use(router);
app.component('navigation', Navigation);
app.mount('#app');
