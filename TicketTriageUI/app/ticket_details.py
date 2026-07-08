import streamlit as st
from datetime import datetime

from services.api_client import get_ticket_by_id


def format_datetime(date_string):

    if not date_string:
        return "N/A"

    return datetime.fromisoformat(
        date_string.replace("Z", "")
    ).strftime("%d %b %Y • %I:%M %p")


def show():

    # =====================================================
    # AUTHENTICATION
    # =====================================================

    if not st.session_state.get("logged_in", False):
        st.error("Login Required")
        st.stop()

    st.title("Ticket Details")
    st.caption("Search and view complete ticket information.")

    st.divider()

    # =====================================================
    # SEARCH SECTION
    # =====================================================

    default_ticket = st.session_state.get(
        "selected_ticket_id",
        ""
    )

    col1, col2 = st.columns([5, 1])

    with col1:

        ticket_id = st.text_input(
            "Ticket ID",
            value=default_ticket,
            placeholder="Enter Ticket ID"
        )

    with col2:

        st.write("")
        st.write("")

        load_ticket = st.button(
            "Load Ticket",
            use_container_width=True
        )

    # Automatically load when coming from My Tickets
    if default_ticket and not load_ticket:
        load_ticket = True

    if not load_ticket:

        st.info(
            "Enter a Ticket ID and click 'Load Ticket'."
        )

        st.stop()

    if not ticket_id:

        st.warning(
            "Please enter a Ticket ID."
        )

        st.stop()

    st.session_state.selected_ticket_id = ticket_id

    # =====================================================
    # FETCH DATA
    # =====================================================

    try:

        ticket = get_ticket_by_id(ticket_id)

    except Exception:

        st.error(
            "Ticket not found."
        )

        st.stop()

    st.divider()

    # =====================================================
    # CUSTOMER INFORMATION
    # =====================================================

    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Customer Name:** {ticket.get('customerName','N/A')}"
        )

    with col2:

        st.write(
            f"**Customer Email:** {ticket.get('customerEmail','N/A')}"
        )

    st.divider()

    # =====================================================
    # TICKET INFORMATION
    # =====================================================

    st.subheader("Ticket Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Ticket ID:** {ticket.get('ticketId','N/A')}"
        )

        st.write(
            f"**Subject:** {ticket.get('subject','N/A')}"
        )

        st.write(
            f"**Status:** {ticket.get('status','N/A').title()}"
        )

    with col2:

        st.write(
            f"**Created On:** {format_datetime(ticket.get('createdAt'))}"
        )

        st.write(
            f"**Updated On:** {format_datetime(ticket.get('updatedAt'))}"
        )

    st.divider()

    # =====================================================
    # ISSUE DESCRIPTION
    # =====================================================

    st.subheader("Issue Description")

    st.info(
        ticket.get(
            "message",
            "No description available."
        )
    )

    st.divider()

    # =====================================================
    # AI ANALYSIS
    # =====================================================

    st.subheader("AI Analysis")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Category",
            ticket.get("category", "N/A")
        )

    with c2:

        st.metric(
            "Priority",
            ticket.get("priority", "N/A")
        )

    with c3:

        st.metric(
            "Sentiment",
            ticket.get("sentiment", "N/A")
        )

    with c4:

        st.metric(
            "Complexity",
            ticket.get("complexity", "N/A")
        )

    st.divider()

    # =====================================================
    # AI RESPONSE
    # =====================================================

    st.subheader("AI Generated Response")

    with st.container(border=True):

        st.markdown(
            ticket.get(
                "draftResponse",
                "No response generated."
            )
        )

    st.divider()

    # =====================================================
    # SEARCH AGAIN
    # =====================================================

    if st.button(
        "Search Another Ticket",
        use_container_width=True
    ):

        st.session_state.selected_ticket_id = ""

        st.rerun()