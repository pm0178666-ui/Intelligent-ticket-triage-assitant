import streamlit as st
import pandas as pd
from datetime import datetime

from services.api_client import get_tickets


def show():
    if not st.session_state.get("logged_in", False):    
        st.error("Login Required")
        st.stop()

    if st.session_state.get("group") != "SUPPORT":
        st.error("Unauthorized")
        st.stop()


    # =====================================================
    # PAGE TITLE
    # =====================================================

    st.title("Support Dashboard")

    st.caption(
        "View, search and manage all customer support tickets."
    )

    # =====================================================
    # FETCH DATA
    # =====================================================

    try:

        tickets = get_tickets()

    except Exception as e:

        st.error(
            f"Failed to load tickets: {e}"
        )

        st.stop()

    # =====================================================
    # SORT NEWEST FIRST
    # =====================================================

    tickets = sorted(
        tickets,
        key=lambda ticket: ticket.get(
            "createdAt",
            ""
        ),
        reverse=True
    )

    # =====================================================
    # DASHBOARD METRICS
    # =====================================================

    total_tickets = len(tickets)

    processed_tickets = sum(
        1
        for ticket in tickets
        if ticket.get(
            "status",
            ""
        ).lower() == "processed"
    )

    pending_tickets = total_tickets - processed_tickets

    high_priority_tickets = sum(
        1
        for ticket in tickets
        if ticket.get(
            "priority",
            ""
        ).lower() == "high"
    )

    # =====================================================
    # METRIC CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Tickets",
            total_tickets
        )

    with col2:
        st.metric(
            "✅ Processed",
            processed_tickets
        )

    with col3:
        st.metric(
            "⏳ Pending",
            pending_tickets
        )

    with col4:
        st.metric(
            "🔥 High Priority",
            high_priority_tickets
        )

    st.divider()

    # =====================================================
    # FILTER FORM
    # =====================================================

    with st.form("ticket_filters"):

        st.subheader("Filters")

        col1, col2, col3 = st.columns(3)

        with col1:

            search_ticket = st.text_input(
                "Ticket ID"
            )

        with col2:

            status_filter = st.selectbox(
                "Status",
                [
                    "All",
                    "processed",
                    "pending"
                ]
            )

        with col3:

            priority_filter = st.selectbox(
                "Priority",
                [
                    "All",
                    "High",
                    "Medium",
                    "Low"
                ]
            )

        apply_filters = st.form_submit_button(
            "🔍"
        )

    # =====================================================
    # APPLY FILTERS
    # =====================================================

    filtered_tickets = tickets

    if apply_filters:

        if search_ticket:

            filtered_tickets = [

                ticket

                for ticket in filtered_tickets

                if search_ticket.lower()
                in ticket.get(
                    "ticketId",
                    ""
                ).lower()
            ]

        if status_filter != "All":

            filtered_tickets = [

                ticket

                for ticket in filtered_tickets

                if ticket.get(
                    "status",
                    ""
                ).lower()
                ==
                status_filter.lower()
            ]

        if priority_filter != "All":

            filtered_tickets = [

                ticket

                for ticket in filtered_tickets

                if ticket.get(
                    "priority",
                    ""
                ).lower()
                ==
                priority_filter.lower()
            ]

    # =====================================================
    # TABLE DATA
    # =====================================================

    table_data = []

    for ticket in filtered_tickets:

        created_on = "N/A"

        if ticket.get("createdAt"):

            created_on = datetime.fromisoformat(
                ticket["createdAt"].replace(
                    "Z",
                    ""
                )
            ).strftime(
                "%d-%b-%Y %I:%M %p"
            )

        table_data.append(
            {
                "Ticket ID":
                    ticket.get(
                        "ticketId",
                        "N/A"
                    ),

                "Customer":
                    ticket.get(
                        "customerName",
                        "N/A"
                    ),

                "Email":
                    ticket.get(
                        "customerEmail",
                        "N/A"
                    ),

                "Subject":
                    ticket.get(
                        "subject",
                        "N/A"
                    ),

                "Category":
                    ticket.get(
                        "category",
                        "N/A"
                    ),

                "Priority":
                    ticket.get(
                        "priority",
                        "N/A"
                    ),

                "Status":
                    ticket.get(
                        "status",
                        "N/A"
                    ),

                "Created On":
                    created_on
            }
        )

    # =====================================================
    # DISPLAY TABLE
    # =====================================================

    st.divider()

    st.subheader("All Support Tickets")

    st.caption(
        f"Showing {len(table_data)} ticket(s)"
    )

    df = pd.DataFrame(
        table_data
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )