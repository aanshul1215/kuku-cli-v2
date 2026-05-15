import { useAuth } from "react-oidc-context";
import { Navigate } from "react-router-dom";

export default function LoginPage() {
  const auth = useAuth();
  if (auth.isAuthenticated) return <Navigate to="/portfolios" replace />;
  return (
    <div className="container">
      <h1>Portfolio Manager</h1>
      <p>Sign in to access your portfolios.</p>
      <button onClick={() => auth.signinRedirect()}>Sign in with Cognito</button>
    </div>
  );
}
