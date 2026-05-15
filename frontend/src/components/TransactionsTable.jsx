import { useState, useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { getTransactions } from "../api/portfolios.js";
import ErrorBanner from "./ErrorBanner.jsx";
import LoadingSpinner from "./LoadingSpinner.jsx";

export default function TransactionsTable({ portfolioId, refreshKey }) {
  const auth = useAuth();
  const token = auth.user?.id_token;

  const [transactions, setTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await getTransactions(token, portfolioId);
        // Ensure reverse chronological order if backend doesn't sort it properly
        const sorted = data.sort((a, b) => new Date(b.date_time) - new Date(a.date_time));
        setTransactions(sorted);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    if (token) fetchTransactions();
  }, [token, portfolioId, refreshKey]);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner message={error} />;
  if (transactions.length === 0) return <p>No transactions yet.</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Type</th>
          <th>Ticker</th>
          <th>Quantity</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((t, i) => (
          <tr key={i}>
            <td>{new Date(t.date_time).toLocaleString()}</td>
            <td>{t.transaction_type}</td>
            <td>{t.ticker}</td>
            <td>{t.quantity}</td>
            <td>${Number(t.price).toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
