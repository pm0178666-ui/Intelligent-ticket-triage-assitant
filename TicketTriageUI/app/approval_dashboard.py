import streamlit as st
from datetime import datetime

from services.api_client import (
    get_approvals,
    approve_request,
    reject_request
)


def format_date(date_string):

    if not date_string:
        return "N/A"

    return datetime.fromisoformat(
        date_string.replace("Z", "")
    ).strftime("%d %b %Y • %I:%M %p")


def show():

    if not st.session_state.get("logged_in", False):
        st.error("Login Required")
        st.stop()

    if st.session_state.get("group") != "SUPPORT":
        st.error("Unauthorized")
        st.stop()

    # ==========================================
    # HEADER
    # ==========================================

    header1, header2 = st.columns([8,1])

    with header1:

        st.title("Approval Dashboard")

        st.caption(
            "Manage refund and password reset approval requests."
        )

    with header2:

        if st.button(
            "Refresh",
            key="refresh_approval_dashboard",
            use_container_width=True
        ):
            st.rerun()

    st.divider()

    try:

        approvals = get_approvals()

        pending = [
            approval
            for approval in approvals
            if approval.get("status","").upper()=="PENDING"
        ]

        approved = [
            approval
            for approval in approvals
            if approval.get("status","").upper()=="APPROVED"
        ]

        rejected = [
            approval
            for approval in approvals
            if approval.get("status","").upper()=="REJECTED"
        ]

        # ==========================================
        # METRICS
        # ==========================================

        c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(
                "Pending",
                len(pending)
            )

        with c2:
            st.metric(
                "Approved",
                len(approved)
            )

        with c3:
            st.metric(
                "Rejected",
                len(rejected)
            )

        st.divider()

        # ==========================================
        # PENDING REQUESTS
        # ==========================================

        st.subheader("Pending Requests")

        if not pending:

            st.success(
                "No pending approval requests."
            )

        else:

            for approval in pending:

                payload = approval.get(
                    "payload",
                    {}
                )

                with st.container(border=True):

                    col1,col2 = st.columns([5,2])

                    with col1:

                        action = approval.get(
                            "actionType",
                            ""
                        )

                        if action == "PASSWORD_RESET":

                            st.markdown(
                                "### Password Reset Request"
                            )

                            st.write(
                                f"**Customer Email:** "
                                f"{payload.get('customerEmail','N/A')}"
                            )

                            st.write(
                                f"**Ticket ID:** "
                                f"{payload.get('ticketId','N/A')}"
                            )

                        elif action == "ISSUE_REFUND":

                            st.markdown(
                                "### Refund Request"
                            )

                            st.write(
                                f"**Order ID:** "
                                f"{payload.get('orderId','N/A')}"
                            )

                            st.write(
                                f"**Amount:** ₹"
                                f"{payload.get('amount','N/A')}"
                            )

                        else:

                            st.markdown(
                                f"### {action}"
                            )

                        st.caption(
                            f"Created : {format_date(approval.get('createdAt'))}"
                        )

                    with col2:

                        st.write("")

                        st.write("")

                        if st.button(
                            "Approve",
                            key=f"approve_{approval['approvalId']}",
                            use_container_width=True
                        ):

                            approve_request(
                                approval["approvalId"]
                            )

                            st.success(
                                "Request Approved."
                            )

                            st.rerun()

                        if st.button(
                            "Reject",
                            key=f"reject_{approval['approvalId']}",
                            use_container_width=True
                        ):

                            reject_request(
                                approval["approvalId"]
                            )

                            st.success(
                                "Request Rejected."
                            )

                            st.rerun()

        st.divider()


                # ==========================================
        # APPROVED REQUESTS
        # ==========================================

        with st.expander(
            f"Approved Requests ({len(approved)})",
            expanded=False
        ):

            if not approved:

                st.info(
                    "No approved requests."
                )

            else:

                for approval in approved:

                    payload = approval.get(
                        "payload",
                        {}
                    )

                    with st.container(border=True):

                        action = approval.get(
                            "actionType",
                            ""
                        )

                        col1, col2 = st.columns([5,1])

                        with col1:

                            if action == "PASSWORD_RESET":

                                st.markdown(
                                    "#### Password Reset"
                                )

                                st.write(
                                    f"**Customer Email:** {payload.get('customerEmail','N/A')}"
                                )

                                st.write(
                                    f"**Ticket ID:** {payload.get('ticketId','N/A')}"
                                )

                            elif action == "ISSUE_REFUND":

                                st.markdown(
                                    "#### Refund Request"
                                )

                                st.write(
                                    f"**Order ID:** {payload.get('orderId','N/A')}"
                                )

                                st.write(
                                    f"**Amount:** ₹{payload.get('amount','N/A')}"
                                )

                            else:

                                st.markdown(
                                    f"#### {action}"
                                )

                            st.caption(
                                f"Created : {format_date(approval.get('createdAt'))}"
                            )

                        with col2:

                            st.success("APPROVED")

        st.divider()

        # ==========================================
        # REJECTED REQUESTS
        # ==========================================

        with st.expander(
            f"Rejected Requests ({len(rejected)})",
            expanded=False
        ):

            if not rejected:

                st.info(
                    "No rejected requests."
                )

            else:

                for approval in rejected:

                    payload = approval.get(
                        "payload",
                        {}
                    )

                    with st.container(border=True):

                        action = approval.get(
                            "actionType",
                            ""
                        )

                        col1, col2 = st.columns([5,1])

                        with col1:

                            if action == "PASSWORD_RESET":

                                st.markdown(
                                    "#### Password Reset"
                                )

                                st.write(
                                    f"**Customer Email:** {payload.get('customerEmail','N/A')}"
                                )

                                st.write(
                                    f"**Ticket ID:** {payload.get('ticketId','N/A')}"
                                )

                            elif action == "ISSUE_REFUND":

                                st.markdown(
                                    "#### Refund Request"
                                )

                                st.write(
                                    f"**Order ID:** {payload.get('orderId','N/A')}"
                                )

                                st.write(
                                    f"**Amount:** ₹{payload.get('amount','N/A')}"
                                )

                            else:

                                st.markdown(
                                    f"#### {action}"
                                )

                            st.caption(
                                f"Created : {format_date(approval.get('createdAt'))}"
                            )

                        with col2:

                            st.error("REJECTED")

    except Exception as e:

        st.error(
            f"Failed to load approvals: {str(e)}"
        )