import { useState } from "react";
import { useAuth } from "react-oidc-context";
import { buy } from "../api/trades.js";
import ErrorBanner from "./ErrorBanner.jsx";

export default function BuyForm({ portfolioId, onTradeComplete }) {
  const auth = useAuth();
  const token = auth.user?.id_token;

  const [ticker, setTicker] = useState("");
  const [quantity, setQuantity] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!ticker.trim() || !quantity || Number(quantity) <= 0) {
      setError("Valid ticker and positive quantity are required");
      return;
    }
    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const upperTicker = ticker.toUpperCase().trim();
      const numQuantity = Number(quantity);
      await buy(token, { portfolio_id: portfolioId, ticker: upperTicker, quantity: numQuantity });
      setTicker("");
      setQuantity("");
      setSuccess(`Bought ${numQuantity} shares of ${upperTicker}`);
      setTimeout(() => setSuccess(null), 3000);
      if (onTradeComplete) onTradeComplete();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ background: "white", padding: "1rem", border: "1px solid #ccc", borderRadius: "4px" }}>
      {error && <ErrorBanner message={error} />}
      {success && <div className="success">{success}</div>}
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <div>
          <label style={{ display: "block", marginBottom: "0.5rem" }}>Ticker</label>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            disabled={isLoading}
            style={{ width: "100%" }}
          />
        </div>
        <div>
          <label style={{ display: "block", marginBottom: "0.5rem" }}>Quantity</label>
          <input
            type="number"
            step="any"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            disabled={isLoading}
            style={{ width: "100%" }}
          />
        </div>
        <button type="submit" disabled={isLoading} style={{ alignSelf: "flex-start" }}>
          {isLoading ? "Buying…" : "Buy"}
        </button>
      </form>
    </div>
  );
}
