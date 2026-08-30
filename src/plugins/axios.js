import axios from 'axios';
import store from '../store';
import { showToast } from './toasted';

axios.defaults.withCredentials = true;

const FALLBACK_MESSAGES = {
  400: "That request wasn't valid",
  401: 'Invalid credentials',
  403: "You don't have permission to do that",
  409: 'That already exists',
};

// doing something with the response
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    // all 4xx/5xx responses will end here
    const status = error.status || (error.response && error.response.status);
    // The backend already sends a specific, readable message for most of
    // these ("Email already exists.") - prefer it over a generic per-status
    // string, which was actively throwing away clearer information.
    const backendMessage = error.response && error.response.data && error.response.data.message;
    const message = backendMessage || FALLBACK_MESSAGES[status];
    if (message) {
      showToast(message, { type: 'error', duration: 7000 });
    }
    store.commit('setLoading', false);
    return Promise.reject(error);
  },
);

export default axios;
