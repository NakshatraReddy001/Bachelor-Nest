import streamlit as st
import base64
from backend.validators import AMENITY_KEYS
from backend.database import save_listings, save_users

def get_active_profile():
    if st.session_state.current_user:
        for u in st.session_state.users:
            if u.get("username") == st.session_state.current_user:
                return u
    return {"favorites": []}

def render_student_dashboard(navigate):
    st.title("🔍 Find a Home")
    st.markdown(f"Displaying **{len(st.session_state.listings)}** premium listings.")
    
    # Left Sidebar Filter Core
    st.sidebar.markdown("### 🛠️ Filter Framework")
    all_cities = sorted(list({listing.get("city", "Other") for listing in st.session_state.listings}))
    city_choice = st.sidebar.selectbox("Target City", ["All Cities"] + all_cities)
    
    prices = [int(listing.get("price", 0)) for listing in st.session_state.listings]
    max_slider = max(prices) if prices else 100000
    budget = st.sidebar.slider("Rent Range (INR ₹)", 0, int(max_slider + 5000), (0, int(max_slider + 5000)))
    
    furnishing = st.sidebar.selectbox("Furnishing Status", ["Any Status", "Fully-Furnished", "Semi-Furnished", "Unfurnished"])
    selected_amenities = [a for a in AMENITY_KEYS if st.sidebar.checkbox(a, key=f"f_chk_{a}")]

    # Dynamic Filter Loop Processing
    filtered = []
    for listing in st.session_state.listings:
        if city_choice != "All Cities" and listing.get("city") != city_choice:
            continue
        if not (budget[0] <= int(listing.get("price", 0)) <= budget[1]):
            continue
        if furnishing != "Any Status" and listing.get("furnishing") != furnishing:
            continue
        if selected_amenities and not all(amt in listing.get("amenities", []) for amt in selected_amenities):
            continue
        filtered.append(listing)

    if not filtered:
        st.info("No options available matching those specific parameters.")
        return

    idx = 0
    profile = get_active_profile()
    
    # 3-Column Visual Grid
    for row in range((len(filtered) + 2) // 3):
        cols = st.columns(3)
        for c in range(3):
            if idx >= len(filtered):
                break
            item = filtered[idx]
            with cols[c]:
                img_tag = '<img src="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80"/>'
                if item.get("image_base64"):
                    img_tag = f'<img src="data:image/jpeg;base64,{item["image_base64"]}"/>'
                
                st.markdown(f"""
                <div class="listing-card">
                    <div class="card-img-container">
                        <span class="badge-type">{item.get("prop_type", "Room")}</span>
                        {img_tag}
                    </div>
                    <div class="card-content">
                        <div class="card-price">₹{int(item.get("price", 0)):,} <span style="font-size:0.85rem; font-weight:400; color:#64748b;">/ mo</span></div>
                        <div class="card-title">{item.get("title")}</div>
                        <div class="card-loc">📍 {item.get("locality")}, {item.get("city")}</div>
                        <div class="card-specs">
                            <span>🛏️ {item.get("bedrooms")} BHK</span>
                            <span>📐 {item.get("area")} sqft</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                act_cols = st.columns([2, 1])
                if act_cols[0].button("🔍 Details", key=f"det_{idx}_{item.get('title')}"):
                    st.session_state.selected_view_item = item
                    navigate("property_details")
                    st.rerun()
                    
                is_fav = item.get("title") in profile.get("favorites", [])
                fav_lbl = "❤️ Saved" if is_fav else "🖤 Save"
                if act_cols[1].button(fav_lbl, key=f"fav_{idx}_{item.get('title')}"):
                    if is_fav:
                        profile["favorites"].remove(item.get("title"))
                    else:
                        if "favorites" not in profile:
                            profile["favorites"] = []
                        profile["favorites"].append(item.get("title"))
                    save_users()
                    st.rerun()
            idx += 1

def render_favorites_dashboard():
    st.title("❤️ Your Saved Properties")
    profile = get_active_profile()
    fav_titles = profile.get("favorites", [])
    fav_listings = [listing for listing in st.session_state.listings if listing.get("title") in fav_titles]
    
    if not fav_listings:
        st.info("No properties bookmarked yet.")
        return
        
    idx = 0
    for row in range((len(fav_listings) + 2) // 3):
        cols = st.columns(3)
        for c in range(3):
            if idx >= len(fav_listings):
                break
            item = fav_listings[idx]
            with cols[c]:
                img_tag = '<img src="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80"/>'
                if item.get("image_base64"):
                    img_tag = f'<img src="data:image/jpeg;base64,{item["image_base64"]}"/>'
                st.markdown(f"""
                <div class="listing-card">
                    <div class="card-img-container">{img_tag}</div>
                    <div class="card-content">
                        <div class="card-price">₹{int(item.get("price",0)):,}</div>
                        <div class="card-title">{item.get("title")}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("💔 Remove", key=f"rem_{idx}", use_container_width=True):
                    profile["favorites"].remove(item.get("title"))
                    save_users()
                    st.rerun()
            idx += 1

def render_property_details(navigate):
    if "selected_view_item" not in st.session_state:
        st.warning("Context vector empty.")
        return
    item = st.session_state.selected_view_item
    
    if st.button("← Back to Grid"):
        navigate("student_dashboard")
        st.rerun()
        
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.header(item.get("title"))
        st.markdown(f"#### 📍 {item.get('locality')}, {item.get('city')}")
        
        if item.get("image_base64"):
            st.image(base64.b64decode(item["image_base64"]), use_column_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80", use_column_width=True)
            
        st.markdown("### Description")
        st.write(item.get("description"))
        st.markdown("### Included Amenities")
        st.write(", ".join([f"✅ {a}" for a in item.get("amenities", [])]))
        
    with col2:
        st.markdown(f"""
        <div style="background:white; border:1px solid #e2e8f0; border-radius:16px; padding:2rem; box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.05);">
            <h3 style="color:#e11d48; margin-top:0;">Financial Spec</h3>
            <h2>₹{int(item.get('price', 0)):,} <span style="font-size:1rem; font-weight:400; color:#64748b;">/ mo</span></h2>
            <hr/>
            <p><b>Furnishing:</b> {item.get('furnishing')}</p>
            <p><b>Area Size:</b> {item.get('area')} sqft</p>
            <p><b>Layout:</b> {item.get('bedrooms')} BHK</p>
            <hr/>
            <h4>👤 Owner Profile</h4>
            <p><b>Name:</b> {item.get('owner_name')}</p>
            <p><b>Age:</b> {item.get('owner_age')} yrs</p>
        </div>
        """, unsafe_allow_html=True)
        
        # WhatsApp URL Redirect API
        phone = str(item.get('owner_phone', '')).replace(" ", "").replace("-", "")
        wa_url = f"https://wa.me/{phone}?text=Interested%20in%20your%20property%20{item.get('title')}"
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; padding:0.75rem; background-color:#25D366; color:white; border:none; border-radius:8px; font-weight:600; cursor:pointer; margin-top:1rem;">💬 WhatsApp Owner</button></a>', unsafe_allow_html=True)

def render_landlord_dashboard(navigate):
    st.title("➕ List a New Property")
    with st.form("landlord_submission_form_optimized", clear_on_submit=True):
        st.markdown('<div class="form-section-header">Primary Ownership Profile</div>', unsafe_allow_html=True)
        col_o1, col_o2 = st.columns(2)
        owner_name = col_o1.text_input("Owner Name", placeholder="e.g. Nakshatra Goli")
        owner_age = col_o2.number_input("Owner Age", min_value=18, max_value=120, value=35)
        owner_phone = st.text_input("WhatsApp Contact Number", placeholder="+919876543210")
        
        st.markdown('<div class="form-section-header">Property Specifications</div>', unsafe_allow_html=True)
        title = st.text_input("Listing Title")
        description = st.text_area("Description")
        
        col_s1, col_s2 = st.columns(2)
        prop_type = col_s1.selectbox("Property Type", ["Apartment / Flat", "PG Accommodation", "Hostel Room", "Independent House"])
        furnishing = col_s2.selectbox("Furnishing Status", ["Semi-Furnished", "Fully-Furnished", "Unfurnished"])
        
        col_g1, col_g2 = st.columns(2)
        city = col_g1.text_input("City", placeholder="e.g. Hyderabad")
        locality = col_g2.text_input("Locality", placeholder="e.g. Madhapur")
        full_address = st.text_input("Full Address")
        
        col_d1, col_d2, col_d3 = st.columns(3)
        bedrooms = col_d1.selectbox("BHK Size", [1, 2, 3, 4])
        bathrooms = col_d2.selectbox("Bathrooms", [1, 2, 3])
        area = col_d3.number_input("Area (sqft)", value=700)
        
        price = st.number_input("Monthly Rent (INR ₹)", value=15000)
        uploaded_file = st.file_uploader("Upload Image Cover Asset", type=["jpg", "jpeg", "png"])
        
        st.markdown('**Amenities:**')
        amenities = [a for a in AMENITY_KEYS if st.checkbox(a, key=f"frm_a_{a}")]
        
        if st.form_submit_button("Publish Listing Entry", use_container_width=True):
            if not owner_name or not title or not city or not locality or not owner_phone:
                st.error("Mandatory form fields missing attributes.")
                return
                
            b64_str = ""
            if uploaded_file is not None:
                b64_str = base64.b64encode(uploaded_file.read()).decode("utf-8")
                
            new_listing = {
                "owner_name": owner_name, "owner_age": int(owner_age), "owner_phone": owner_phone.strip(),
                "title": title.strip(), "description": description.strip(), "prop_type": prop_type,
                "furnishing": furnishing, "city": city.strip(), "locality": locality.strip(),
                "full_address": full_address.strip(), "bedrooms": int(bedrooms), "bathrooms": int(bathrooms),
                "area": int(area), "price": float(price), "image_base64": b64_str, "amenities": amenities
            }
            st.session_state.listings.append(new_listing)
            save_listings()
            st.success("Property live on matrix! Redirecting...")
            navigate("student_dashboard")
            st.rerun()