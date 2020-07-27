// src/store/index.js

import Vue from 'vue';
import Vuex from 'vuex';
import { fetchPortoflios, fetchPortoflio } from '../api';

Vue.use(Vuex);

const state = {
  // single source of data
  portfolios: [],
};

const actions = {
  // asynchronous operations
  loadPortoflios(context) {
    return fetchPortoflios().then(response => {
      context.commit('setPortfolios', { portfolios: response.data });
    });
  },
  loadPortfolio(context, { id }) {
    return fetchPortoflio(id).then(response => {
      context.commit('setPortfolio', { portfolio: response.data });
    });
  },
};

const mutations = {
  // isolated data mutations
};

const getters = {
  // reusable data accessors
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
