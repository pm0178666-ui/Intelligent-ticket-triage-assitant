import {
  CheckCircle2,
  Info,
  AlertTriangle,
  XCircle,
  ChevronRight,
  ArrowLeft,
} from "lucide-react";

const ALERT_ICONS = {
  success: CheckCircle2,
  info: Info,
  warning: AlertTriangle,
  error: XCircle,
};

export function Metric({ label, value, icon: Icon, tone = "" }) {
  return (
    <div className="metric-card">
      {Icon && (
        <div className={`icon-badge ${tone}`}>
          <Icon size={20} />
        </div>
      )}
      <div className="metric-body">
        <div className="metric-label">{label}</div>
        <div className="metric-value">{value}</div>
      </div>
    </div>
  );
}

export function Alert({ type = "info", children }) {
  const Icon = ALERT_ICONS[type] || Info;
  return (
    <div className={`alert alert-${type}`}>
      <Icon size={17} />
      <div>{children}</div>
    </div>
  );
}

export function Card({ children, hover = false, className = "" }) {
  return <div className={`card ${hover ? "card-hover" : ""} ${className}`}>{children}</div>;
}

export function Badge({ children, tone = "pending" }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

export function PageHeader({ title, subtitle, onBack, action }) {
  return (
    <div className="page-header">
      <div>
        {onBack && (
          <button className="page-header-back" onClick={onBack}>
            <ArrowLeft size={15} />
            Back
          </button>
        )}
        <h1>{title}</h1>
        {subtitle && <p className="caption" style={{ marginBottom: 0 }}>{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

export { ChevronRight };
