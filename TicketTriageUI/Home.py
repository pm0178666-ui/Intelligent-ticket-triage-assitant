import streamlit as st
import boto3
import jwt
from app import create_ticket
from app import my_tickets
from app import ticket_details
from app import support_dashboard
from app import approval_dashboard
from app import orders_dashboard

from pathlib import Path


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Ticket Triage Assistant",
    page_icon="🎫",
    layout="wide"
)



# =====================================================
# CSS
# =====================================================

css_path = Path(__file__).parent / "assets" / "style.css"

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()






# =====================================================
# HIDE DEFAULT STREAMLIT NAVIGATION
# =====================================================

st.markdown("""
<style>

/* Hide ONLY the default multipage navigation */
[data-testid="stSidebarNav"] {
    display: none !important;
}    

</style>

""", unsafe_allow_html=True)



# =====================================================
# COGNITO CONFIG
# =====================================================

CLIENT_ID = "1am1r9q8r3ih6i2e4llqov93kb"

client = boto3.client(
    "cognito-idp",
    region_name="us-east-1"
)

# =====================================================
# LOGIN FUNCTION
# =====================================================

def login(username, password):

    response = client.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )

    return response


# =====================================================
# LOGIN SCREEN
# =====================================================

if not st.session_state.get("logged_in", False):

    st.title("Ticket Triage Assistant")

    st.subheader("Login")

    username = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:

            response = login(
                username,
                password
            )

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.email = username

            id_token = response[
                "AuthenticationResult"
            ]["IdToken"]

            decoded_token = jwt.decode(
                id_token,
                options={
                    "verify_signature": False
                }
            )

            groups = decoded_token.get(
                "cognito:groups",
                []
            )

            if "supportTeam" in groups:

                st.session_state.group = "SUPPORT"

            elif "Users" in groups:

                st.session_state.group = "CUSTOMER"

            else:

                st.session_state.group = "UNKNOWN"

            st.success("Login Successful")

            st.session_state.page = "home"

            st.rerun()

        except Exception as e:

            st.error(str(e))

    st.stop()

    if "page" not in st.session_state:
        st.session_state.page = "home"



# =====================================================
# TOP NAVIGATION BAR
# =====================================================

col1, col2, col3, col4 = st.columns([5, 1, 2, 1])

with col1:
    st.markdown("## Ticket Triage Assistant")

with col2:
    if st.button("Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

with col3:
    st.markdown(
        f"""
        <div style='text-align:center;padding-top:8px;'>
        👤 <b>{st.session_state.group}</b><br>
        <span style='font-size:12px;'>{st.session_state.username}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.divider()



# =====================================================
# NAVIGATION BUTTONS
# =====================================================

if st.session_state.group == "CUSTOMER":

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Create Ticket", use_container_width=True):
            st.session_state.page = "create_ticket"
            st.rerun()

    with col2:
        if st.button("My Tickets", use_container_width=True):
            st.session_state.page = "my_tickets"
            st.rerun()

    with col3:
        if st.button("Ticket Details", use_container_width=True):
            st.session_state.page = "ticket_details"
            st.rerun()

elif st.session_state.group == "SUPPORT":

    col1, col2, col3 = st.columns(3)


    with col1:
        if st.button("Support Dashboard", use_container_width=True):
            st.session_state.page = "support_dashboard"
            st.rerun()

    with col2:
        if st.button("Orders Dashboard", use_container_width=True):
            st.session_state.page = "orders_dashboard"
            st.rerun()

    with col3:
        if st.button("Approval Dashboard", use_container_width=True):
            st.session_state.page = "approval_dashboard"
            st.rerun()

st.divider()




# =====================================================
# HOME PAGE
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

page = st.session_state.page
if page == "home":
    
    if st.session_state.group == "CUSTOMER":

        st.markdown("""
        <div class="welcome-banner">
            <h2>Customer Support Portal</h2>
            <p>
            Welcome! Submit support requests, track ticket progress,
            and view AI-generated ticket analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Quick Access")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card">
            <h3>Create Ticket</h3>
            <p>Submit a new support request.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
            <h3>My Tickets</h3>
            <p>View and monitor all your submitted tickets.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card">
            <h3>Ticket Details</h3>
            <p>Search any ticket using its Ticket ID.</p>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="welcome-banner">
            <h2>Support Operations Portal</h2>
            <p>
            Manage support operations, monitor AI ticket analysis,
            review customer orders, and approve pending requests.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Operations")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card">
            <h3>Support Dashboard</h3>
            <p>Review AI processed support tickets.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
            <h3>Orders Dashboard</h3>
            <p>Monitor customer orders and refund requests.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card">
            <h3>Approval Dashboard</h3>
            <p>Approve or reject pending operational requests.</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    st.subheader("Workflow")

    if st.session_state.group == "CUSTOMER":

        c1, c2, c3, c4 = st.columns(4)

        c1.success("\n\nCreate Ticket")
        c2.success("\n\nAI Analysis")
        c3.success("\n\nSupport Review")
        c4.success("\n\nResolution")

    else:

        c1, c2, c3, c4 = st.columns(4)

        c1.success("\n\nReceive Tickets")
        c2.success("\n\nAI Prioritization")
        c3.success("\n\nReview & Approval")
        c4.success("\n\nCustomer Resolution")


elif page == "create_ticket":
    create_ticket.show()

elif page == "my_tickets":
    my_tickets.show()

elif page == "ticket_details":
    ticket_details.show()

elif page == "support_dashboard":
    support_dashboard.show()

elif page == "orders_dashboard":
    orders_dashboard.show()

elif page == "approval_dashboard":
    approval_dashboard.show()