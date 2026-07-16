import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2, ListChecks, CheckCircle2, Clock, ArrowRight } from "lucide-react";
import { getTickets } from "../api/apiClient";
import { useAuth } from "../context/AuthContext";
import { Alert, Metric, Card, Badge, PageHeader } from "../components/UI";

function formatDate(dateString) {
  if (!dateString) return "N/A";
  const d = new Date(dateString);
  return d.toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function statusTone(status) {
  const s = (status || "").toLowerCase();
  if (s === "processed") return "processed";
  if (s === "pending") return "pending";
  return "neutral";
}

export default function MyTickets() {
  const { email } = useAuth();
  const navigate = useNavigate();

  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    getTickets()
      .then((all) => {
        if (cancelled) return;
        const mine = all
          .filter((t) => t.customerEmail === email)
          .sort((a, b) => (b.createdAt || "").localeCompare(a.createdAt || ""));
        setTickets(mine);
      })
      .catch((e) => {
        if (!cancelled) setError(`Failed to load tickets: ${e.message || e}`);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [email]);

  if (loading) {
    return (
      <div className="spinner-wrap">
        <Loader2 size={16} className="spin" /> Loading tickets...
      </div>
    );
  }

  if (error) {
    return <Alert type="error">{error}</Alert>;
  }

  const total = tickets.length;
  const processed = tickets.filter((t) => (t.status || "").toLowerCase() === "processed").length;
  const pending = total - processed;

  return (
    <div>
      <PageHeader
        title="My Tickets"
        subtitle="View and track all support tickets submitted by you."
        onBack={() => navigate("/")}
      />

      <div className="metrics-row cols-3">
        <Metric label="Total Tickets" value={total} icon={ListChecks} />
        <Metric label="Processed" value={processed} icon={CheckCircle2} tone="success" />
        <Metric label="Pending" value={pending} icon={Clock} tone="warning" />
      </div>

      <hr />

      {total === 0 ? (
        <Alert type="warning">You haven't created any tickets yet.</Alert>
      ) : (
        tickets.map((ticket) => (
          <Card key={ticket.ticketId} hover>
            <div className="row-between">
              <div>
                <h3>{ticket.subject || "N/A"}</h3>
                <p><b>Ticket ID:</b> {ticket.ticketId || "N/A"}</p>
                <p>
                  <b>Status:</b>{" "}
                  <Badge tone={statusTone(ticket.status)}>
                    {(ticket.status || "N/A").toUpperCase()}
                  </Badge>
                </p>
                <p><b>Created On:</b> {formatDate(ticket.createdAt)}</p>
              </div>

              <button
                className="btn btn-auto"
                onClick={() => navigate("/ticket-details", { state: { ticketId: ticket.ticketId } })}
              >
                View
                <ArrowRight size={15} />
              </button>
            </div>
          </Card>
        ))
      )}
    </div>
  );
}
