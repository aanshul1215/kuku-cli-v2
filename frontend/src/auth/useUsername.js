import { useAuth } from "react-oidc-context";

export function useUsername() {
  const auth = useAuth();
  return auth.user?.profile?.sub ?? null;
}
