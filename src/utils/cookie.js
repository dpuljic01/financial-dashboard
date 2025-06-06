import VueCookies from 'vue-cookies';

export function setCookie(name, value, expiry = '1d', path = '/', domain = '', secure = '', sameSite = 'Lax') {
  const secureProd = (process.env.NODE_ENV === 'production') ? true : secure;
  VueCookies.set(name, value, expiry, path, domain, secureProd, sameSite);
}

export function getCookie(name) {
  return VueCookies.get(name);
}

export function removeCookie(name) {
  VueCookies.remove(name);
}
