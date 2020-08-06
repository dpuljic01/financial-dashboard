import Vue from 'vue';
import Vuex from 'vuex';
import {
  fetchPortoflios,
  fetchPortoflio,
  createNewPortfolio,
  login,
  register,
  logout,
  resetPassword,
  changePassword,
  getStockHistoryData,
} from '../api';
import { isValidJwt } from '../utils';
import { getCookie, setCookie } from '../utils/cookie';
import AUTH_COOKIE_NAME from '../consts';

Vue.use(Vuex);

const getDefaultState = function () {
  return {
    // single source of data
    portfolios: [],
    currentPortfolio: {},
    userData: {},
    remember: false,
    loggedIn: false,
    loading: false,
    jwt: {
      access_token: getCookie(AUTH_COOKIE_NAME) || null,
    },
    confirmed: false,
  };
};

const state = getDefaultState();

const actions = {
  // asynchronous operations
  loadPortoflios(context) {
    return fetchPortoflios().then((response) => {
      context.commit('setPortfolios', { portfolios: response.data });
    });
  },
  loadPortfolio(context, { id }) {
    return fetchPortoflio(id).then((response) => {
      context.commit('setPortfolio', { portfolio: response.data });
    });
  },
  login(context, userData) {
    state.userData = userData;
    context.commit('setUserData', { userData });
    return login(userData)
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
  logout(context) {
    return logout(context.state.jwt.access_token)
      .then(() => {
        context.commit('resetState');
      })
      .catch(() => {
        context.commit('resetState');
      }); // clear cookies even if it fails, then they will be logged out anyway
  },
  register(context, userData) {
    context.commit('setUserData', { userData });
    return register(userData).then(() => {
      Vue.toasted.show('Check your email to finish setting up your account.', { type: 'success' });
    });
  },
  resetPassword(context, payload) {
    return resetPassword(payload).then(() => {
      Vue.toasted.show('Check your email to set up a new password', { type: 'success' });
    });
  },
  changePassword(context, payload) {
    return changePassword(payload).then(() => {
      context.commit('resetState');
      Vue.toasted.show('You can now log in');
    });
  },
  submitNewPortfolio(context, portfolio) {
    return createNewPortfolio(portfolio, context.state.jwt.access_token);
  },
  getStockHistoryData(context, params) {
    return getStockHistoryData(params, context.state.jwt.access_token);
  },
};

const mutations = {
  // isolated data mutations
  setPortfolios(state, payload) {
    state.portfolios = payload.portfolios;
  },
  setUserData(state, payload) {
    state.userData = payload.userData;
  },
  setJwtToken(state, payload) {
    state.jwt = payload.jwt;
  },
  resetState(state) {
    // Merge rather than replace so we don't lose observers
    Object.assign(state, getDefaultState());
  },
};

const getters = {
  // reusable data accessors
  isAuthenticated(state) {
    return isValidJwt(state.jwt.access_token);
  },
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
