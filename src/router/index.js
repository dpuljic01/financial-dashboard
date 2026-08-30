import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import { PUBLIC_ROUTES, PROTECTED_ROUTES } from '../consts';

// Route components are lazy-loaded (dynamic import) instead of bundled
// into one file - previously every page's code (plus lightweight-charts,
// chart.js, moment...) shipped in a single ~1.8MB bundle that had to be
// downloaded before ANY page could render, even the login screen.
// webpackChunkName groups pages that are always navigated together (a
// portfolio's own tabs, the auth pages) into one chunk, so switching
// between them doesn't cost an extra round trip.
const Landing = () => import(/* webpackChunkName: "landing" */ '../components/Landing.vue');
const Dashboard = () => import(/* webpackChunkName: "dashboard" */ '../components/Dashboard.vue');
const Login = () => import(/* webpackChunkName: "auth" */ '../components/Login.vue');
const Register = () => import(/* webpackChunkName: "auth" */ '../components/Register.vue');
const ResetPassword = () => import(/* webpackChunkName: "auth" */ '../components/ResetPassword.vue');
const MyPortfolios = () => import(/* webpackChunkName: "portfolio" */ '../components/MyPortfolios.vue');
const Portfolio = () => import(/* webpackChunkName: "portfolio" */ '../components/Portfolio.vue');
const Holdings = () => import(/* webpackChunkName: "portfolio" */ '../components/portfolio/Holdings.vue');
const Summary = () => import(/* webpackChunkName: "portfolio" */ '../components/portfolio/Summary.vue');
const News = () => import(/* webpackChunkName: "portfolio" */ '../components/portfolio/News.vue');
const Performance = () => import(/* webpackChunkName: "portfolio" */ '../components/portfolio/Performance.vue');
const Quote = () => import(/* webpackChunkName: "quote" */ '../components/Quote.vue');
const Compare = () => import(/* webpackChunkName: "compare" */ '../components/Compare.vue');
const Profile = () => import(/* webpackChunkName: "profile" */ '../components/Profile.vue');
const NotFound = () => import(/* webpackChunkName: "misc" */ '../components/NotFound.vue');

const router = createRouter({
  history: createWebHistory('/'),
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
        {
          name: 'Performance',
          path: 'performance',
          component: Performance,
        },
      ],
    },
    {
      path: '/quote/:quote',
      name: 'Quote',
      component: Quote,
      children: [
        {
          // Quote.vue renders the profile/news tabs itself (no nested
          // <router-view>) - these children only exist so vue-router
          // matches /quote/:quote/profile and /quote/:quote/news.
          name: 'QuoteProfile',
          path: 'profile',
          component: Quote,
        },
        {
          name: 'QuoteNews',
          path: 'news',
          component: Quote,
        },
      ],
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
      path: '/:pathMatch(.*)*',
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
