import { NavLink, useNavigate } from "react-router-dom";
import {
  Ticket,
  Home,
  PlusCircle,
  ListChecks,
  Search,
  LayoutDashboard,
  Package,
  CheckSquare,
  LogOut,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

const customerLinks = [
  { to: "/", label: "Home", icon: Home, end: true },
  { to: "/create-ticket", label: "Create Ticket", icon: PlusCircle },
  { to: "/my-tickets", label: "My Tickets", icon: ListChecks },
  { to: "/ticket-details", label: "Ticket Details", icon: Search },
];

const supportLinks = [
  { to: "/", label: "Home", icon: Home, end: true },
  { to: "/support-dashboard", label: "Support Dashboard", icon: LayoutDashboard },
  { to: "/orders-dashboard", label: "Orders Dashboard", icon: Package },
  { to: "/approval-dashboard", label: "Approval Dashboard", icon: CheckSquare },
];

export default function Sidebar() {
  const { group, username, logout } = useAuth();
  const navigate = useNavigate();

  const links = group === "CUSTOMER" ? customerLinks : supportLinks;
  const initials = (username || "?").slice(0, 2).toUpperCase();

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">
          <Ticket size={18} />
        </div>
        <div>
          <div className="brand-name">Ticket Triage</div>
          <div className="brand-sub">Assistant</div>
        </div>
      </div>

      <div className="sidebar-section-label">
        {group === "CUSTOMER" ? "Customer" : "Operations"}
      </div>

      <nav className="sidebar-nav">
        {links.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => `sidebar-link${isActive ? " active" : ""}`}
          >
            <Icon size={17} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="user-chip">
          <div className="user-avatar">{initials}</div>
          <div className="user-meta">
            <div className="role">{group}</div>
            <div className="email">{username}</div>
          </div>
        </div>

        <button
          className="logout-btn"
          onClick={() => {
            logout();
            navigate("/login");
          }}
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </aside>
  );
}
