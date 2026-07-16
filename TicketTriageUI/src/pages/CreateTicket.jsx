import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2, Paperclip } from "lucide-react";
import { createTicket } from "../api/apiClient";
import { Alert, Card, PageHeader } from "../components/UI";

const initialForm = {
  customerName: "",
  customerEmail: "",
  subject: "",
  message: "",
};

export default function CreateTicket() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [fieldError, setFieldError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setFieldError("");
    setSubmitError("");
    setResult(null);

    if (!form.customerName.trim()) {
      setFieldError("Customer Name is required.");
      return;
    }
    if (!form.customerEmail.trim()) {
      setFieldError("Customer Email is required.");
      return;
    }
    if (!form.subject.trim()) {
      setFieldError("Issue Summary is required.");
      return;
    }
    if (!form.message.trim()) {
      setFieldError("Issue Description is required.");
      return;
    }

    setSubmitting(true);
    try {
      const data = await createTicket(form);
      setResult(data);
      setForm(initialForm);
    } catch (err) {
      setSubmitError(err.message || String(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <PageHeader
        title="Create Support Ticket"
        subtitle="Submit your issue to our AI-powered support system."
        onBack={() => navigate("/")}
      />

      <Card>
        <h3>Ticket Information</h3>

        <form onSubmit={handleSubmit}>
          <div className="field-group">
            <label>Customer Name</label>
            <input
              className="text-input"
              placeholder="Enter your full name"
              value={form.customerName}
              onChange={(e) => update("customerName", e.target.value)}
            />
          </div>

          <div className="field-group">
            <label>Customer Email</label>
            <input
              className="text-input"
              placeholder="Enter your email address"
              value={form.customerEmail}
              onChange={(e) => update("customerEmail", e.target.value)}
            />
          </div>

          <div className="field-group">
            <label>Issue Summary</label>
            <input
              className="text-input"
              placeholder="Briefly describe your issue"
              value={form.subject}
              onChange={(e) => update("subject", e.target.value)}
            />
          </div>

          <div className="field-group">
            <label>Describe Your Issue</label>
            <textarea
              className="text-input"
              rows={7}
              placeholder="Explain your issue in detail..."
              value={form.message}
              onChange={(e) => update("message", e.target.value)}
            />
          </div>

          <div className="field-group">
            <label>
              <Paperclip size={13} style={{ verticalAlign: -2, marginRight: 5 }} />
              Attachment (Optional)
            </label>
            <input className="text-input" type="file" />
          </div>

          {fieldError && <Alert type="error">{fieldError}</Alert>}

          <button className="btn" type="submit" disabled={submitting}>
            {submitting && <Loader2 size={16} className="spin" />}
            {submitting ? "Creating..." : "Create Ticket"}
          </button>
        </form>
      </Card>

      {submitError && (
        <Alert type="error">Failed to create ticket. {submitError}</Alert>
      )}

      {result && (
        <>
          <Alert type="success">Ticket Created Successfully!</Alert>

          <div className="grid-2">
            <Alert type="info">
              <b>Ticket ID</b>
              <br />
              {result.ticketId}
            </Alert>
            <Alert type="info">
              <b>Current Status</b>
              <br />
              {result.status}
            </Alert>
          </div>

          <Alert type="success">
            You can monitor your ticket status and AI response anytime from
            the My Tickets page.
          </Alert>
        </>
      )}
    </div>
  );
}
