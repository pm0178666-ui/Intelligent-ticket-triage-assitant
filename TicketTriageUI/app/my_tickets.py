import streamlit as st
from datetime import datetime

from services.api_client import get_tickets


def show():

    if not st.session_state.get("logged_in", False):
        st.error("Login Required")
        st.stop()

    if st.session_state.get("group") != "CUSTOMER":
        st.error("Unauthorized")
        st.stop()

    # =====================================================
    # HEADER
    # =====================================================

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("⬅ Back", key="back_tickets"):
            st.session_state.page = "home"
            st.rerun()

    with col2:
        st.title("My Tickets")

    try:

        # =====================================================
        # FETCH TICKETS
        # =====================================================

        tickets = get_tickets()


        logged_in_email = st.session_state.get("email")

        tickets = [
            ticket
            for ticket in tickets
            if ticket.get("customerEmail") == logged_in_email
        ]

        # =====================================================
        # SORT TICKETS
        # =====================================================

        tickets = sorted(
            tickets,
            key=lambda ticket: ticket.get("createdAt", ""),
            reverse=True
        )
        

        # =====================================================
        # METRICS
        # =====================================================

        total_tickets = len(tickets)

        processed_tickets = sum(
            1
            for ticket in tickets
            if ticket.get("status", "").lower() == "processed"
        )

        pending_tickets = total_tickets - processed_tickets

        # =====================================================
        # DESCRIPTION
        # =====================================================

        st.caption(
            "View and track all support tickets submitted by you."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Tickets",
                total_tickets
            )

        with col2:
            st.metric(
                "Processed",
                processed_tickets
            )

        with col3:
            st.metric(
                "Pending",
                pending_tickets
            )

        st.info(
            f"You have submitted {total_tickets} tickets."
        )

        st.divider()

        # =====================================================
        # NO TICKETS
        # =====================================================

        if total_tickets == 0:

            st.warning("You haven't created any tickets yet.")

            return

        # =====================================================
        # DISPLAY TICKETS
        # =====================================================

        for ticket in tickets:

            created_on = "N/A"

            if ticket.get("createdAt"):

                created_on = datetime.fromisoformat(
                    ticket["createdAt"].replace("Z", "")
                ).strftime("%d-%b-%Y %I:%M %p")

            with st.container(border=True):

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.subheader(
                        ticket.get("subject", "N/A")
                    )

                    st.write(
                        f"**Ticket ID:** {ticket.get('ticketId', 'N/A')}"
                    )

                    st.write(
                        f"**Status:** {ticket.get('status', 'N/A').title()}"
                    )

                    st.write(
                        f"**Created On:** {created_on}"
                    )

                with col2:

                    st.write("")

                    st.write("")

                    if st.button(
                        "View",
                        key=ticket["ticketId"]
                    ):

                        st.session_state.selected_ticket_id = ticket["ticketId"]

                        st.session_state.page = "ticket_details"

                        st.rerun()

    except Exception as e:

        st.error(
            f"Failed to load tickets: {str(e)}"
        )