import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Ticket, Mail, KeyRound, Loader2, CheckCircle2 } from "lucide-react";
import { confirmSignUp, resendConfirmationCode } from "../auth/cognito";
import { Alert } from "../components/UI";

export default function VerifyOtp() {
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState(location.state?.email || "");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [resendMessage, setResendMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [resending, setResending] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setResendMessage("");

    if (!email.trim()) {
      setError("Email is required.");
      return;
    }
    if (!code.trim()) {
      setError("Enter the OTP sent to your email.");
      return;
    }

    setSubmitting(true);
    try {
      await confirmSignUp(email, code);
      navigate("/login", {
        state: {
          email,
          message: "Account verified! You can now sign in.",
        },
      });
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleResend() {
    setError("");
    setResendMessage("");

    if (!email.trim()) {
      setError("Enter your email first.");
      return;
    }

    setResending(true);
    try {
      await resendConfirmationCode(email);
      setResendMessage("A new OTP has been sent to your email.");
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setResending(false);
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

        <h2>Verify your account</h2>
        <p className="subtitle">Enter the OTP we sent to your email to activate your account.</p>

        {error && <Alert type="error">{error}</Alert>}
        {resendMessage && <Alert type="success">{resendMessage}</Alert>}

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
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="login-field">
            <label htmlFor="code">OTP Code</label>
            <div className="input-with-icon">
              <KeyRound size={16} />
              <input
                id="code"
                className="text-input"
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                placeholder="Enter the 6-digit code"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </div>
          </div>

          <button className="btn" type="submit" disabled={submitting}>
            {submitting ? <Loader2 size={16} className="spin" /> : <CheckCircle2 size={16} />}
            {submitting ? "Verifying..." : "Verify Account"}
          </button>
        </form>

        <div className="auth-switch">
          Didn&apos;t get a code?{" "}
          <button type="button" className="link-btn" onClick={handleResend} disabled={resending}>
            {resending ? "Sending..." : "Resend Code"}
          </button>
        </div>
      </div>
    </div>
  );
}
