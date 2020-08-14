import Vue from 'vue';
import axios from 'axios';
import store from '../store';

axios.defaults.withCredentials = true;

// doing something with the response
axios.interceptors.response.use(
  (response) => {
    store.commit('setLoading', false);
    return response;
  },
  (error) => {
    // all 4xx/5xx responses will end here
    let message = 'Unknown error';
    const switchError = error.status ? error.status : error.response.status;
    switch (switchError) {
      case 401:
        message = 'Invalid credentials';
        break;
      case 403:
        message = 'Unauthorized';
        break;
      case 400:
        message = 'Bad request';
        break;
      case 409:
        message = 'Entry already exist';
        break;
      default:
        message = 'Error';
    }
    if (message !== 'Error') {
      Vue.toasted.show(message, { type: 'error' });
    }
    store.commit('setLoading', false);
    return Promise.reject(error);
  },
);

export default axios;
