import { useLocation } from "react-router-dom";

const TITLES = {
  "/": "Home",
  "/create-ticket": "Create Ticket",
  "/my-tickets": "My Tickets",
  "/ticket-details": "Ticket Details",
  "/support-dashboard": "Support Dashboard",
  "/orders-dashboard": "Orders Dashboard",
  "/approval-dashboard": "Approval Dashboard",
};

export default function Topbar() {
  const { pathname } = useLocation();
  const title = TITLES[pathname] || "Ticket Triage Assistant";

  return (
    <header className="topbar">
      <div className="topbar-title">{title}</div>
    </header>
  );
}
