import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import { Alert } from "./UI";

// requiredGroup mirrors the `if st.session_state.get("group") != "X": st.error(...)` checks
// in each Streamlit page.
export default function ProtectedRoute({ requiredGroup }) {
  const { loggedIn, group } = useAuth();

  if (!loggedIn) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="shell">
      <Sidebar />

      <div className="main">
        <Topbar />

        <div className="content">
          {requiredGroup && group !== requiredGroup ? (
            <Alert type="error">Unauthorized</Alert>
          ) : (
            <Outlet />
          )}
        </div>
      </div>
    </div>
  );
}
