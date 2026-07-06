import json
import os
import streamlit as st

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
LISTINGS_FILE = os.path.join(DATA_DIR, "listings.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_persisted_data():
    ensure_data_dir()
    # Read User Accounts
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                st.session_state.users = json.load(f)
        except Exception:
            st.session_state.users = []
    else:
        st.session_state.users = []

    # Read Property Index
    if os.path.exists(LISTINGS_FILE):
        try:
            with open(LISTINGS_FILE, "r", encoding="utf-8") as f:
                st.session_state.listings = json.load(f)
        except Exception:
            st.session_state.listings = []
    else:
        st.session_state.listings = []

def save_users():
    ensure_data_dir()
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.users, f, indent=2)

def save_listings():
    ensure_data_dir()
    with open(LISTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.listings, f, indent=2)