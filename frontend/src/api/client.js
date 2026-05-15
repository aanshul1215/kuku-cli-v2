const API_BASE = import.meta.env.VITE_API_BASE_URL;

export class ApiError extends Error {
  constructor(status, message, detail) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

/**
 * Make an authenticated request to the backend.
 * @param {string} path - path beginning with "/"
 * @param {object} options - fetch options
 * @param {string} token - the JWT (id_token from auth.user)
 */
export async function apiRequest(path, options = {}, token) {
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };
  let res;
  try {
    res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  } catch {
    throw new ApiError(0, "Could not reach the server. Check your connection and try again.", null);
  }
  
  if (res.status === 401) {
    sessionStorage.clear();
    window.location.href = "/login";
    return null;
  }

  const text = await res.text();
  const body = text ? JSON.parse(text) : null;
  if (!res.ok) {
    const message = body?.error || `Request failed with status ${res.status}`;
    const detail = body?.detail || null;
    throw new ApiError(res.status, message, detail);
  }
  return body;
}
