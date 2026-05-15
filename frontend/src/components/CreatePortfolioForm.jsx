import { useState } from "react";
import { useAuth } from "react-oidc-context";
import { createPortfolio } from "../api/portfolios.js";
import { useUsername } from "../auth/useUsername.js";
import ErrorBanner from "./ErrorBanner.jsx";

export default function CreatePortfolioForm({ onCreated }) {
  const auth = useAuth();
  const username = useUsername();
  const token = auth.user?.id_token;

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    setIsLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const finalDescription = description.trim() || "No description provided";
      await createPortfolio(token, { username, name, description: finalDescription });
      setName("");
      setDescription("");
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      if (onCreated) onCreated();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ marginBottom: "2rem", padding: "1rem", background: "white", border: "1px solid #ccc", borderRadius: "4px" }}>
      <h3>Create New Portfolio</h3>
      {error && <ErrorBanner message={error} />}
      {success && <div className="success">Portfolio created successfully!</div>}
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <div>
          <label htmlFor="portfolioName" style={{ display: "block", marginBottom: "0.5rem" }}>Name</label>
          <input
            id="portfolioName"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={isLoading}
            style={{ width: "100%" }}
          />
        </div>
        <div>
          <label htmlFor="portfolioDescription" style={{ display: "block", marginBottom: "0.5rem" }}>Description</label>
          <textarea
            id="portfolioDescription"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isLoading}
            style={{ width: "100%" }}
          />
        </div>
        <button type="submit" disabled={isLoading} style={{ alignSelf: "flex-start" }}>
          {isLoading ? "Creating…" : "Create Portfolio"}
        </button>
      </form>
    </div>
  );
}
