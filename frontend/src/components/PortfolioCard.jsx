import { Link } from "react-router-dom";

export default function PortfolioCard({ portfolio, onDelete }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: "1rem", borderRadius: "4px", marginBottom: "1rem", background: "white" }}>
      <h3>{portfolio.name}</h3>
      <p>{portfolio.description}</p>
      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        <Link to={`/portfolios/${portfolio.id}`} style={{ padding: "0.5rem 1rem", border: "1px solid #007bff", color: "#007bff", textDecoration: "none", borderRadius: "4px" }}>
          View
        </Link>
        <button onClick={() => {
          if (window.confirm("Delete this portfolio? This cannot be undone.")) {
            onDelete(portfolio.id);
          }
        }} style={{ color: "red", borderColor: "red" }}>
          Delete
        </button>
      </div>
    </div>
  );
}
