import { apiRequest } from "./client.js";

export const buy = (token, { portfolio_id, ticker, quantity }) =>
  apiRequest(
    "/trades/buy",
    { method: "POST", body: JSON.stringify({ portfolio_id, ticker, quantity }) },
    token
  );

export const sell = (token, { portfolio_id, ticker, quantity }) =>
  apiRequest(
    "/trades/sell",
    { method: "POST", body: JSON.stringify({ portfolio_id, ticker, quantity }) },
    token
  );
