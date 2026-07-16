import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Ticket, Mail, Lock, Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { Alert } from "../components/UI";

export default function Login() {
  const { loggedIn, login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (loggedIn) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await login(username, password);
      navigate("/");
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="login-screen">
      <div className="login-card">
        <div className="brand">
          <div className="brand-mark">
            <Ticket size={16} />
          </div>
          <div>
            <div className="brand-name">Ticket Triage</div>
            <div className="brand-sub">Assistant</div>
          </div>
        </div>

        <h2>Welcome back</h2>
        <p className="subtitle">Sign in to continue to your dashboard.</p>

        {error && <Alert type="error">{error}</Alert>}

        <form onSubmit={handleSubmit}>
          <div className="login-field">
            <label htmlFor="email">Email</label>
            <div className="input-with-icon">
              <Mail size={16} />
              <input
                id="email"
                className="text-input"
                type="text"
                autoComplete="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
          </div>

          <div className="login-field">
            <label htmlFor="password">Password</label>
            <div className="input-with-icon">
              <Lock size={16} />
              <input
                id="password"
                className="text-input"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button className="btn" type="submit" disabled={submitting}>
            {submitting && <Loader2 size={16} className="spin" />}
            {submitting ? "Signing in..." : "Login"}
          </button>
        </form>

        <div className="login-footer">
          &copy; {new Date().getFullYear()} Ticket Triage Assistant
        </div>
      </div>
    </div>
  );
}
