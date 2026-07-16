import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Loader2, Search, Tags, Flame, Smile, Gauge } from "lucide-react";
import { getTicketById } from "../api/apiClient";
import { Alert, Metric, Card, Badge, PageHeader } from "../components/UI";

function formatDateTime(dateString) {
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

export default function TicketDetails() {
  const location = useLocation();
  const incomingId = location.state?.ticketId || "";

  const [ticketIdInput, setTicketIdInput] = useState(incomingId);
  const [ticket, setTicket] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function loadTicket(id) {
    if (!id.trim()) {
      setError("Please enter a Ticket ID.");
      return;
    }

    setLoading(true);
    setError("");
    setSearched(true);

    try {
      const data = await getTicketById(id);
      setTicket(data);
    } catch {
      setTicket(null);
      setError("Ticket not found.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (incomingId) {
      loadTicket(incomingId);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSearchAgain() {
    setTicket(null);
    setTicketIdInput("");
    setSearched(false);
    setError("");
  }

  return (
    <div>
      <PageHeader title="Ticket Details" subtitle="Search and view complete ticket information." />

      <Card>
        <div className="row">
          <div className="input-with-icon" style={{ flex: 5 }}>
            <Search size={16} />
            <input
              className="text-input"
              placeholder="Enter Ticket ID"
              value={ticketIdInput}
              onChange={(e) => setTicketIdInput(e.target.value)}
            />
          </div>
          <button
            className="btn btn-auto"
            style={{ flex: 1 }}
            onClick={() => loadTicket(ticketIdInput)}
          >
            Load Ticket
          </button>
        </div>
      </Card>

      {loading && (
        <div className="spinner-wrap">
          <Loader2 size={16} className="spin" /> Loading ticket...
        </div>
      )}

      {!loading && !searched && (
        <Alert type="info">Enter a Ticket ID and click 'Load Ticket'.</Alert>
      )}

      {!loading && error && <Alert type="error">{error}</Alert>}

      {!loading && ticket && (
        <>
          <h3>Customer Information</h3>
          <div className="grid-2">
            <p><b>Customer Name:</b> {ticket.customerName || "N/A"}</p>
            <p><b>Customer Email:</b> {ticket.customerEmail || "N/A"}</p>
          </div>

          <hr />

          <h3>Ticket Information</h3>
          <div className="grid-2">
            <div>
              <p><b>Ticket ID:</b> {ticket.ticketId || "N/A"}</p>
              <p><b>Subject:</b> {ticket.subject || "N/A"}</p>
              <p>
                <b>Status:</b>{" "}
                <Badge tone={statusTone(ticket.status)}>
                  {(ticket.status || "N/A").toUpperCase()}
                </Badge>
              </p>
            </div>
            <div>
              <p><b>Created On:</b> {formatDateTime(ticket.createdAt)}</p>
              <p><b>Updated On:</b> {formatDateTime(ticket.updatedAt)}</p>
            </div>
          </div>

          <hr />

          <h3>Issue Description</h3>
          <Alert type="info">{ticket.message || "No description available."}</Alert>

          <hr />

          <h3>AI Analysis</h3>
          <div className="metrics-row cols-4">
            <Metric label="Category" value={ticket.category || "N/A"} icon={Tags} />
            <Metric label="Priority" value={ticket.priority || "N/A"} icon={Flame} tone="danger" />
            <Metric label="Sentiment" value={ticket.sentiment || "N/A"} icon={Smile} tone="cyan" />
            <Metric label="Complexity" value={ticket.complexity || "N/A"} icon={Gauge} tone="warning" />
          </div>

          <hr />

          <h3>AI Generated Response</h3>
          <Card>{ticket.draftResponse || "No response generated."}</Card>

          <hr />

          <button className="btn btn-outline btn-auto" onClick={handleSearchAgain}>
            Search Another Ticket
          </button>
        </>
      )}
    </div>
  );
}
