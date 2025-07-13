# common.py
import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# ─── Supabase setup ─────────────────────────────
load_dotenv("supabase.env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Session‐state defaults ──────────────────────
st.session_state.setdefault("dm_finished", False)
st.session_state.setdefault("answers", {})

# ─── Sidebar CSS hook ───────────────────────────
def hide_sidebar_if_participant():
    if (
        st.session_state.get("user_role") == "participant"
        and st.session_state.get("simulation_id")
    ):
        st.markdown(
            """
            <style>
              /* Hide entire Streamlit sidebar */
              .css-1d391kg { display: none; }
              /* Let main content expand */
              .css-1v0mbdj { margin-left: 0; }
            </style>
            """,
            unsafe_allow_html=True,
        )

# ─── Global menu ─────────────────────────────────
def render_sidebar_menu():
    """
    Draws the “New / Running / Past / Control Center” menu
    in the sidebar, on every page except when hidden above.
    """
    # If hidden by CSS, bail out
    if (
        st.session_state.get("user_role") == "participant"
        and st.session_state.get("simulation_id")
    ):
        return

    role = st.session_state.get("user_role", "participant")
    st.sidebar.header("Main Menu")

    # Build menu items with callbacks
    items = [
        ("➕ New Simulation", _nav_new_sim),
        ("🏃 Ongoing Simulations", lambda: st.experimental_set_query_params(page="running_simulations")),
        ("📜 Past Simulations",   lambda: st.experimental_set_query_params(page="past_simulations")),
    ]
    if role == "administrator":
        items.append(("⚙️ Control Center", lambda: st.experimental_set_query_params(page="control_center")))

    choice = st.sidebar.radio("Go to:", [label for label,_ in items])
    for label, cb in items:
        if label == choice:
            cb()
            st.experimental_rerun()
            break

def _nav_new_sim():
    role = st.session_state.get("user_role")
    if role == "participant":
        st.query_params["participant_new_simulation"]
    elif role == "supervisor":
        st.query_params["supervisor_menu"]
    elif role == "administrator":
        st.query_params["control_center"]
