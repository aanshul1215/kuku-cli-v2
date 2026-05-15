import { useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { useNavigate } from "react-router-dom";

export default function CallbackPage() {
  const auth = useAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (auth.isAuthenticated) navigate("/portfolios", { replace: true });
    if (auth.error) navigate("/login", { replace: true });
  }, [auth.isAuthenticated, auth.error, navigate]);
  return <div className="container">Completing sign-in…</div>;
}
