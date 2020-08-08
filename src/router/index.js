import Vue from 'vue';
import Router from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import NotFound from '../components/NotFound.vue';
import Landing from '../components/Landing.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import ResetPassword from '../components/ResetPassword.vue';
import Portfolio from '../components/Portfolio.vue';
import Notifications from '../components/Notifications.vue';
import Settings from '../components/Settings.vue';
import store from '../store';
import { PUBLIC_ROUTES, PROTECTED_ROUTES } from '../consts';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      redirect: {
        path: '/landing',
      },
    },
    {
      path: '/landing',
      name: 'Landing',
      component: Landing,
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      props: { title: 'Dashboard' },
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      props: { title: 'Dashboard' },
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      props: { title: 'Dashboard' },
    },
    {
      path: '/portfolio',
      name: 'Portfolio',
      component: Portfolio,
      props: { title: 'Portfolio' },
    },
    {
      path: '/notifications',
      name: 'Notifications',
      component: Notifications,
      props: { title: 'Notifications' },
    },
    {
      path: '/settings',
      name: 'Settings',
      component: Settings,
      props: { title: 'Settings' },
    },
    {
      path: '/reset/:passwordToken',
      name: 'ResetPassword',
      component: ResetPassword,
    },
    {
      path: '*',
      component: NotFound,
    },
  ],
});

router.beforeEach((to, from, next) => {
  // if the user is logged in and tries to access login/register pages, return him to dashboard
  // if the user is just coming to the site it will redirect him to /landing
  // if the user is not logged in and tries to access protected route (e.g dashboard), redirect him to /login
  // in every other case take him to the path he requested
  if (!store.getters.isAuthenticated) {
    if (PROTECTED_ROUTES.includes(to.name)) {
      next('/login');
    } else {
      next();
    }
  } else if (PUBLIC_ROUTES.includes(to.name)) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
