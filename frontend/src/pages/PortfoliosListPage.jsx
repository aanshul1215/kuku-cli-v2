import { useState, useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { listMyPortfolios } from "../api/portfolios.js";
import PortfolioCard from "../components/PortfolioCard.jsx";
import ErrorBanner from "../components/ErrorBanner.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";

export default function PortfoliosListPage() {
  const auth = useAuth();
  const token = auth.user?.id_token;
  const [portfolios, setPortfolios] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPortfolios = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listMyPortfolios(token);
      setPortfolios(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (token) fetchPortfolios();
  }, [token]);

  const handleDelete = async (id) => {
    // To be fully wired in Phase 8
  };

  return (
    <div className="container">
      <h2>My Portfolios</h2>
      {error && <ErrorBanner message={error} />}
      
      {/* Placeholder for CreatePortfolioForm (Phase 7) */}

      {isLoading ? (
        <LoadingSpinner />
      ) : portfolios.length === 0 ? (
        <p>You have no portfolios yet. Create one below.</p>
      ) : (
        portfolios.map((p) => (
          <PortfolioCard key={p.id} portfolio={p} onDelete={handleDelete} />
        ))
      )}
    </div>
  );
}
