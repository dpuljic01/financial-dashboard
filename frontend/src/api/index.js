// api/index.js

import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api'; // TODO: change this on deployment ofc

export function login(user) {
  return axios.post(`${API_URL}/login/`, user);
}

export function register(user) {
  return axios.post(`${API_URL}/register/${surveyId}/`, user);
}

export function fetchPortoflios() {
  return axios.get(`${API_URL}/portoflios/`);
}

export function fetchPortoflio() {
  return axios.get(`${API_URL}/portoflios/${portfolioId}`);
}

export function saveSurveyResponse(portfolioResponse) {
  return axios.put(`${API_URL}/portfolios/${portfolioResponse.id}/`, portfolioResponse);
}

export function createNewPortfolio(portfolio) {
  return axios.post(`${API_URL}/portfolios/`, portfolio);
}
