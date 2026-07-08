import streamlit as st
import pandas as pd

from services.api_client import get_orders


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

    st.title("Orders Dashboard")

    try:

        # =====================================================
        # FETCH ORDERS
        # =====================================================

        orders = get_orders()

        # =====================================================
        # METRICS
        # =====================================================

        total_orders = len(orders)

        delivered_orders = sum(
            1
            for order in orders
            if order.get("status", "").lower() == "delivered"
        )

        shipped_orders = sum(
            1
            for order in orders
            if order.get("status", "").lower() == "shipped"
        )

        cancelled_orders = sum(
            1
            for order in orders
            if order.get("status", "").lower() == "cancelled"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Orders",
                total_orders
            )

        with col2:
            st.metric(
                "Delivered",
                delivered_orders
            )

        with col3:
            st.metric(
                "Shipped",
                shipped_orders
            )

        with col4:
            st.metric(
                "Cancelled",
                cancelled_orders
            )

        st.divider()

        # =====================================================
        # FILTERS
        # =====================================================

        col1, col2 = st.columns(2)

        with col1:

            search_order = st.text_input(
                "Search Order ID"
            )

        with col2:

            status_filter = st.selectbox(
                "Filter Status",
                [
                    "All",
                    "Delivered",
                    "Shipped",
                    "Cancelled"
                ]
            )

        # =====================================================
        # APPLY FILTERS
        # =====================================================

        filtered_orders = orders

        if search_order:

            filtered_orders = [
                order
                for order in filtered_orders
                if search_order.lower()
                in order.get(
                    "orderId",
                    ""
                ).lower()
            ]

        if status_filter != "All":

            filtered_orders = [
                order
                for order in filtered_orders
                if order.get(
                    "status",
                    ""
                ).lower()
                ==
                status_filter.lower()
            ]

        # =====================================================
        # TABLE
        # =====================================================

        if filtered_orders:

            df = pd.DataFrame(
                filtered_orders
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No orders found."
            )

    except Exception as e:

        st.error(
            f"Failed to load orders: {e}"
        )