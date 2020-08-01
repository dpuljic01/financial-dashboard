import Vue from 'vue';
import Router from 'vue-router';
import Home from '../components/Home.vue';
import NotFound from '../components/NotFound.vue';
import Landing from '../components/Landing.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import ResetPassword from '../components/ResetPassword.vue';
import store from '../store';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      redirect: {
        path: '/home',
      },
    },
    {
      path: '/landing',
      name: 'Landing',
      component: Landing,
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
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
  const openRoutes = ['Login', 'Register', 'Landing', 'ResetPassword'];
  const protectedRoutes = ['Home'];

  // if the user is logged in and tries to access login/register pages, return him to home
  if (store.getters.isAuthenticated && openRoutes.includes(to.name)) {
    next('/home');
  }

  if (protectedRoutes.includes(to.name) && !store.getters.isAuthenticated) {
    next('/login');
  }
  next();
});

export default router;
