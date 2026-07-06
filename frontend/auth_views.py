import streamlit as st
from backend.validators import is_valid_gmail

def page_login(navigate):
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown('<div class="hero-brand">🏠 BachelorNest</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="font-size:2.8rem; font-weight:800; color:white; line-height:1.2; margin-bottom:1rem;">Find your perfect bachelor pad in India</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:1.1rem; color:#f1f5f9; margin-bottom:2.5rem; opacity:0.9;">Affordable rooms, PGs, and flats for students and working professionals.</p>', unsafe_allow_html=True)
        
        stat_cols = st.columns(3)
        stat_cols[0].markdown('<h3>10+</h3><p style="color:#f1f5f9;font-size:0.9rem;">Listings</p>', unsafe_allow_html=True)
        stat_cols[1].markdown('<h3>5</h3><p style="color:#f1f5f9;font-size:0.9rem;">Cities</p>', unsafe_allow_html=True)
        stat_cols[2].markdown('<h3>4.8★</h3><p style="color:#f1f5f9;font-size:0.9rem;">Rating</p>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<h2>Welcome back</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b; margin-bottom:2rem;">Sign in to continue your search</p>', unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="you@example.com", key="login_email_input")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass_input")
        
        if st.button("Sign In →", use_container_width=True, type="primary", key="login_submit_btn"):
            user_found = None
            for u in st.session_state.users:
                if u.get("email") == email.strip() and u.get("password") == password:
                    user_found = u
                    break
            
            if user_found:
                st.session_state.logged_in = True
                st.session_state.current_user = user_found["username"]
                st.session_state.user_role = user_found["role"]
                
                if user_found["role"] == "landlord":
                    navigate("landlord_dashboard")
                else:
                    navigate("student_dashboard")
                st.rerun()
            else:
                st.error("Invalid credentials.")
                
        st.markdown('<p style="text-align:center; margin-top:2rem; color:#64748b;">Don\'t have an account?</p>', unsafe_allow_html=True)
        if st.button("Sign up free", key="go_to_signup_btn"):
            navigate("signup")
            st.rerun()

def page_signup(navigate):
    st.markdown('<h2 style="text-align:center;">Create Your Account</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Choose Username", placeholder="e.g. samasai")
        email = st.text_input("Gmail Address", placeholder="name@gmail.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
    with col2:
        phone = st.text_input("WhatsApp Phone Number", placeholder="e.g. +91 9876543210")
        age = st.number_input("Your Age", min_value=18, max_value=100, value=20)
        role = st.selectbox("I want to:", ["Find a Home (Student)", "List Property (Landlord)"])
        
    if st.button("Complete Registration", use_container_width=True, type="primary"):
        if not username or not email or not password or not phone:
            st.error("All parameters are mandatory.")
            return
        if not is_valid_gmail(email):
            st.error("Registration requires a valid @gmail.com address.")
            return
        if any(u.get("username") == username for u in st.session_state.users):
            st.error("Username already taken!")
            return
            
        selected_role = "landlord" if "Landlord" in role else "student"
        
        new_profile = {
            "username": username.strip(),
            "email": email.strip(),
            "password": password,
            "phone": phone.strip(),
            "age": int(age),
            "role": selected_role,
            "favorites": []
        }
        
        st.session_state.users.append(new_profile)
        from backend.database import save_users
        save_users()
        
        st.success("Registration success! Please sign in.")
        navigate("login")
        st.rerun()
        
    if st.button("← Return to Sign In"):
        navigate("login")
        st.rerun()