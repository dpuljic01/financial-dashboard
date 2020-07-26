import Vue from 'vue';
import Router from 'vue-router';
import home from '../components/Home.vue';
import notfound from '../components/NotFound.vue';
import showcase from '../components/Showcase.vue';
import login from '../components/Login.vue';
import register from '../components/Register.vue';

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
      name: 'home',
      component: home,
    },
    {
      path: '/',
      redirect: {
        name: 'showcase',
      },
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/register',
      name: 'register',
      component: register,
    },
    {
      path: '*',
      component: notfound,
    },
  ],
});
