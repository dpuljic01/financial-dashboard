import Vue from 'vue';

const API_URL = process.env.VUE_APP_API_URL;

export function getUser(accessToken) {
  return Vue.axios.get(`${API_URL}/users/self/`, { headers: { Authorization: `Bearer ${accessToken}` } });
}

export function login(userData) {
  return Vue.axios.post(`${API_URL}/session/auth`, userData);
}

export function logout(accessToken) {
  return Vue.axios.delete(`${API_URL}/session/revoke`, { headers: { Authorization: `Bearer ${accessToken}` } });
}

export function register(userData) {
  return Vue.axios.post(`${API_URL}/register`, userData);
}

export function resetPassword(payload) {
  return Vue.axios.post(`${API_URL}/reset-password`, payload);
}

export function changePassword(payload) {
  return Vue.axios.put(`${API_URL}/reset-password`, payload);
}

export function fetchPortfolios(accessToken) {
  return Vue.axios.get(`${API_URL}/users/self/portfolios`, { headers: { Authorization: `Bearer ${accessToken}` } });
}

export function fetchPortfolio(portfolioId, accessToken) {
  return Vue.axios.get(`${API_URL}/users/self/portfolios/${portfolioId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function createNewHolding(portfolioId, payload) {
  return Vue.axios.post(`${API_URL}/users/self/portfolios/${portfolioId}/`, payload);
}

export function createNewPortfolio(portfolio, accessToken) {
  return Vue.axios.post(`${API_URL}/users/self/portfolios`, portfolio, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function getStockHistoryData(params, accessToken) {
  return Vue.axios.get(`${API_URL}/stocks/yfinance`, {
    params,
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function search(params, accessToken) {
  return Vue.axios.get(`${API_URL}/stocks/search`, {
    params,
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}
