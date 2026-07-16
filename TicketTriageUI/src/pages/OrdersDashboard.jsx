import { useEffect, useState } from "react";
import { Loader2, Package, PackageCheck, Truck, XCircle } from "lucide-react";
import { getOrders } from "../api/apiClient";
import { Alert, Metric, Badge, PageHeader } from "../components/UI";
import DataTable from "../components/DataTable";

function statusTone(status) {
  const s = (status || "").toLowerCase();
  if (s === "delivered") return "processed";
  if (s === "shipped") return "pending";
  if (s === "cancelled") return "rejected";
  return "neutral";
}

const columns = [
  { key: "orderId", header: "Order ID" },
  { key: "customerName", header: "Customer" },
  { key: "customerEmail", header: "Email" },
  { key: "amount", header: "Amount" },
  {
    key: "status",
    header: "Status",
    render: (r) => <Badge tone={statusTone(r.status)}>{(r.status || "N/A").toUpperCase()}</Badge>,
  },
];

export default function OrdersDashboard() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [searchOrder, setSearchOrder] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");

  useEffect(() => {
    getOrders()
      .then(setOrders)
      .catch((e) => setError(`Failed to load orders: ${e.message || e}`))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="spinner-wrap">
        <Loader2 size={16} className="spin" /> Loading orders...
      </div>
    );
  }
  if (error) return <Alert type="error">{error}</Alert>;

  const total = orders.length;
  const delivered = orders.filter((o) => (o.status || "").toLowerCase() === "delivered").length;
  const shipped = orders.filter((o) => (o.status || "").toLowerCase() === "shipped").length;
  const cancelled = orders.filter((o) => (o.status || "").toLowerCase() === "cancelled").length;

  let filtered = orders;
  if (searchOrder) {
    filtered = filtered.filter((o) =>
      (o.orderId || "").toLowerCase().includes(searchOrder.toLowerCase())
    );
  }
  if (statusFilter !== "All") {
    filtered = filtered.filter((o) => (o.status || "").toLowerCase() === statusFilter.toLowerCase());
  }

  return (
    <div>
      <PageHeader title="Orders Dashboard" subtitle="Monitor customer orders and refund requests." />

      <div className="metrics-row cols-4">
        <Metric label="Total Orders" value={total} icon={Package} />
        <Metric label="Delivered" value={delivered} icon={PackageCheck} tone="success" />
        <Metric label="Shipped" value={shipped} icon={Truck} tone="cyan" />
        <Metric label="Cancelled" value={cancelled} icon={XCircle} tone="danger" />
      </div>

      <hr />

      <div className="grid-2">
        <div className="field-group">
          <label>Search Order ID</label>
          <input
            className="text-input"
            value={searchOrder}
            onChange={(e) => setSearchOrder(e.target.value)}
          />
        </div>

        <div className="field-group">
          <label>Filter Status</label>
          <select
            className="text-input"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option>All</option>
            <option>Delivered</option>
            <option>Shipped</option>
            <option>Cancelled</option>
          </select>
        </div>
      </div>

      <DataTable
        columns={columns}
        rows={filtered.map((o) => ({ ...o, id: o.orderId }))}
      />
    </div>
  );
}
