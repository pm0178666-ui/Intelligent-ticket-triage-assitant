import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const http = axios.create({
  baseURL: BASE_URL,
});

// POST TICKET (Creating ticket)
export async function createTicket(payload) {
  try {
    const response = await http.post("/tickets", payload);
    return response.data;
  } catch (e) {
    throw new Error(`Failed to create ticket: ${describeError(e)}`);
  }
}

// GET TICKETS (Fetching tickets)
export async function getTickets() {
  const response = await http.get("/tickets");
  return response.data;
}

// GET TICKET BY ID (Each ticket)
export async function getTicketById(ticketId) {
  const response = await http.get(`/tickets/${ticketId}`);
  return response.data;
}

export async function getApprovals() {
  const response = await http.get("/approvals");
  return response.data;
}

export async function approveRequest(approvalId) {
  const response = await http.get("/approve", {
    params: { approvalId, action: "approve" },
  });
  return response.data;
}

export async function rejectRequest(approvalId) {
  const response = await http.get("/reject", {
    params: { approvalId, action: "reject" },
  });
  return response.data;
}

// GET ORDERS
export async function getOrders() {
  const response = await http.get("/orders");
  return response.data;
}

function describeError(e) {
  return e.response?.data?.message || e.message || String(e);
}
