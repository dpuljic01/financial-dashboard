import Vue from 'vue';

const API_URL = process.env.VUE_APP_API_URL;

export function getUser(accessToken) {
  return Vue.axios.get(`${API_URL}/users/self`, { headers: { Authorization: `Bearer ${accessToken}` } });
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

export function setPassword(payload) {
  return Vue.axios.put(`${API_URL}/reset-password`, payload);
}

export function changePassword(payload, accessToken) {
  return Vue.axios.put(`${API_URL}/users/self/change-password`, payload, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function updateUser(payload, accessToken) {
  return Vue.axios.put(`${API_URL}/users/self`, payload, { headers: { Authorization: `Bearer ${accessToken}` } });
}

export function getPortfolios(accessToken) {
  return Vue.axios.get(`${API_URL}/portfolios`, { headers: { Authorization: `Bearer ${accessToken}` } });
}

export function getPortfolio(identifier, accessToken) {
  return Vue.axios.get(`${API_URL}/portfolios/${identifier}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function getLatestStockPrices(params, accessToken) {
  return Vue.axios.get(`${API_URL}/stocks/yfinance/latest`, {
    params,
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function getCompanyInfo(symbol, accessToken) {
  return Vue.axios.get(`${API_URL}/stocks/${symbol}/company-info`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function getNews(params, accessToken) {
  return Vue.axios.get(`${API_URL}/news/scrape`, {
    params,
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function createNewHolding(data, accessToken) {
  return Vue.axios({
    method: 'post',
    url: `${API_URL}/portfolios/${data.portfolio}/holdings`,
    headers: { Authorization: `Bearer ${accessToken}` },
    data: data.payload,
  });
}

export function createNewPortfolio(portfolio, accessToken) {
  return Vue.axios.post(`${API_URL}/portfolios`, portfolio, {
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

export function addSymbol(data, accessToken) {
  return Vue.axios({
    method: 'post',
    url: `${API_URL}/portfolios/${data.portfolio}/symbols`,
    headers: { Authorization: `Bearer ${accessToken}` },
    data: data.payload,
  });
}

// this only unlinks symbol from portfolio, not completely from Stock table
export function deleteSymbol(params, accessToken) {
  return Vue.axios.delete(`${API_URL}/portfolios/${params.portfolioId}/${params.stockId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function deletePortfolio(params, accessToken) {
  return Vue.axios.delete(`${API_URL}/portfolios/${params.portfolioId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}
