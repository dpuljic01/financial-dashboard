import Vue from 'vue';
import Router from 'vue-router';
import Navigation from '../components/Navigation.vue';
import NotFound from '../components/NotFound.vue';
import showcase from '../components/Showcase.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/showcase',
      name: 'showcase',
      component: showcase,
    },
    {
      path: '/home',
      name: 'navigation',
      component: Navigation,
    },
    {
      path: '/',
      redirect: { name: 'showcase' },
    },
    {
      path: '*',
      component: NotFound,
    },
  ],
});
