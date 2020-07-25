import Navigation from './components/Navigation.vue';
import showcase from './components/Showcase.vue';

/**
 * You can register global components here and use them as a plugin in your main Vue instance
 */

const GlobalComponents = {
  install(Vue) {
    Vue.component('navigation', Navigation);
    Vue.component('showcase', showcase);
  },
};

export default GlobalComponents;
