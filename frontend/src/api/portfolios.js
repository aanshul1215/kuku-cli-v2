import { apiRequest } from "./client.js";

export const listMyPortfolios = (token) =>
  apiRequest("/portfolios/me", { method: "GET" }, token);

export const createPortfolio = (token, { username, name, description }) =>
  apiRequest(
    "/portfolios/",
    { method: "POST", body: JSON.stringify({ username, name, description }) },
    token
  );

export const deletePortfolio = (token, portfolioId) =>
  apiRequest(`/portfolios/${portfolioId}`, { method: "DELETE" }, token);

export const getPortfolio = (token, portfolioId) =>
  apiRequest(`/portfolios/${portfolioId}`, { method: "GET" }, token);

export const getHoldings = (token, portfolioId) =>
  apiRequest(`/portfolios/${portfolioId}/holdings`, { method: "GET" }, token);

export const getTransactions = (token, portfolioId) =>
  apiRequest(`/portfolios/${portfolioId}/transactions`, { method: "GET" }, token);
