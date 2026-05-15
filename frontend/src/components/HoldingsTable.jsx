import { useState, useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { getHoldings } from "../api/portfolios.js";
import ErrorBanner from "./ErrorBanner.jsx";
import LoadingSpinner from "./LoadingSpinner.jsx";

export default function HoldingsTable({ portfolioId, refreshKey }) {
  const auth = useAuth();
  const token = auth.user?.id_token;

  const [holdings, setHoldings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHoldings = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await getHoldings(token, portfolioId);
        setHoldings(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    if (token) fetchHoldings();
  }, [token, portfolioId, refreshKey]);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner message={error} />;
  if (holdings.length === 0) return <p>This portfolio has no holdings yet.</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Ticker</th>
          <th>Quantity</th>
        </tr>
      </thead>
      <tbody>
        {holdings.map((h, i) => (
          <tr key={i}>
            <td>{h.ticker}</td>
            <td>{h.quantity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
