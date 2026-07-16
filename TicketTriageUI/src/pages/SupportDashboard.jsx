import { useEffect, useState } from "react";
import { Loader2, Ticket, CheckCircle2, Clock, Flame, Search } from "lucide-react";
import { getTickets } from "../api/apiClient";
import { Alert, Metric, Badge, PageHeader } from "../components/UI";
import DataTable from "../components/DataTable";

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

function priorityTone(priority) {
  const p = (priority || "").toLowerCase();
  if (p === "high") return "high";
  if (p === "medium") return "medium";
  if (p === "low") return "low";
  return "neutral";
}

const columns = [
  { key: "ticketId", header: "Ticket ID" },
  { key: "customerName", header: "Customer" },
  { key: "customerEmail", header: "Email" },
  { key: "subject", header: "Subject" },
  { key: "category", header: "Category" },
  {
    key: "priority",
    header: "Priority",
    render: (r) => <Badge tone={priorityTone(r.priority)}>{r.priority || "N/A"}</Badge>,
  },
  {
    key: "status",
    header: "Status",
    render: (r) => <Badge tone={statusTone(r.status)}>{(r.status || "N/A").toUpperCase()}</Badge>,
  },
  { key: "createdOn", header: "Created On", render: (r) => formatDate(r.createdAt) },
];

export default function SupportDashboard() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [searchTicket, setSearchTicket] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [priorityFilter, setPriorityFilter] = useState("All");
  const [applied, setApplied] = useState({ search: "", status: "All", priority: "All" });

  useEffect(() => {
    getTickets()
      .then((data) => {
        const sorted = [...data].sort((a, b) =>
          (b.createdAt || "").localeCompare(a.createdAt || "")
        );
        setTickets(sorted);
      })
      .catch((e) => setError(`Failed to load tickets: ${e.message || e}`))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="spinner-wrap">
        <Loader2 size={16} className="spin" /> Loading tickets...
      </div>
    );
  }
  if (error) return <Alert type="error">{error}</Alert>;

  const total = tickets.length;
  const processed = tickets.filter((t) => (t.status || "").toLowerCase() === "processed").length;
  const pending = total - processed;
  const highPriority = tickets.filter((t) => (t.priority || "").toLowerCase() === "high").length;

  let filtered = tickets;
  if (applied.search) {
    filtered = filtered.filter((t) =>
      (t.ticketId || "").toLowerCase().includes(applied.search.toLowerCase())
    );
  }
  if (applied.status !== "All") {
    filtered = filtered.filter((t) => (t.status || "").toLowerCase() === applied.status.toLowerCase());
  }
  if (applied.priority !== "All") {
    filtered = filtered.filter((t) => (t.priority || "").toLowerCase() === applied.priority.toLowerCase());
  }

  return (
    <div>
      <PageHeader
        title="Support Dashboard"
        subtitle="View, search and manage all customer support tickets."
      />

      <div className="metrics-row cols-4">
        <Metric label="Total Tickets" value={total} icon={Ticket} />
        <Metric label="Processed" value={processed} icon={CheckCircle2} tone="success" />
        <Metric label="Pending" value={pending} icon={Clock} tone="warning" />
        <Metric label="High Priority" value={highPriority} icon={Flame} tone="danger" />
      </div>

      <hr />

      <h3>Filters</h3>

      <div className="filter-bar">
        <div className="field-group">
          <label>Ticket ID</label>
          <input
            className="text-input"
            value={searchTicket}
            onChange={(e) => setSearchTicket(e.target.value)}
          />
        </div>

        <div className="field-group">
          <label>Status</label>
          <select
            className="text-input"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option>All</option>
            <option value="processed">processed</option>
            <option value="pending">pending</option>
          </select>
        </div>

        <div className="field-group">
          <label>Priority</label>
          <select
            className="text-input"
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
          >
            <option>All</option>
            <option>High</option>
            <option>Medium</option>
            <option>Low</option>
          </select>
        </div>

        <div className="field-group">
          <button
            className="btn btn-auto"
            onClick={() =>
              setApplied({ search: searchTicket, status: statusFilter, priority: priorityFilter })
            }
          >
            <Search size={15} />
            Search
          </button>
        </div>
      </div>

      <hr />

      <div className="section-heading">
        <h3>All Support Tickets</h3>
        <span className="caption" style={{ marginBottom: 0 }}>
          Showing {filtered.length} ticket(s)
        </span>
      </div>

      <DataTable
        columns={columns}
        rows={filtered.map((t) => ({ ...t, id: t.ticketId }))}
      />
    </div>
  );
}
