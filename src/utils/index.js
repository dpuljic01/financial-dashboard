import Vue from 'vue';

export const EventBus = new Vue();

export function isValidJwt(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1])); // atob decodes base64 encoded string
  const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds and in flask we had seconds
  const now = new Date();
  return now < exp;
}

export function isValidEmail(email) {
  /* eslint max-len: ["error", { "code": 200 }] */
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}
