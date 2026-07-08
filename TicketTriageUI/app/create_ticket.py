import streamlit as st

from services.api_client import create_ticket


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

    col1, col2 = st.columns([1, 6])

    with col1:

        if st.button("⬅ Back", key="back_create"):

            st.session_state.page = "home"

            st.rerun()

    with col2:

        st.title("Create Support Ticket")

    st.caption(
        "Submit your issue to our AI-powered support system."
    )

    st.divider()

    # =====================================================
    # TICKET FORM
    # =====================================================

    with st.container(border=True):

        st.subheader("Ticket Information")

        with st.form("ticket_form"):

            customer_name = st.text_input(
                "Customer Name",
                placeholder="Enter your full name"
            )

            customer_email = st.text_input(
                "Customer Email",
                placeholder="Enter your email address"
            )

            subject = st.text_input(
                "Issue Summary",
                placeholder="Briefly describe your issue"
            )

            message = st.text_area(
                "Describe Your Issue",
                height=180,
                placeholder="Explain your issue in detail..."
            )

            attachment = st.file_uploader(
                "Attachment (Optional)"
            )

            st.write("")

            submit_button = st.form_submit_button(
                "Create Ticket",
                use_container_width=True
            )

    # =====================================================
    # FORM VALIDATION
    # =====================================================

    if submit_button:

        if not customer_name.strip():

            st.error("Customer Name is required.")

        elif not customer_email.strip():

            st.error("Customer Email is required.")

        elif not subject.strip():

            st.error("Issue Summary is required.")

        elif not message.strip():

            st.error("Issue Description is required.")

        else:

            payload = {

                "customerName": customer_name,

                "customerEmail": customer_email,

                "subject": subject,

                "message": message

            }

            try:

                result = create_ticket(payload)

                st.success("Ticket Created Successfully!")

                st.divider()

                col1, col2 = st.columns(2)

                with col1:

                    st.info(
                        f"**Ticket ID**\n\n{result['ticketId']}"
                    )

                with col2:

                    st.info(
                        f"**Current Status**\n\n{result['status']}"
                    )

                st.success(
                    "You can monitor your ticket status and AI response anytime from the **My Tickets** page."
                )

            except Exception as e:

                st.error(f"Failed to create ticket.\n\n{str(e)}")