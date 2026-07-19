import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Ticket, User, Mail, Lock, Loader2 } from "lucide-react";
import { signUp } from "../auth/cognito";
import { Alert } from "../components/UI";

export default function SignUp() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!name.trim()) {
      setError("Full Name is required.");
      return;
    }
    if (!email.trim()) {
      setError("Email is required.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setSubmitting(true);
    try {
      await signUp(name, email, password);
      navigate("/verify-otp", { state: { email } });
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

        <h2>Create your account</h2>
        <p className="subtitle">Sign up to start submitting support tickets.</p>

        {error && <Alert type="error">{error}</Alert>}

        <form onSubmit={handleSubmit}>
          <div className="login-field">
            <label htmlFor="name">Full Name</label>
            <div className="input-with-icon">
              <User size={16} />
              <input
                id="name"
                className="text-input"
                type="text"
                autoComplete="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          </div>

          <div className="login-field">
            <label htmlFor="email">Email</label>
            <div className="input-with-icon">
              <Mail size={16} />
              <input
                id="email"
                className="text-input"
                type="text"
                autoComplete="username"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div className="login-field">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <div className="input-with-icon">
              <Lock size={16} />
              <input
                id="confirmPassword"
                className="text-input"
                type="password"
                autoComplete="new-password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
          </div>

          <button className="btn" type="submit" disabled={submitting}>
            {submitting && <Loader2 size={16} className="spin" />}
            {submitting ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <div className="auth-switch">
          Already have an account?{" "}
          <button type="button" className="link-btn" onClick={() => navigate("/login")}>
            Sign In
          </button>
        </div>
      </div>
    </div>
  );
}
