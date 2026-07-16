import { createContext, useContext, useState } from "react";
import { login as cognitoLogin } from "../auth/cognito";

const STORAGE_KEY = "ticketTriageSession";

const AuthContext = createContext(null);

function loadSession() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function saveSession(session) {
  if (session) {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(session));
  } else {
    sessionStorage.removeItem(STORAGE_KEY);
  }
}

export function AuthProvider({ children }) {
  const [session, setSession] = useState(loadSession);

  async function login(username, password) {
    const { group } = await cognitoLogin(username, password);

    const newSession = {
      loggedIn: true,
      username,
      email: username,
      group,
    };

    setSession(newSession);
    saveSession(newSession);
  }

  function logout() {
    setSession(null);
    saveSession(null);
  }

  const value = {
    loggedIn: !!session?.loggedIn,
    username: session?.username || "",
    email: session?.email || "",
    group: session?.group || "UNKNOWN",
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
