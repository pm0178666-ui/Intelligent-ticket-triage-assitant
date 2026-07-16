import { useNavigate } from "react-router-dom";
import {
  Sparkles,
  PlusCircle,
  ListChecks,
  Search,
  LayoutDashboard,
  Package,
  CheckSquare,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

const customerFeatures = [
  { icon: PlusCircle, title: "Create Ticket", desc: "Submit a new support request.", to: "/create-ticket" },
  { icon: ListChecks, title: "My Tickets", desc: "View and monitor all your submitted tickets.", to: "/my-tickets" },
  { icon: Search, title: "Ticket Details", desc: "Search any ticket using its Ticket ID.", to: "/ticket-details" },
];

const supportFeatures = [
  { icon: LayoutDashboard, title: "Support Dashboard", desc: "Review AI processed support tickets.", to: "/support-dashboard" },
  { icon: Package, title: "Orders Dashboard", desc: "Monitor customer orders and refund requests.", to: "/orders-dashboard" },
  { icon: CheckSquare, title: "Approval Dashboard", desc: "Approve or reject pending operational requests.", to: "/approval-dashboard" },
];

const customerSteps = ["Create Ticket", "AI Analysis", "Support Review", "Resolution"];
const supportSteps = ["Receive Tickets", "AI Prioritization", "Review & Approval", "Customer Resolution"];

export default function Home() {
  const { group } = useAuth();
  const navigate = useNavigate();
  const isCustomer = group === "CUSTOMER";

  const features = isCustomer ? customerFeatures : supportFeatures;
  const steps = isCustomer ? customerSteps : supportSteps;

  return (
    <div>
      <div className="welcome-banner">
        <div className="eyebrow">
          <Sparkles size={13} />
          {isCustomer ? "Customer Portal" : "Operations Portal"}
        </div>

        {isCustomer ? (
          <>
            <h2>Customer Support Portal</h2>
            <p>
              Welcome! Submit support requests, track ticket progress, and
              view AI-generated ticket analysis.
            </p>
          </>
        ) : (
          <>
            <h2>Support Operations Portal</h2>
            <p>
              Manage support operations, monitor AI ticket analysis, review
              customer orders, and approve pending requests.
            </p>
          </>
        )}
      </div>

      <div className="section-heading">
        <h3>{isCustomer ? "Quick Access" : "Operations"}</h3>
      </div>

      <div className="feature-grid">
        {features.map(({ icon: Icon, title, desc, to }) => (
          <div key={title} className="feature-card" onClick={() => navigate(to)}>
            <div className="icon-badge">
              <Icon size={20} />
            </div>
            <h3>{title}</h3>
            <p>{desc}</p>
          </div>
        ))}
      </div>

      <hr />

      <div className="section-heading">
        <h3>Workflow</h3>
      </div>

      <div className="stepper">
        {steps.map((step, i) => (
          <div key={step} className="stepper-step">
            <div className="stepper-index">{i + 1}</div>
            <div className="label">{step}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
