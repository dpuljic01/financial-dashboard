import Vue from 'vue';

const API_URL = process.env.VUE_APP_API_URL;

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

export function fetchPortoflios() {
  return Vue.axios.get(`${API_URL}/users/self/portoflios`);
}

export function fetchPortoflio(portfolioId) {
  return Vue.axios.get(`${API_URL}/users/self/portoflios/${portfolioId}`);
}

export function savePortfolioResponse(portfolioResponse) {
  return Vue.axios.put(`${API_URL}/users/self/portfolios/${portfolioResponse.id}/`, portfolioResponse);
}

export function createNewPortfolio(portfolio) {
  return Vue.axios.post(`${API_URL}/users/self/portfolios`, portfolio);
}

export function getStockHistoryData(params, accessToken) {
  return Vue.axios.get(`${API_URL}/stocks/yfinance`, {
    params,
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}
