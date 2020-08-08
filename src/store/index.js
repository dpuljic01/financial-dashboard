import Vue from 'vue';
import Vuex from 'vuex';
import * as api from '../api';
import { isValidJwt } from '../utils';
import { getCookie, setCookie, removeCookie } from '../utils/cookie';
import { AUTH_COOKIE_NAME } from '../consts';

Vue.use(Vuex);

// eslint-disable-next-line
const getDefaultState = function() {
  return {
    // single source of data
    portfolios: localStorage.getItem('_portfolios') || [],
    currentPortfolio: localStorage.getItem('_portfolio') || {},
    userData: {},
    remember: false,
    loggedIn: false,
    loading: false,
    jwt: {
      access_token: getCookie(AUTH_COOKIE_NAME) || null,
    },
    shouldRefresh: false,
  };
};

const state = getDefaultState();

const actions = {
  // asynchronous operations
  loadPortfolios(context) {
    return api.fetchPortfolios(context.state.jwt.access_token).then((response) => {
      context.commit('setPortfolios', { portfolios: response.data });
    });
  },
  loadPortfolio(context, id) {
    return api.fetchPortfolio(id, context.state.jwt.access_token).then((response) => {
      context.commit('setPortfolio', { portfolio: response.data });
    });
  },
  login(context, userData) {
    return api.login(userData)
      .then((response) => {
        context.commit('setJwtToken', { jwt: response.data });
        if (state.remember) {
          setCookie(AUTH_COOKIE_NAME, state.jwt.access_token, '30d');
        } else {
          setCookie(AUTH_COOKIE_NAME, state.jwt.access_token);
        }
        state.loggedIn = true;
      })
      .catch(() => {
        context.commit('resetState');
      });
  },
  getCurrentUser(context) {
    return api.getUser(state.jwt.access_token).then((response) => {
      context.commit('setUserData', { user: response.data });
    });
  },
  logout(context) {
    return api.logout(context.state.jwt.access_token)
      .then(() => {
        context.commit('resetState');
      })
      .catch(() => {
        context.commit('resetState');
      }); // clear cookies even if it fails, then they will be logged out anyway
  },
  register(context, userData) {
    context.commit('setUserData', { userData });
    return api.register(userData).then(() => {
      Vue.toasted.show('Check your email to finish setting up your account.', { type: 'success' });
    });
  },
  resetPassword(context, payload) {
    return api.resetPassword(payload).then(() => {
      Vue.toasted.show('Check your email to set up a new password', { type: 'success' });
    });
  },
  changePassword(context, payload) {
    return api.changePassword(payload).then(() => {
      context.commit('resetState');
      Vue.toasted.show('You can now log in');
    });
  },
  submitNewPortfolio(context, portfolio) {
    return api.createNewPortfolio(portfolio, context.state.jwt.access_token).then(() => {
      context.dispatch('successMessage');
    });
  },
  getStockHistoryData(context, params) {
    return api.getStockHistoryData(params, context.state.jwt.access_token);
  },
  search(context, params) {
    return api.search(params, context.state.jwt.access_token);
  },
  resetState(context) {
    context.commit('resetState');
  },
  successMessage(context, message = 'Saved') {
    Vue.toasted.show(message, { type: 'success', duration: 1500 });
  },
  errorMessage(context, message = "Something's wrong") {
    Vue.toasted.show(message, { type: 'error', duration: 1500 });
  },
};

const mutations = {
  // isolated data mutations
  setPortfolios(state, payload) {
    state.portfolios = payload.portfolios;
  },
  setCurrentPortfolio(state, payload) {
    state.currentPortfolio = payload.portfolio;
  },
  setUserData(state, payload) {
    state.userData = payload.user;
  },
  setJwtToken(state, payload) {
    state.jwt = payload.jwt;
  },
  resetState(state) {
    localStorage.clear();
    removeCookie(AUTH_COOKIE_NAME);
    Object.assign(state, getDefaultState());
  },
};

const getters = {
  // reusable data accessors
  isAuthenticated(state) {
    return isValidJwt(state.jwt.access_token);
  },
  hasPortfolio(state) {
    return state.portfolios.length > 0;
  },
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
