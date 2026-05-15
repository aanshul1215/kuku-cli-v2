import { useState, useEffect, useCallback } from "react";
import { useAuth } from "react-oidc-context";
import { listMyPortfolios } from "../api/portfolios.js";
import PortfolioCard from "../components/PortfolioCard.jsx";
import ErrorBanner from "../components/ErrorBanner.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import CreatePortfolioForm from "../components/CreatePortfolioForm.jsx";

export default function PortfoliosListPage() {
  const auth = useAuth();
  const token = auth.user?.id_token;
  const [portfolios, setPortfolios] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPortfolios = useCallback(async () => {
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
  }, [token]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (token) fetchPortfolios();
  }, [fetchPortfolios, token]);

  const handleDelete = async (id) => {
    try {
      await import("../api/portfolios.js").then((m) => m.deletePortfolio(token, id));
      fetchPortfolios();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h2>My Portfolios</h2>
      {error && <ErrorBanner message={error} />}
      
      <CreatePortfolioForm onCreated={fetchPortfolios} />

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
