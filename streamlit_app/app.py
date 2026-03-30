import streamlit as st
from api_client import api

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Finance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Authentication State ---
if 'token' not in st.session_state:
    st.session_state['token'] = None

def render_login():
    st.title("💸 AI Finance Dashboard")
    st.markdown("Please log in to your account.")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Logging in..."):
                    try:
                        res = api.login(email, password)
                        st.session_state['token'] = res.get("access_token")
                        st.success("Logged in successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Login failed: {str(e)}")

# --- Main App Logic ---
if not st.session_state['token']:
    render_login()
else:
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    
    # Define pages
    pages = {
        "📊 Dashboard": "pages/dashboard.py",
        "💼 Portfolio": "pages/portfolio.py",
        "📝 Transactions": "pages/transactions.py",
        "🤖 AI Analytics": "pages/analytics.py"
    }

    # Streamlit Navigation (st.navigation for 1.36+ or custom routing)
    try:
        # Streamlit 1.36+ native navigation
        pgs = [st.Page(v, title=k) for k, v in pages.items()]
        pg = st.navigation(pgs)
        
        # Logout button in sidebar
        with st.sidebar:
            st.divider()
            if st.button("Logout", use_container_width=True):
                st.session_state['token'] = None
                st.rerun()
                
        pg.run()
    except AttributeError:
        # Fallback for older Streamlit versions
        st.error("Streamlit version too old. Please upgrade to >1.36 for st.navigation support.")
        # Alternatively, we could write a manual router here.
