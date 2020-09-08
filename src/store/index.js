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
    userData: JSON.parse(localStorage.getItem('_currentUser')) || {},
    portfolios: JSON.parse(localStorage.getItem('_portfolios')) || [],
    currentPortfolio: JSON.parse(localStorage.getItem('_currentPortfolio')) || {},
    searchedSymbol: null,
    remember: false,
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
  getPortfolios(context) {
    return api.getPortfolios(context.state.jwt.access_token).then((response) => {
      context.commit('setPortfolios', { portfolios: response.data });
    });
  },
  getPortfolio(context, identifier) {
    return api.getPortfolio(identifier, context.state.jwt.access_token).then((response) => {
      context.commit('setPortfolio', { portfolio: response.data });
    });
  },
  login(context, userData) {
    return api
      .login(userData.payload)
      .then((response) => {
        context.commit('setJwtToken', { jwt: response.data });
        if (userData.remember) {
          setCookie(AUTH_COOKIE_NAME, state.jwt.access_token, '30d');
        } else {
          setCookie(AUTH_COOKIE_NAME, state.jwt.access_token);
        }
        state.loggedIn = true;
      })
      .catch(() => {
        context.commit('resetState');
        state.loggedIn = false;
      });
  },
  getCurrentUser(context) {
    return api.getUser(state.jwt.access_token).then((response) => {
      context.commit('setUserData', { user: response.data });
    });
  },
  logout(context) {
    return api
      .logout(context.state.jwt.access_token)
      .then(() => {
        context.commit('resetState');
      })
      .catch(() => {
        context.commit('resetState');
      }); // clear cookies even if it fails, then they will be logged out anyway
  },
  register(context, userData) {
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
  createNewHolding(context, data) {
    return api.createNewHolding(data, context.state.jwt.access_token).then(() => {
      context.dispatch('successMessage');
    });
  },
  getStockHistoryData(context, params) {
    return api.getStockHistoryData(params, context.state.jwt.access_token);
  },
  search(context, params) {
    return api.search(params, context.state.jwt.access_token);
  },
  addSymbol(context, payload) {
    return api.addSymbol(payload, context.state.jwt.access_token).then(() => {
      context.dispatch('getCurrentUser');
    });
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
  getLatestStockPrices(context, params) {
    return api.getLatestStockPrices(params, context.state.jwt.access_token);
  },
  getNews(context, params) {
    return api.getNews(params, context.state.jwt.access_token);
  },
};

const mutations = {
  // isolated data mutations
  setPortfolios(state, payload) {
    // localStorage.setItem('_portfolios', JSON.stringify(payload.portfolios));
    state.portfolios = payload.portfolios;
  },
  setPortfolio(state, payload) {
    // localStorage.setItem('_currentPortfolio', JSON.stringify(payload.portfolio));
    state.currentPortfolio = payload.portfolio;
  },
  setUserData(state, payload) {
    // localStorage.setItem('_currentUser', JSON.stringify(payload.user));
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
  setLoading(state, bool) {
    state.loading = bool;
  },
};

const getters = {
  // reusable data accessors
  isAuthenticated(state) {
    return isValidJwt(state.jwt.access_token);
  },
  getCurrentUser(state) {
    return state.userData;
  },
  hasPortfolio(state) {
    return state.portfolios.length > 0;
  },
  listPortfolios(state) {
    if (!state.portfolios.length > 0) {
      return [];
    }
    return state.portfolios;
  },
  currentPortfolio(state) {
    return state.currentPortfolio;
  },
  hasHoldings(state) {
    const { holdings } = state.currentPortfolio.holdings;
    return holdings && holdings.length > 0;
  },
  searchedSymbol(state) {
    return state.searchedSymbol;
  },
  isLoading(state) {
    return state.loading;
  },
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
