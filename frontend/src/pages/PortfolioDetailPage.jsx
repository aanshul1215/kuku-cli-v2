import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { getPortfolio } from "../api/portfolios.js";
import ErrorBanner from "../components/ErrorBanner.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";

export default function PortfolioDetailPage() {
  const { id } = useParams();
  const auth = useAuth();
  const token = auth.user?.id_token;

  const [portfolio, setPortfolio] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const fetchMetadata = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await getPortfolio(token, id);
        setPortfolio(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    if (token) fetchMetadata();
  }, [id, token]);

  if (isLoading) return <div className="container"><LoadingSpinner /></div>;
  if (error) return <div className="container"><ErrorBanner message={error} /></div>;
  if (!portfolio) return null;

  return (
    <div className="container">
      <Link to="/portfolios" style={{ textDecoration: "none", color: "#007bff", marginBottom: "1rem", display: "inline-block" }}>
        &larr; Back to portfolios
      </Link>
      
      <header style={{ marginBottom: "2rem" }}>
        <h1>{portfolio.name}</h1>
        <p style={{ color: "#666", fontSize: "1.1rem" }}>{portfolio.description}</p>
      </header>

      <section style={{ marginBottom: "2rem" }}>
        <h2>Holdings</h2>
        <div>Coming soon</div>
      </section>

      <section style={{ marginBottom: "2rem", display: "flex", gap: "2rem" }}>
        <div style={{ flex: 1 }}>
          <h2>Buy</h2>
          <div>Coming soon</div>
        </div>
        <div style={{ flex: 1 }}>
          <h2>Sell</h2>
          <div>Coming soon</div>
        </div>
      </section>

      <section style={{ marginBottom: "2rem" }}>
        <h2>Transaction history</h2>
        <div>Coming soon</div>
      </section>
    </div>
  );
}
