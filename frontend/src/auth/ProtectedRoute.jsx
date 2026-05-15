import { useAuth } from "react-oidc-context";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const auth = useAuth();
  if (auth.isLoading) return <div className="container">Loading…</div>;
  if (auth.error) return <div className="container error">Auth error: {auth.error.message}</div>;
  if (!auth.isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}
