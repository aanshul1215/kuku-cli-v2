import { Link } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { buildLogoutUrl } from "../auth/authConfig.js";

export default function NavBar() {
  const auth = useAuth();
  const handleLogout = () => {
    auth.removeUser();
    window.location.href = buildLogoutUrl();
  };
  return (
    <nav style={{ background: "white", borderBottom: "1px solid #eee", padding: "0.75rem 1rem" }}>
      <div className="container" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 0 }}>
        <Link to="/portfolios" style={{ fontWeight: 600, fontSize: "1.1rem", textDecoration: "none", color: "#1a1a1a" }}>
          Portfolio Manager
        </Link>
        {auth.isAuthenticated && (
          <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
            <span style={{ color: "#666" }}>{auth.user?.profile?.email}</span>
            <button onClick={handleLogout}>Sign out</button>
          </div>
        )}
      </div>
    </nav>
  );
}
