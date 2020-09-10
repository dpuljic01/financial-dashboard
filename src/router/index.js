import Vue from 'vue';
import Router from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import NotFound from '../components/NotFound.vue';
import Landing from '../components/Landing.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import ResetPassword from '../components/ResetPassword.vue';
import MyPortfolios from '../components/MyPortfolios.vue';
import Portfolio from '../components/Portfolio.vue';
import Holdings from '../components/portfolio/Holdings.vue';
import Summary from '../components/portfolio/Summary.vue';
import News from '../components/portfolio/News.vue';
import Quote from '../components/Quote.vue';
import Compare from '../components/Compare.vue';
import Profile from '../components/Profile.vue';
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
    },
    {
      path: '/portfolios',
      name: 'Portfolios',
      component: MyPortfolios,
    },
    {
      path: '/portfolios/:portfolioId',
      name: 'Portfolio',
      component: Portfolio,
      children: [
        {
          name: 'Holdings',
          path: 'holdings',
          component: Holdings,
        },
        {
          name: 'Summary',
          path: 'summary',
          component: Summary,
        },
        {
          name: 'News',
          path: 'news',
          component: News,
        },
      ],
    },
    {
      path: '/quote/:quote',
      name: 'Quote',
      component: Quote,
    },
    {
      path: '/compare',
      name: 'Compare',
      component: Compare,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
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
