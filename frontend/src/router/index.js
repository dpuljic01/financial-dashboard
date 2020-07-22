import Vue from 'vue';
import Router from 'vue-router';
import Courses from '../components/Courses.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Courses',
      component: Courses,
    },
  ],
});
