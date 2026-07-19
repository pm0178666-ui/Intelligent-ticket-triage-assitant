import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import VerifyOtp from "./pages/VerifyOtp";
import Home from "./pages/Home";
import CreateTicket from "./pages/CreateTicket";
import MyTickets from "./pages/MyTickets";
import TicketDetails from "./pages/TicketDetails";
import SupportDashboard from "./pages/SupportDashboard";
import OrdersDashboard from "./pages/OrdersDashboard";
import ApprovalDashboard from "./pages/ApprovalDashboard";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/verify-otp" element={<VerifyOtp />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Home />} />
        <Route path="/ticket-details" element={<TicketDetails />} />
      </Route>

      <Route element={<ProtectedRoute requiredGroup="CUSTOMER" />}>
        <Route path="/create-ticket" element={<CreateTicket />} />
        <Route path="/my-tickets" element={<MyTickets />} />
      </Route>

      <Route element={<ProtectedRoute requiredGroup="SUPPORT" />}>
        <Route path="/support-dashboard" element={<SupportDashboard />} />
        <Route path="/orders-dashboard" element={<OrdersDashboard />} />
        <Route path="/approval-dashboard" element={<ApprovalDashboard />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
