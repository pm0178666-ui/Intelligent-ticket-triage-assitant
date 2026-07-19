import { useEffect, useState } from "react";
import {
  Loader2,
  RefreshCw,
  Clock,
  CheckCircle2,
  XCircle,
  ChevronRight,
} from "lucide-react";
import { getApprovals, approveRequest, rejectRequest } from "../api/apiClient";
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

function ApprovalBody({ approval }) {
  const payload = approval.payload || {};
  const action = approval.actionType || "";

  if (action === "PASSWORD_RESET") {
    return (
      <>
        <h4>Password Reset Request</h4>
        <p><b>Customer Email:</b> {payload.customerEmail || "N/A"}</p>
        <p><b>Ticket ID:</b> {payload.ticketId || "N/A"}</p>
      </>
    );
  }

  if (action === "ISSUE_REFUND") {
    return (
      <>
        <h4>Refund Request</h4>
        <p><b>Order ID:</b> {payload.orderId || "N/A"}</p>
        <p><b>Amount:</b> ₹{payload.amount ?? "N/A"}</p>
      </>
    );
  }

  return <h4>{action}</h4>;
}

export default function ApprovalDashboard() {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [busyId, setBusyId] = useState(null);

  function load() {
    setLoading(true);
    setError("");

    getApprovals()
      .then((data) => {
        const sortedApprovals = [...data].sort(
          (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
        );

        setApprovals(sortedApprovals);
      })
      .catch((e) => setError(`Failed to load approvals: ${e.message || e}`))
      .finally(() => setLoading(false));
  }

  useEffect(load, []);

  async function handleApprove(id) {
    setActionError("");
    setBusyId(id);
    try {
      await approveRequest(id);
      load();
    } catch (e) {
      setActionError(e.message || String(e));
      setBusyId(null);
    }
  }

  async function handleReject(id) {
    setActionError("");
    setBusyId(id);
    try {
      await rejectRequest(id);
      load();
    } catch (e) {
      setActionError(e.message || String(e));
      setBusyId(null);
    }
  }

  if (loading) {
    return (
      <div className="spinner-wrap">
        <Loader2 size={16} className="spin" /> Loading approvals...
      </div>
    );
  }
  if (error) return <Alert type="error">{error}</Alert>;

  const pending = approvals.filter((a) => (a.status || "").toUpperCase() === "PENDING");
  const approved = approvals.filter((a) => (a.status || "").toUpperCase() === "APPROVED");
  const rejected = approvals.filter((a) => (a.status || "").toUpperCase() === "REJECTED");

  return (
    <div>
      <PageHeader
        title="Approval Dashboard"
        subtitle="Manage refund and password reset approval requests."
        action={
          <button className="btn btn-outline btn-auto" onClick={load}>
            <RefreshCw size={15} />
            Refresh
          </button>
        }
      />

      <div className="metrics-row cols-3">
        <Metric label="Pending" value={pending.length} icon={Clock} tone="warning" />
        <Metric label="Approved" value={approved.length} icon={CheckCircle2} tone="success" />
        <Metric label="Rejected" value={rejected.length} icon={XCircle} tone="danger" />
      </div>

      <hr />

      <h3>Pending Requests</h3>

      {actionError && <Alert type="error">{actionError}</Alert>}

      {pending.length === 0 ? (
        <Alert type="success">No pending approval requests.</Alert>
      ) : (
        pending.map((approval) => (
          <Card key={approval.approvalId} hover>
            <div className="row-between">
              <div>
                <ApprovalBody approval={approval} />
                <p className="caption">Created : {formatDate(approval.createdAt)}</p>
              </div>

              <div className="btn-row" style={{ minWidth: 140 }}>
                <button
                  className="btn btn-auto"
                  disabled={busyId === approval.approvalId}
                  onClick={() => handleApprove(approval.approvalId)}
                >
                  {busyId === approval.approvalId ? <Loader2 size={15} className="spin" /> : <CheckCircle2 size={15} />}
                  Approve
                </button>
                <button
                  className="btn btn-auto btn-danger"
                  disabled={busyId === approval.approvalId}
                  onClick={() => handleReject(approval.approvalId)}
                >
                  <XCircle size={15} />
                  Reject
                </button>
              </div>
            </div>
          </Card>
        ))
      )}

      <hr />

      <details>
        <summary>
          <ChevronRight size={16} className="chev" />
          Approved Requests ({approved.length})
        </summary>

        {approved.length === 0 ? (
          <Alert type="info">No approved requests.</Alert>
        ) : (
          approved.map((approval) => (
            <Card key={approval.approvalId}>
              <div className="row-between">
                <div>
                  <ApprovalBody approval={approval} />
                  <p className="caption">Created : {formatDate(approval.createdAt)}</p>
                </div>
                <Badge tone="approved">APPROVED</Badge>
              </div>
            </Card>
          ))
        )}
      </details>

      <hr />

      <details>
        <summary>
          <ChevronRight size={16} className="chev" />
          Rejected Requests ({rejected.length})
        </summary>

        {rejected.length === 0 ? (
          <Alert type="info">No rejected requests.</Alert>
        ) : (
          rejected.map((approval) => (
            <Card key={approval.approvalId}>
              <div className="row-between">
                <div>
                  <ApprovalBody approval={approval} />
                  <p className="caption">Created : {formatDate(approval.createdAt)}</p>
                </div>
                <Badge tone="rejected">REJECTED</Badge>
              </div>
            </Card>
          ))
        )}
      </details>
    </div>
  );
}
