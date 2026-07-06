import streamlit as st
from backend.database import load_persisted_data
from frontend.styles import inject_global_css
from frontend.auth_views import page_login, page_signup
from frontend.dashboards import (
    render_student_dashboard, 
    render_favorites_dashboard, 
    render_property_details, 
    render_landlord_dashboard
)

# 1. Initialize Window Metadata Layout Frame
st.set_page_config(page_title="BachelorNest", layout="wide", initial_sidebar_state="expanded")
inject_global_css()

# 2. Initialize In-Memory Session Variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state: 
    st.session_state.current_user = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "page" not in st.session_state: 
    st.session_state.page = "login"

load_persisted_data()

def navigate(target_page):
    st.session_state.page = target_page

# 3. Global Top Navigation Component
def render_header_navigator():
    role_lbl = f" ({st.session_state.user_role.upper()})" if st.session_state.user_role else ""
    st.markdown(f"""
    <div class="custom-navbar">
        <div class="nav-logo">🏠 BachelorNest <span style="font-size:0.9rem; color:#64748b; font-weight:400;">Active Session: <b>{st.session_state.current_user}{role_lbl}</b></span></div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns([1, 1, 1, 1, 4])
    if cols[0].button("🔍 Marketplace Grid", key="nav_home"): 
        navigate("student_dashboard")
        st.rerun()
    if cols[1].button("❤️ My Favorites", key="nav_fav"): 
        navigate("favorites") 
        st.rerun()
    if cols[2].button("➕ Add Property", key="nav_add"): 
        navigate("landlord_dashboard")
        st.rerun()
    if cols[3].button("🚪 Disconnect Session", key="nav_exit"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.user_role = None
        navigate("login")
        st.rerun()

# 4. Core Core Orchestrator Controller Execution Block Loop
def orchestrator():
    if not st.session_state.logged_in:
        if st.session_state.page == "signup":
            page_signup(navigate)
        else:
            page_login(navigate)
    else:
        # Prevent unauthorized view tracking
        if st.session_state.page in ("login", "signup"):
            navigate("landlord_dashboard" if st.session_state.user_role == "landlord" else "student_dashboard")
            st.rerun()
            
        render_header_navigator()
        
        if st.session_state.page == "student_dashboard":
            render_student_dashboard(navigate)
        elif st.session_state.page == "favorites":
            render_favorites_dashboard()
        elif st.session_state.page == "property_details":
            render_property_details(navigate)
        elif st.session_state.page == "landlord_dashboard":
            render_landlord_dashboard(navigate)

if __name__ == "__main__":
    orchestrator()