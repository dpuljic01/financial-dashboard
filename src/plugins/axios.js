import Vue from 'vue';
import axios from 'axios';

axios.defaults.withCredentials = true;

// doing something with the response
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    // all 4xx/5xx responses will end here
    let message = 'We were unable to complete your request';
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
        message = 'We were unable to complete your request';
    }

    Vue.toasted.show(message, { type: 'error' });
    return Promise.reject(error);
  },
);

export default axios;
