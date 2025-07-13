# pages/2_Welcome.py
import streamlit as st
from common import hide_sidebar_if_participant, render_sidebar_menu, show_logos

# 1) Must be first Streamlit command in this file
st.set_page_config(page_title="Welcome", layout="wide")

# 2) Hide sidebar for in-sim participants
hide_sidebar_if_participant()

# 3) Draw your Main Menu
render_sidebar_menu()

# --- now your existing welcome-page body ---
show_logos([
    ("Logo_CHIRON.png", 90),
    ("IDEAS_LAB.png",    180),
    ("Novologofct2021.png", 150),
])

st.title("Welcome to CHIRON System")
role = st.session_state.get("user_role", "participant")
st.markdown(f"**You are logged in as:** `{role}`")
st.markdown("---")
st.write("Use the sidebar to navigate…")
