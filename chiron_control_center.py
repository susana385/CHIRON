# chiron_control_center.py
import streamlit as st
import data_simulation          # your wrapper now exposes run(simulation_name)               # sets st.session_state['teamwork_submitted']=True
import questionnaire1           # sets st.session_state['dm_finished']=True
import os, json
import pandas as pd
from questionnaire1 import show_initial_situation, decisions1to15, decision16_12A, decisions17to18_12B, decisions17to19_12C, decisions17to26
import base64
from questionnaire1 import apply_vital_consequences
import matplotlib.pyplot as plt
import numpy as np
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from supabase_client import supabase, auth 
from dotenv import load_dotenv
#from supabase_client import supabase
from datetime import datetime, timedelta, timezone
from questionnaire1 import get_inject_text
from reportlab.platypus import Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table as RLTable
from reportlab.platypus import Image as RLImage
from typing import Dict
import time, random
from postgrest.exceptions import APIError
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="CHIRON Control Center",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# local fallback
load_dotenv()

# url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
# key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

# #supabase = create_client(url, key)
# auth = supabase.auth

# Build a global map: inject ID → question text
# build a map from inject → generic prompt, and (inject, role) → role-specific prompt
@st.cache_data(ttl=2)
def fetch_snapshot(sim_id: str, last_answer_id: int):
    """
    Vai buscar:
      - Delta de answers com id > last_answer_id
      - Lista completa de participants (pouca cardinalidade)
      - Últimos vitals (limit para não crescer)
    TTL=2 evita chamadas repetidas em reruns rapidos.
    """
    # ANSWERS DELTA
    try:
        answers_delta = (supabase
            .from_("answers")
            .select("id,id_simulation, simulation_name, id_participant, participant_role, inject,answer_text, basic_life_support, primary_survey, secondary_survey, definitive_care, crew_roles_communication, systems_procedural_knowledge, response_seconds,penalty")
            .eq("id_simulation", sim_id)
            .gt("id", last_answer_id)
            .order("id")
            .execute()
            .data or [])

        # PARTICIPANTS
        participants = (supabase
            .from_("participant")
            .select("id,id_simulation, id_profile,participant_role,started_at, finished_at, current_inject, current_answer")
            .eq("id_simulation", sim_id)
            .execute()
            .data or [])
    except Exception as e:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="loading")
        return


    return {
        "answers_delta": answers_delta,
        "participants": participants
    }

@st.cache_data(ttl=60*10)
def load_sim_metadata(sim_id):
    return (supabase
        .from_("simulation")
        .select("id,created_at, name,roles_logged,status,started_at, finished_at")
        .eq("id", sim_id)
        .single()
        .execute()
        .data)

@st.cache_data(ttl=60)
def load_teamwork(sim_id):
    return (supabase
        .from_("teamwork")
        .select("id, leadership, teamwork, total, comments, updated_at")
        .eq("id_simulation", sim_id)
        .maybe_single()
        .execute()
        .data)

def sync_simulation_state(sim_id: str):
    ss = st.session_state
    ss.setdefault("answers_cache", [])          # deve ser lista se usas .extend
    ss.setdefault("answers_delta", [])          # lista de novos
    ss.setdefault("participants_cache", {})     # dict id_participant -> info
    ss.setdefault("last_answer_id", 0)
    ss.setdefault("last_snapshot_ts", 0.0)
    now = time.time()
    # Debounce adicional (opcional)
    if now - st.session_state.last_snapshot_ts < 0.4:
        return
    snap = fetch_snapshot(sim_id, st.session_state.last_answer_id)
    delta = snap["answers_delta"]
    if delta:
        st.session_state.answers_cache.extend(delta)
        st.session_state.last_answer_id = delta[-1]["id"]
    st.session_state.participants_cache = snap["participants"]
    st.session_state.last_snapshot_ts = now

def build_answer_index():
    # Mapa rápido: (id_participant, inject) -> answer_row
    idx = {}
    for a in st.session_state.answers_cache:
        idx[(a["id_participant"], a["inject"])] = a
    return idx

def get_fd_participant_id(sim_id: str):
    # procurar na cache de participants
    for p in st.session_state.participants_cache:
        if p["participant_role"] == "FD":
            return p["id"]
    return None

def get_fd_answer_prefix(inject_prefix: str, fd_id: int, answer_idx):
    # percorre chaves do índice para esse participante
    for (pid, inj), row in answer_idx.items():
        if pid == fd_id and inj.startswith(inject_prefix):
            return row.get("answer_text")
    return None

def count_answers_for_step(sim_id: str, step: str, answer_rows, key_decisions):
    """
    answer_rows: st.session_state.answers_cache (já filtrado por sim_id)
    """
    total = 0
    for a in answer_rows:
        if a["id_simulation"] != sim_id:
            continue
        if a["inject"] != step:
            continue
        # lógica inject vs decision:
        if step.startswith("Inject"):
            if a["answer_text"] == "DONE":
                total += 1
        else:
            if a["answer_text"] != "SKIP":
                total += 1
    # Needed para comparar depois externamente
    needed = 1 if any(step.startswith(k) for k in key_decisions) else 8
    return total, needed


inject_prompt_map = {}
try:
    all_blocks = [
        questionnaire1.decisions1to15,
        questionnaire1.decision16_12A,
        questionnaire1.decisions17to18_12B,
        questionnaire1.decisions17to19_12C,
        *questionnaire1.decisions17to26.values(),
    ]
    for block in all_blocks:
        for d in block:
            inj = d["inject"]
            # the generic text
            inject_prompt_map[(inj, None)] = d.get("text", "")
            # any role_specific overrides
            for role, details in d.get("role_specific", {}).items():
                inject_prompt_map[(inj, role)] = details.get("text", "")
except Exception as e:
    st.error(f"❌ Could not build prompt map: {e}")



#--------------------------------------------Page 1 - Login --------------------------------------
def page_login():

    show_logos([
        ("Logo_CHIRON.png", 90),
        ("IDEAS_LAB.png", 180),
        ("Novologofct2021.png", 150)
    ])

    st.title("Welcome to CHIRON System")
    st.write("""
    CHIRON towards the future of Deep-Space Medical Decision-Making!
    """)

    st.header("Login")
    login_id = st.text_input("Username or Email", key="login_id")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Log In"):
            if not login_id or not password:
                st.error("Please enter username/email and password.")
                return
            else:
            # detect if user entered an email address or a username
                if "@" in login_id:
                        auth_params = {"email": login_id, "password": password}
                else:
                        # look up their email by username
                    try:
                        prof = supabase.from_("profiles") \
                                    .select("email") \
                                    .eq("username", login_id) \
                                    .maybe_single().execute()
                    except Exception:
                        st.info("⏳ Loading… please wait a moment.")
                        st_autorefresh(interval=2000, limit=None, key="retry_answers")
                        return
                    if not getattr(prof, "data", None):
                        st.error("No such username.")
                        return

                    auth_params = {"email": prof.data["email"], "password": password}
                try:
                    signin = auth.sign_in_with_password(auth_params)
                except Exception as e:
                    st.error(f"Sign-in failed: {e}")
                
                    # fetch exactly one profile row
                try:
                    res = (
                        supabase
                        .from_("profiles")
                        .select("id, username, role, profile_type_code")
                        .eq("id", signin.user.id)
                        .single()
                        .execute()
                        )
                except Exception as e:
                    st.info("Could not load profile: {e}.⏳ Loading… please wait a moment.")
                    st_autorefresh(interval=2000, limit=None, key="retry_answers")
                    return
                
                profile = res.data
                if not profile:
                    st.error("❌ No profile found for this user.")
                    return
                st.session_state.user      = signin.user
                st.session_state.user_role = profile["role"]
                st.session_state.simulation_id   = None
                st.session_state.simulation_name = None
                st.session_state.participant_id  = None
                st.session_state.profile   = profile
                st.session_state.profile_id = signin.user.id
                st.session_state.answers_cache      = []
                st.session_state.last_answer_id     = 0
                st.session_state.participants_cache = []
                st.session_state.last_snapshot_ts   = 0.0
                nav_to("welcome")
    
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False

    if not st.session_state.show_signup:
        if st.button("Don’t have an account yet? Register here"):
            st.session_state.show_signup = True
    
    if st.session_state.show_signup:
        st.markdown("---")
        st.header("Sign Up")

        signup_user  = st.text_input("Choose a Username", key="signup_user")
        signup_email = st.text_input("Your Email", key="signup_email")
        signup_password = st.text_input("Choose a Password", type="password", key="signup_password")
        role_code    = st.text_input("Profile type code", key="signup_code")

        col1, col2 = st.columns([1,3])
        with col1:
            if st.button("Register"):
                # validation
                if not (signup_user.strip() 
                        and signup_email.strip() 
                        and signup_password 
                        and role_code.strip()):
                    st.error("All fields are required to register.")
                    return

                # 2) Profile‐type code check
                code     = int(role_code)
                role_map = {140:"administrator", 198:"supervisor", 220:"participant"}
                if code not in role_map:
                    st.error("Invalid profile type code.")
                    return

                # 3) Create the Auth user
                try:
                    auth_res = auth.sign_up({
                        "email":    signup_email,
                        "password": signup_password
                    })
                except Exception as e:
                    st.error(f"Sign‑up failed: {e}")
                    return

                # 4) Insert into profiles
                try:
                    sup_res = (
                        supabase
                        .from_("profiles")
                        .insert({
                            "id":                auth_res.user.id,
                            "username":          signup_user,
                            "email":             signup_email,
                            "role":              role_map[code],
                            "profile_type_code": code
                        })
                        .execute()
                        )       
                except Exception:
                    st.info("⏳ Loading… please wait a moment.")
                    st_autorefresh(interval=2000, limit=None, key="retry_answers")
                    return         

                if not getattr(sup_res, "data", None):
                    st.error("❌ Failed to create profile.")
                    return

                # success!
                st.success("✅ Registered! Please confirm your email, then log in.")
                st.session_state.show_signup = False

        with col2:
            if st.button("Cancel"):
                st.session_state.show_signup = False
                # clear the signup fields if you want:
                for k in ("signup_user","signup_email","signup_password","signup_code"):
                    st.session_state.pop(k, None)

# ------------------------------------------------------- Other functions -----------------------------------------------

# teste de conexão
try:
    res = supabase.from_("profiles").select("id").limit(1).execute()
except Exception as e:
    st.info("Erro na ligação ao Supabase: {e}.⏳ Loading… please wait a moment.")
    st_autorefresh(interval=2000, limit=None, key="retry_answers")
    


def show_logos(logo_paths_with_widths):
    logos_html = ""
    for path, width in logo_paths_with_widths:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            logos_html += f"<img src='data:image/png;base64,{encoded}' width='{width}' style='margin: 0 20px;'/>"

    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            {logos_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def load_selected_roles():
    return sorted({p["participant_role"] for p in st.session_state.get("participants_cache", [])})

def save_current(name: str):
    st.session_state.simulation_name = name

def load_current():
    return st.session_state.get("simulation_name", "")

def nav_to(page_name: str):
    """Helper: set the app’s current page in session_state and rerun."""
    st.session_state.page = page_name
    st.rerun()


#------------------------------------------------------ Page 2 - Welcome to CHIRON System ----------------------------------------------
def page_welcome():
    """
    Main menu after login. Branches on user_role:
      - participant / supervisor / manager all see New, Running & Past simulations
      - administrator gets an extra Control Center button
    """

    if "post_login_init" not in st.session_state:
        st.session_state.answers_cache      = []
        st.session_state.last_answer_id     = 0
        st.session_state.participants_cache = []
        st.session_state.last_snapshot_ts   = 0.0
        st.session_state.post_login_init    = True

    # render your logos
    show_logos([
        ("Logo_CHIRON.png", 90),
        ("IDEAS_LAB.png", 180),
        ("Novologofct2021.png", 150)
    ])

    st.title("Welcome to CHIRON System")
    st.write("This system was developed in the IDeaS Laboratory at NOVA School of Science and Technology in Lisbon, Portugal.The CHIRON training system was developed with the objective of training astronaut crews and mission control crews for crisis during space missions. With this system it is possible to develop hard skills, such as procedural knowledge, and soft skills, such as teamwork.")

    role = st.session_state.get("user_role", "participant")
    st.markdown(f"**You are logged in as:** `{role}`")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ New Simulation"):
            if role == "participant":
                nav_to("participant_new_simulation")
            elif role == "supervisor":
                nav_to("supervisor_menu")
            elif role == "administrator":
                nav_to("control_center")
            else:  # e.g. manager
                nav_to("manager_menu")
    with col2:
        if st.button("🏃 Running Simulations"):
            nav_to("running_simulations")

    if st.button("📜 Past Simulations"):
        nav_to("past_simulations")

    if role == "administrator":
        st.markdown("---")
        if st.button("⚙️ Control Center"):
            nav_to("control_center")

#------------------------------------------- Page 3 - supervisor----------------------------------------------------------------------

def page_create_new_simulation():
    role = st.session_state.user_role
    if role not in ("supervisor", "administrator"):
        st.warning("🔒 Only supervisors or administrators can create or resume simulations.")
        return

    st.header("Simulations ▶ Create or Resume")

    if st.button("Go back to the Main Menu"):
            nav_to("welcome")
    

    # ─── 1) Fetch all currently pending simulations ─────────────────────────────────
    @st.cache_data(ttl=3)
    def load_pending():
        resp = (supabase
                .from_("simulation")
                .select("id,name,roles_logged,created_at")
                .eq("status", "pending")
                .order("created_at", desc=True)
                .execute())
        return resp.data or []
    pending = load_pending()

    left, right = st.columns(2)

    # ─── Left: Resume an existing pending sim ──────────────────────────────────────
    with left:
        st.subheader("Resume Pending")
        if pending:
            # label→row mapping
            opts = {
                f"{s['name']} (id={s['id']})—{len(s['roles_logged'])}/8 roles": s
                for s in pending
            }
            choice = st.selectbox("Choose to resume", list(opts.keys()))
            if st.button("Open Selected"):
                sim = opts[choice]
                st.session_state.simulation_id   = sim["id"]
                st.session_state.simulation_name = sim["name"]
                st.session_state.answers_cache      = []
                st.session_state.last_answer_id     = 0
                st.session_state.participants_cache = []
                st.session_state.last_snapshot_ts   = 0.0
                nav_to("roles_claimed_supervisor")
        else:
            st.write("_No simulations pending right now_")

    # ─── Right: Create a brand-new simulation ─────────────────────────────────────
    with right:
        st.subheader("Start New")
        new_name = st.text_input("New simulation name", key="new_sim_name")
        if st.button("Create New Simulation"):
            if not new_name.strip():
                st.error("Please enter a name for your simulation.")
            else:
                sim_name = new_name.strip()
                try:
                    ins = (
                        supabase
                        .from_("simulation")
                        .insert({
                            "name":         sim_name,
                            "roles_logged": [],          # no roles yet
                            "status":       "pending"
                        })
                        .execute()
                    )
                    created = ins.data[0]
                except Exception as e:
                    st.info("Could not create simulation: {e}.⏳ Loading… please wait a moment.")
                    st_autorefresh(interval=2000, limit=None, key="retry_answers")
                    return

                st.success(f"✅ Created '{new_name}' (id={created['id']})")
                st.session_state.simulation_id   = created["id"]
                st.session_state.simulation_name = new_name
                st.success(f"✅ Created '{sim_name}' (id={created['id']})")
                st.session_state.simulation_id   = created["id"]
                st.session_state.simulation_name = sim_name
                st.session_state.answers_cache      = []
                st.session_state.last_answer_id     = 0
                st.session_state.participants_cache = []
                st.session_state.last_snapshot_ts   = 0.0
                # Invalidar cache de pending para que desapareça imediatamente
                load_pending.clear()
                nav_to("roles_claimed_supervisor")

def roles_claimed_supervisor():
    if st.button("Go back to the Main Menu"):
            nav_to("welcome")
    sim_id = st.session_state.simulation_id

    # 0) Pull in the current participants in the lobby (usernames) and existing roles_logged
    try:
        sim_meta = (
            supabase
            .from_("simulation")
            .select("participants_logged, roles_logged")
            .eq("id", sim_id)
            .single()
            .execute()
            .data or {}
        )
    except Exception:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
    joined = sim_meta.get("participants_logged", [])
    st.markdown("**Participants in lobby:**")
    st_autorefresh(interval=5000, key="wait_for_invite")
    for u in joined:
        st.write("• " + u)
    st.markdown("---")

    # 1) Load the raw participant rows (so we can update them)
    try:
        parts = (
            supabase
            .from_("participant")
            .select("id, id_profile, participant_role")
            .eq("id_simulation", sim_id)
            .execute()
            .data or []
        )
    except Exception:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return

    # 2) Build a map of profile_id → username
    profile_ids = [p["id_profile"] for p in parts]
    try:
        profiles = (
            supabase
            .from_("profiles")
            .select("id, username")
            .in_("id", profile_ids)
            .execute()
            .data or []
        )
    except Exception:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
    username_map = {prof["id"]: prof["username"] for prof in profiles}

    st.subheader("Assign Roles to Participants")
    with st.form("assign_roles"):
        assignments = {}
        for p in parts:
            uname = username_map.get(p["id_profile"], f"#{p['id_profile']}")
            current = p.get("participant_role") or ""
            options = [""] + ALL_ROLES
            idx = options.index(current) if current in options else 0
            assignments[p["id"]] = st.selectbox(uname, options, index=idx, key=f"role_{p['id']}")
        submitted = st.form_submit_button("Save Assignments")

    if submitted:
        # 3) Write each participant's selected role back into participant.participant_role
        for pid, role in assignments.items():
            try:
                resp = (
                    supabase
                    .from_("participant")
                    .update({"participant_role": role or None})
                    .eq("id", pid)
                    .execute()
                )
                # debug:
                st.write(f"Update pid={pid} →", resp.__dict__)
            except APIError as e:
                st.info("Failed to update participant {pid}: {e.args[0]['message']}.⏳ Loading… please wait a moment.")
                st_autorefresh(interval=2000, limit=None, key="retry_answers")
                return

        # 4) Build the new_roles list from your assignments dict
        new_roles = [role for role in assignments.values() if role]

        # 5) Push that into simulation.roles_logged
        try:
            resp = (
                supabase
                .from_("simulation")
                .update({"roles_logged": new_roles})
                .eq("id", sim_id)
                .execute()
            )
            # Optionally inspect resp:
            # st.write("🔍 simulation update response:", resp.__dict__)
        except APIError as e:
            st.info("Could not update simulation.roles_logged.⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")
            return

        # 6) Rerun the page so sim_meta (and parts) get re‑loaded with the updated array
        st.success("Roles updated.")
        st.rerun()

    # 7) Only enable “Start Simulation” when all 8 roles are set
    if all(p.get("participant_role") for p in parts) and len(parts) == 8:
        if st.button("▶️ Enter Simulation"):
            try:
                supabase.from_("simulation") \
                        .update({
                            "status":     "running",
                            "started_at": datetime.now(timezone.utc).isoformat()
                        }).eq("id", sim_id).execute()
            except Exception:
                st.info("⏳ Loading… please wait a moment.")
                st_autorefresh(interval=2000, limit=None, key="retry_answers")
                return
            nav_to("menu_iniciar_simulação_supervisor")
    else:
        st.info(f"{len(parts)} joined; fill all roles to start.")


def page_supervisor_menu():

    sim_id = st.session_state.get("simulation_id")
    role   = st.session_state.get("user_role")

    if role not in ("supervisor", "administrator"):
        st.warning("🔒 Only supervisors / administrators have access to this menu.")
        return
    if not sim_id:
        st.error("No simulation selected. Create or resume one first.")
        return

    @st.cache_data(ttl=3)
    def load_sim(sim_id: str):
        resp = (supabase
                .from_("simulation")
                .select("status, roles_logged, name, started_at")
                .eq("id", sim_id)
                .single()
                .execute())
        return resp.data

    sim_row = load_sim(sim_id)
    if not sim_row:
        st.error("❌ Simulation not found.")
        return

    roles_logged = sim_row.get("roles_logged") or []
    status       = sim_row.get("status")

    # Optional small status header
    st.markdown(f"**Simulation:** `{sim_row.get('name','')}` | "
                f"Roles: {len(roles_logged)}/8 | Status: `{status}`")
    if st.button("🔄 Refresh"):
        load_sim.clear()
        st.rerun()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("▶️ Go to Supervisor Dashboard"):
            nav_to("live_dashboard")
    
    with c2:
        if st.button("▶️ Go to Decision Suport Dashboard"):
            nav_to("dashboard")

    with c3:
        can_team = (len(roles_logged) == 8 and status == "running")
        if st.button("▶️ Go to Team Assessment Form",
                     disabled=not can_team,
                     help="Enabled when all 8 roles are claimed and simulation is running."):
            nav_to("teamwork_survey")

# --------------------------------------------------------- Page 3 Participant----------------------------------------------------

from streamlit_autorefresh import st_autorefresh

def participant_new_simulation():
    """
    Picks the single pending simulation created in the last 5 minutes (if any).
    """
    if st.button("Go back to the Main Menu"):
            nav_to("welcome")

    st_autorefresh(interval=5000, key="pending_autorefresh")
    MINUTES_WINDOW = 30
    MAX_ROLES = 8

    @st.cache_data(ttl=5)
    def _load_recent_pending(window_minutes: int):
        cutoff_iso = (datetime.utcnow() - timedelta(minutes=window_minutes)).isoformat() + "Z"
        try:
            resp = (supabase
                    .from_("simulation")
                    .select("id,name,roles_logged,created_at,status")
                    .eq("status", "pending")
                    .gte("created_at", cutoff_iso)
                    .order("created_at", desc=True)
                    .limit(1)
                    .execute())
            return resp.data or []
        except Exception as e:
            st.info("Could not look up new simulations: {e}.⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")
            return []

    sims = _load_recent_pending(MINUTES_WINDOW)

    # supabase-py no longer has res.error; use try/except
    try:
        if not isinstance(sims, list):
            raise TypeError("Unexpected response type for simulations list.")
    except Exception as e:
        st.error(f"❌ Internal processing error: {e}")
        return

    if not sims:
        st.info(f"No pending simulations created in the last {MINUTES_WINDOW} minutes—please wait for a supervisor.")
        return

    sim = sims[0]
    claimed        = len(sim.get("roles_logged") or [])
    is_full        = claimed >= MAX_ROLES
    current_sim_id = st.session_state.get("simulation_id")
    if claimed >= MAX_ROLES:
        st.info("The newest pending simulation is already full — please wait for a new one.")
        return

    st.subheader("Join the newest pending simulation:")
    created_at = sim.get("created_at", "")
    st.write(f"**{sim['name']}**  \nCreated at: `{created_at}`  \nRoles claimed: **{claimed}/{MAX_ROLES}**")

    # Prevent accidental rejoin if already in another simulation

    if is_full:
        help_text = f"Simulation full ({claimed}/{MAX_ROLES})."
    else:
        help_text = f"{claimed}/{MAX_ROLES} roles claimed."


    if st.button("Join this Simulation", help=help_text):
        # reset delta caches to avoid leaking old answers context
        st.session_state.answers_cache          = []
        st.session_state.participants_cache     = []
        st.session_state.last_answer_id         = 0
        st.session_state.last_snapshot_ts       = 0.0
        st.session_state.current_decision_index = None
        st.session_state.dm_stage               = 0
        st.session_state.loaded_35to43          = False
        st.session_state.simulation_id      = sim["id"]
        st.session_state.simulation_name    = sim["name"]
        st.session_state.dm_stage               = 0
        st.session_state._stage_locked          = False
        st.session_state.current_decision_index = None
        st.session_state.all_questions          = []
        # clear any “you‐clicked‐inject” flags so handle_initial_start() will show the start button
        st.session_state.inject1_clicked = False
        st.session_state.inject2_clicked = False
        st.session_state.inject3_clicked = False
        st.session_state.inject4_clicked = False
        my_username = st.session_state.profile["username"]
        my_profile  = st.session_state.profile_id

        # 1) fetch current list
        try:
            resp = (
                supabase
                .from_("simulation")
                .select("participants_logged")
                .eq("id", sim["id"])
                .single()
                .execute()
            )
        except Exception:
            st.info("⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")
            return
        current = resp.data.get("participants_logged") or []

        # 2) append if missing
        if my_username not in current:
            current.append(my_username)
            try:
                supabase.from_("simulation") \
                    .update({"participants_logged": current}) \
                    .eq("id", sim["id"]) \
                    .execute()
            except Exception:
                st.info("⏳ Loading… please wait a moment.")
                st_autorefresh(interval=2000, limit=None, key="retry_answers")
                return
            
        try:
            resp = (
                supabase
                .from_("participant")
                .insert({
                    "id_simulation":   sim["id"],
                    "id_profile":      my_profile,
                    "participant_role": None
                })
                .execute()
            )
        except APIError as e:
            st.info("Could not join simulation.⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")        # show full dict (code, message, hint, detail)
            return
        
        # grab the newly‑inserted participant row
        new_participant = resp.data[0]
        st.session_state.participant_id = new_participant["id"]

        nav_to("dm_role_claim")

MAX_ROLES = 8
ALL_ROLES = list(questionnaire1.roles.keys())

@st.cache_data(ttl=3)
def _load_sim_and_participants(sim_id: str):
    """Light cached fetch of simulation name, roles_logged and current participants."""
    sim_row = (supabase
               .from_("simulation")
               .select("id,name,status,roles_logged")
               .eq("id", sim_id)
               .single()
               .execute()
               .data)
    parts = (supabase
             .from_("participant")
             .select("id,participant_role,id_profile")
             .eq("id_simulation", sim_id)
             .execute()
             .data or [])
    return sim_row, parts


def page_dm_role_claim():

    st.header("Simulation role assignment")
    st_autorefresh(interval=7000, key="wait_for_role")

    sim_id  = st.session_state.simulation_id
    user_id = st.session_state.user.id

    # 1) Load all participant rows for this simulation
    try:
        parts = (
            supabase
            .from_("participant")
            .select("id, id_profile, participant_role")
            .eq("id_simulation", sim_id)
            .execute()
            .data or []
        )
        
        profiles = (
            supabase
            .from_("profiles")
            .select("id, username")
            .in_("id", profile_ids)
            .execute()
            .data or []
        )
    except Exception:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
    
    profile_ids = [p["id_profile"] for p in parts]
    username_map = {p["id"]: p["username"] for p in profiles}

    # 3) Find *your* participant record
    me = next((p for p in parts if p["id_profile"] == user_id), None)
    if me is None:
        st.error("Waiting for the supervisor to invite you into this simulation…")
        return

    # 4) If you haven’t been assigned yet, wait & auto‑refresh
    if not me.get("participant_role"):
        st.info("Waiting for your supervisor to assign your role…")
        return

    # 5) Show your role
    st.success(f"✅ Your assigned role: **{me['participant_role']}**")

    # 6) Show the full roster
    st.markdown("### Team Roster")
    for p in parts:
        uname = username_map.get(p["id_profile"], "Unknown")
        role  = p["participant_role"] or "_Unassigned_"
        st.write(f"- **{uname}** → {role}")

    # 7) Only let them start once everyone has a role
    if all(p.get("participant_role") for p in parts) and len(parts) == 8:
        if st.button("▶️ Enter Simulation"):
            me = next(p for p in parts if p["id_profile"] == st.session_state.user.id)
            # store the id and role so the next page has context
            st.session_state.participant_id = me["id"]
            st.session_state.dm_role        = me["participant_role"]
            st.session_state.dm_stage             = 0
            st.session_state._stage_locked        = False
            st.session_state.current_decision_index = None
            st.session_state.all_questions        = []
            # st.write("🔍 [DEBUG join] about to enter questionnaire, dm_stage =", st.session_state.get("dm_stage"))
            # st.write("🔍 [DEBUG join] answers dict:", st.session_state.get("answers"))
            st.session_state._stage_locked = True
            nav_to("dm_questionnaire")
    else:
        st.info(f"Waiting until all {len(parts)} participants have roles…")

# ------------------------------------------------------- Page 4 Participant ----------------------------------------------------------

def page_dm_questionnaire(key_prefix: str = ""):
    sim_id  = st.session_state.get("simulation_id")
    part_id = st.session_state.get("participant_id")
    role    = st.session_state.get("dm_role")
    if not sim_id or not part_id or not role:
        st.error("Missing simulation / participant context.")
        if st.button("⬅️ Back to Main Menu"):
            nav_to("welcome")
        return
    

    try:
        sync_simulation_state(sim_id)
    except Exception as e:
        # you could check isinstance(e, httpx.ReadError) if you want to be more specific
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=1000, limit=None, key="wait")
        return
    
    answer_idx = build_answer_index()

    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        st.markdown(f"### Role: **{st.session_state.dm_role}**")

    with col2:
        st.markdown(f"### Simulation: **{st.session_state.simulation_name}**")

    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()

    # —————————————————————
    # 1) On first entry, mark simulation + participant as started
    # —————————————————————
    if st.session_state.dm_stage == 0 and not st.session_state.get("dm_started_marker", False):
        # 1a) Update simulation
        try:
            now_iso = datetime.utcnow().isoformat() + "Z"
            supabase.from_("simulation").update(
                {"status": "running", "started_at": now_iso}
            ).eq("id", sim_id).execute()
            supabase.from_("participant").update(
                {"started_at": now_iso}
            ).eq("id", part_id).execute()
        except Exception as e:
            st.info("Could not mark start (continuing): {e}.⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")

        st.session_state.dm_started_marker = True

    # —————————————————————
    # 2) Run the questionnaire engine
  
    stage = st.session_state.dm_stage
    # only default to 1 on actual decision stages, not injects
    if stage not in (1, 3, 5) \
    and not isinstance(st.session_state.get("current_decision_index"), int):
        st.session_state.current_decision_index = 1

    questionnaire1.run(
        supabase,
        simulation_name=st.session_state.simulation_name,
        role=role # ignored if not implemented
    )

    st.session_state.roles = [
      "FE-3(EV2)", "Commander(CMO,IV2)", "FE-1(EV1)", "FE-2(IV1)",
      "FD", "FS", "BME", "CAPCOM",
    ]

    if st.session_state.get("dm_stage") == 8 and st.button("✅ Submit and Continue", key=f"{key_prefix}-submit_continue"):
        # 1) mark this participant finished
        try:
            finish_iso = datetime.utcnow().isoformat() + "Z"
            supabase.from_("participant").update(
                {"finished_at": finish_iso}
            ).eq("id", part_id).execute()
            st.success("✅ Finish time recorded!")
        except Exception as e:
            st.info("Could not mark finished: {e}.⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")
            return

        # 4) onward to individual results
        nav_to("individual_results")
        return


#----------------------------------------------------Page 4 - Supervisor---------------------------------------------------------------
# at the top of questionnaire1.py (or wherever render_participant_live lives)
from questionnaire1 import (
    decisions1to15,
    decision16_12A,
    decisions17to18_12B,
    decisions17to19_12C,
    decisions17to26,
)

def normalize_inject(label: str) -> str:
    import re
    if not label:
        return ""
    m = re.match(r"^(Initial Situation|Inject \d+|Decision \d+)", label.strip())
    return m.group(1) if m else label.strip()

def build_participant_role_map():
    return {p["id"]: p["participant_role"] for p in st.session_state.participants_cache}

def build_answers_by_part(sim_id: int):
    """Return dict participant_id -> list[answer_row] filtered to this simulation."""
    out = {}
    for a in st.session_state.answers_cache:
        if a["id_simulation"] != sim_id:
            continue
        out.setdefault(a["id_participant"], []).append(a)
    return out



def render_participant_live(pid: int, sim_id: int):
    """
    Read‑only live progress panel for a participant, using snapshot cache only.
    No direct queries here.
    """
    # ---- Guards ----
    if "answers_cache" not in st.session_state or "participants_cache" not in st.session_state:
        st.warning("Snapshot cache not initialized yet.")
        return

    # Participant role lookup
    role_map = build_participant_role_map()
    role = role_map.get(pid, "—")
    st.markdown(f"#### {role} — Participant #{pid}")

    # Simulation status check
    sim_status = st.session_state.get("simulation_status", "running")
    if sim_status != "running":
        st.write("⏳ Waiting for simulation to start…")
        return

    # Gather all answers by participant
    answers_by_part = build_answers_by_part(sim_id)
    my_answers = answers_by_part.get(pid, [])
    my_answer_map = {normalize_inject(a["inject"]): a for a in my_answers}

    # Extract FD key decisions
    fd_id = next((p["id"] for p in st.session_state.participants_cache if p["participant_role"] == "FD"), None)
    fd_answers = {}
    if fd_id:
        for a in answers_by_part.get(fd_id, []):
            key = normalize_inject(a["inject"])
            if key in {"Decision 12", "Decision 15"}:
                fd_answers[key] = a.get("answer_text")

    # 1) Core block: Decisions 1–15
    core = decisions1to15[:]

    # 2) Branch on FD Decision 12 after Inject 2
    a12 = fd_answers.get("Decision 12", "")
    if a12.startswith("A"):
        branch = decision16_12A[:]
    elif a12.startswith("B"):
        branch = decisions17to18_12B[:]
    elif a12.startswith("C"):
        branch = decisions17to19_12C[:]
    else:
        branch = []

    # 3) Final block after Inject 3, keyed by (Decision 12, Decision 15)
    a15 = fd_answers.get("Decision 15", "")
    final = decisions17to26.get((a12, a15), [])

    # 4) Assemble ordered steps
    steps = ["Initial Situation"]
    steps += [d["inject"] for d in core]
    steps += ["Inject 2"]
    steps += [d["inject"] for d in branch]
    steps += ["Inject 3"]
    steps += [d["inject"] for d in final]
    st.write("🛠️ DEBUG steps:", steps)


    # 5) Count completions
    # inside render_participant_live(pid, sim_id):
    sync_simulation_state(sim_id)

    sim_answers = [a for a in st.session_state.answers_cache if a["id_simulation"] == sim_id]
    step_counts = {}
    for a in sim_answers:
        key = normalize_inject(a["inject"])
        if key == "Initial Situation" or key.startswith("Inject"):
            if a.get("answer_text") == "DONE":
                step_counts[key] = step_counts.get(key, 0) + 1
        else:
            if a.get("answer_text") and a["answer_text"] != "SKIP":
                step_counts[key] = step_counts.get(key, 0) + 1
    
    st.write("🛠️ DEBUG counts:", step_counts)
    key_steps = {"Decision 12", "Decision 15"}

    # Determine current step
    current = "Finished"
    for s in steps:
        key = normalize_inject(s)
        needed = 1 if key in key_steps else 8
        if step_counts.get(key, 0) < needed:
            current = key
            break

    st.markdown(f"**Current stage:** {current}")

    # Display logic based on current
    if current == "Initial Situation":
        show_initial_situation()
        my_row = my_answer_map.get("Initial Situation")
        if my_row and my_row.get("answer_text") == "DONE":
            st.info("✅ You have started the simulation")
        else:
            st.warning("⏳ You have not started the simulation yet")
        return
    if current == "Finished":
        st.success("✅ All steps completed.")
        return

    # Helper: lookup question by inject across core, branch, final
    def lookup(inj):
        for block in (core, branch, final):
            for d in block:
                if normalize_inject(d["inject"]) == inj:
                    txt = d.get("text", "")
                    opts = d.get("options", [])
                    rs = d.get("role_specific", {})
                    if role in rs:
                        txt = rs[role].get("text", txt)
                        opts = rs[role].get("options", opts)
                    return d["inject"], txt, opts
        return inj, "_Prompt not found_", []

    # Render FD key decisions read‑only
    if current in key_steps:
        inj, txt, opts = lookup(current)
        st.markdown(f"### {inj}")
        st.info("FD decision (read-only). Use questionnaire view to answer.")
        ans = fd_answers.get(current)
        if ans:
            st.success(f"FD answered: **{ans}**")
        else:
            st.warning("FD has not answered yet.")
        return

    # Render inject completion status
    if current.startswith("Inject"):
        prompt = inject_prompt_map.get((current, None), "")
        st.markdown(f"### {current}")
        st.write(prompt)
        row = my_answer_map.get(current)
        done = row and row.get("answer_text") == "DONE"
        cnt = step_counts.get(current, 0)
        if done:
            st.info(f"You marked DONE. Waiting others… ({cnt}/8)")
        else:
            st.warning("You haven't clicked next yet.")
        return

    # Regular decision prompt
    inj, txt, opts = lookup(current)
    st.markdown(f"### {inj}")
    st.write(txt)
    if opts:
        st.markdown("**Options:**")
        for o in opts:
            st.write(f"- {o}")

    my_row = my_answer_map.get(current)
    cnt = step_counts.get(current, 0)
    if my_row:
        st.success(f"Your answer: **{my_row.get('answer_text','')}**")
        if cnt < 8:
            st.info(f"Waiting for others… ({cnt}/8)")
        else:
            st.info("All participants answered. Advancing…")
    else:
        st.warning("This decision hasn't been made yet.")



def compute_step_counts(sim_id, answers):
    counts = {}
    for a in answers:
        if a["id_simulation"] != sim_id:
            continue
        pref = normalize_inject(a["inject"])
        if pref.startswith("Inject"):
            if a["answer_text"] == "DONE":
                counts[pref] = counts.get(pref, 0) + 1
        else:
            if a["answer_text"] and a["answer_text"] != "SKIP":
                counts[pref] = counts.get(pref, 0) + 1
    return counts

def sync_simulation(sim_id):
    """Fetch any new answers/participants from Supabase into the session cache."""
    # 1) Answers as you already have
    last_ts = st.session_state.last_snapshot_ts
    try:
        new_answers = (
            supabase
            .from_("answers")
            .select("*")
            .gt("created_at", last_ts)
            .eq("id_simulation", sim_id)
            .execute()
            .data or []
        )
    except Exception:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
    if new_answers:
        st.session_state.answers_cache.extend(new_answers)
        st.session_state.last_snapshot_ts = max(a["created_at"] for a in new_answers)

    # 2) **Participants** (so that roster gets up‑to‑date roles)
    try: 
        parts = (
            supabase
            .from_("participant")
            .select("id,participant_role,id_profile")
            .eq("id_simulation", sim_id)
            .execute()
            .data or []
        )
    except Exception:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
    if parts:
        st.session_state.participants_cache = parts



def page_live_dashboard():
    st.header("Supervisor Live Dashboard")

    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name", "")

    if not sim_id:
        st.error("No simulation selected.")
        if st.button("Go back to Main Menu"):
            nav_to("welcome")
        return

    # 1) Sync snapshot FIRST (answers + participants)          # respects ttl
    # build_answer_index() only if you actually use it for cross lookups here
    # answer_idx = build_answer_index()

    # Optional: manual hard refresh (bust ttl)
    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        if st.button("⬅️ Back"):
            nav_to("menu_iniciar_simulação_supervisor")

    with col2:
        if st.button("🏠 Main Menu"):
            nav_to("welcome")

    with col3:
        if st.button("🔄 Refresh", key="refresh_force"):
            fetch_snapshot.clear()
            sync_simulation_state(sim_id)
            st.rerun()

    # 2) Build roster from participants_cache (no new query)
    participants_cache = st.session_state.get("participants_cache", [])
    roster = {p["participant_role"]: p["id"] for p in participants_cache if p.get("participant_role")}

    EXPECTED_ROLES = [
        "FE-3(EV2)", "Commander(CMO,IV2)", "FE-1(EV1)", "FE-2(IV1)",
        "FD", "FS", "BME", "CAPCOM",
    ]

    # 3) Dashboard grid
    st.markdown("### Roles")
    top_row  = EXPECTED_ROLES[:4]
    bottom_row = EXPECTED_ROLES[4:]
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=10000, limit=None, key="supervisor_autorefresh")

    for row in (top_row, bottom_row):
        cols = st.columns(4, gap="small")
        for role, col in zip(row, cols):
            with col:
                #st.markdown(f"**{role}**")
                pid = roster.get(role)
                if not pid:
                    st.info("Not joined yet")
                else:
                    render_participant_live(pid, sim_id)

    # 4) Missing roles summary
    missing = [r for r in EXPECTED_ROLES if r not in roster]
    if missing:
        st.warning("Missing roles: " + ", ".join(missing))
    else:
        st.success("All roles are present.")

    st.markdown("---")
    if st.button("🧪 Teamwork Assessment"):
        nav_to("page_one")

def normalize_inject(label: str) -> str:
    import re
    if not label:
        return ""
    m = re.match(r"^(Initial Situation|Inject \d+|Decision \d+)", label.strip())
    return m.group(1) if m else label.strip()

def build_role_specific_text(inject_label: str, role: str):
    # Search across currently active decision blocks (will pass them in)
    return ""  # placeholder if you integrate below logic differently


def page_override_interface():
    st.header("Supervisor Override")

    sim_id  = st.session_state.get("simulation_id")
    pid     = st.session_state.get("override_for")
    if not sim_id or not pid:
        st.error("No simulation or participant selected for override.")
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
        return

    # 1) Ensure snapshot is fresh enough
    sync_simulation_state(sim_id)

    # 2) Participant role from cache
    participants = st.session_state.get("participants_cache", [])
    role_map = {p["id"]: p["participant_role"] for p in participants}
    target_role = role_map.get(pid, "Unknown")
    st.subheader(f"Override for: **{target_role}** (participant #{pid})")

    # 3) Derive FD key decisions from cache
    answers = [a for a in st.session_state.answers_cache if a["id_simulation"] == sim_id]
    # Find FD id
    fd_id = next((p["id"] for p in participants if p.get("participant_role") == "FD"), None)
    fd_answers = {}
    if fd_id:
        for a in answers:
            if a["id_participant"] == fd_id:
                pref = normalize_inject(a["inject"])
                if pref in {"Decision 12", "Decision 15", "Decision 23", "Decision 34"}:
                    fd_answers[pref] = a.get("answer_text")

    ans12  = fd_answers.get("Decision 12")
    ans15 = fd_answers.get("Decision 15")

    # Resolve dynamic blocks
    block1 = decisions1to15

    # dynamically pick block2 depending on what FD answered at Decision 12:
    ans12 = fd_answers.get("Decision 12")
    block2 = decision16_12A.get(ans12, [])

    # then after inject 2 you go straight to the B or C branch:
    block3 = decisions17to18_12B.get(ans12, [])    if ans12 == "B" else []
    block4 = decisions17to19_12C.get(ans12, [])    if ans12 == "C" else []

    # after inject 3, look up the final “slot” by (ans12, ans15)
    ans15 = fd_answers.get("Decision 15")
    block5 = decisions17to26.get((ans12, ans15), [])

    active_blocks = [block1, block2, block3, block4, block5]

    # 5) Collect override-able injects (decisions only, optionally inject markers)
    # If you also want to override inject markers (Inject 1–4), include them manually.
    decision_injects = []
    for blk in active_blocks:
        for d in blk:
            decision_injects.append(d["inject"])
    # optional: add inject markers
    inject_markers = []
    if block2: inject_markers.append("Inject 2")
    if block3: inject_markers.append("Inject 3")
    if block4 or block5: inject_markers.append("Inject 4")
    # Always include first block's marker(s):
    inject_markers.insert(0, "Inject 1")
    # Combine if you want to override markers:
    full_inject_list = decision_injects  # or: inject_markers + decision_injects

    if not full_inject_list:
        st.info("No active decisions available to override (path unresolved).")
        return

    choice = st.selectbox(
        "Select decision/inject to override",
        sorted(set(full_inject_list)),
        key="override_inject_select"
    )

    # 6) Show original prompt & options
    def lookup_dec(inject_label: str):
        for blk in active_blocks:
            for d in blk:
                if d["inject"] == inject_label:
                    txt = d.get("text", "")
                    opts = d.get("options", [])
                    rs = d.get("role_specific", {})
                    if target_role in rs:
                        rsd = rs[target_role]
                        txt = rsd.get("text", txt)
                        opts = rsd.get("options", opts)
                    return txt, opts
        # If it's an inject marker
        if inject_label.startswith("Inject"):
            return f"{inject_label} marker", []
        return "_Not found_", []

    orig_text, orig_opts = lookup_dec(choice)
    with st.expander("Original Prompt / Options"):
        st.write(orig_text or "_No text_")
        if orig_opts:
            st.markdown("**Options:**")
            for o in orig_opts:
                st.write(f"- {o}")

    # 7) Existing answer (if any)
    existing = next(
        (a for a in answers if a["id_participant"] == pid and normalize_inject(a["inject"]) ==
         normalize_inject(choice)), None
    )
    if existing:
        st.info(f"Current stored answer: **{existing.get('answer_text','')}**")

    override_val = st.text_input("New answer (leave blank to delete / reset):", key="override_new_answer")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        apply_clicked = st.button("💾 Apply Override")
    with col_b:
        delete_clicked = st.button("🗑️ Delete Answer")
    with col_c:
        cancel_clicked = st.button("✖️ Cancel")

    if cancel_clicked:
        st.session_state.pop("override_for", None)
        nav_to("live_dashboard")
        return

    # 8) Apply override
    if apply_clicked:
        # Prepare row payload
        # Reconstruct question_text (optional)
        question_text = orig_text or ""
        payload = {
            "id_simulation":  sim_id,
            "id_participant": pid,
            "inject":         choice,
            "question_text":  question_text,
            "answer_text":    override_val,
            "score":          0,
            "response_time":  None
        }
        try:
            # Use upsert on conflict (id_simulation, id_participant, inject) if constraint exists
            resp = supabase.from_("answers").upsert([payload]).execute()
            if not resp.data:
                st.warning("Override applied but no data returned (check schema).")
            else:
                st.success(f"Override applied: {target_role} → {choice} = “{override_val}”")
                # Update local cache immediately
                updated_row = resp.data[0]
                # Remove any old cached row with same triple
                st.session_state.answers_cache = [
                    r for r in st.session_state.answers_cache
                    if not (r["id_simulation"] == sim_id and
                            r["id_participant"] == pid and
                            normalize_inject(r["inject"]) == normalize_inject(choice))
                ]
                st.session_state.answers_cache.append(updated_row)
                st.session_state.last_answer_id = max(
                    st.session_state.last_answer_id,
                    updated_row.get("id", st.session_state.last_answer_id)
                )
                st.session_state.pop("override_for", None)
                nav_to("live_dashboard")
                return
        except Exception as e:
            st.info("Override failed: {e}.⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")
    

    # 9) Delete answer
    if delete_clicked:
        if not existing:
            st.info("No existing answer to delete.")
        else:
            try:
                supabase.from_("answers") \
                        .delete() \
                        .eq("id_simulation", sim_id) \
                        .eq("id_participant", pid) \
                        .eq("inject", existing["inject"]) \
                        .execute()
                st.success("Answer deleted.")
                # Update cache
                st.session_state.answers_cache = [
                    r for r in st.session_state.answers_cache
                    if not (r["id_simulation"] == sim_id and
                            r["id_participant"] == pid and
                            normalize_inject(r["inject"]) == normalize_inject(choice))
                ]
                st.session_state.pop("override_for", None)
                nav_to("live_dashboard")
                return
            except Exception as e:
                st.info("Delete failed: {e}.⏳ Loading… please wait a moment.")
                st_autorefresh(interval=2000, limit=None, key="retry_answers")
    



# -------------------------------------------- 
@st.cache_data(ttl=5)
def teamwork_submitted(sim_id: int):
    try:
        res = (supabase
               .from_("teamwork")
               .select("id")
               .eq("id_simulation", sim_id)
               .maybe_single()
               .execute())
        return bool(res.data)
    except Exception:
        return False

def page_dashboard():
    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name", "")
    if not sim_id:
        st.error("No simulation selected.")
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
        return

    # Navigation controls
    top_cols = st.columns([1, 2, 2])
    with top_cols[0]:
        if st.button("⬅️ Back"):
            nav_to("menu_iniciar_simulação_supervisor")
            return
    with top_cols[1]:
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
            return
    with top_cols[2]:
        if st.button("🔄 Refresh"):
            fetch_snapshot.clear()
            sync_simulation_state(sim_id)
            st.rerun()

    # 1) Sync / read snapshot
    sync_simulation_state(sim_id)
    answers_cache = st.session_state.get("answers_cache", [])

    # 2) Filter relevant answers (FD & FS only)
    participants = st.session_state.get("participants_cache", [])
    role_by_pid = {p["id"]: p["participant_role"] for p in participants}
    interested_roles = {"FD", "FS"}
    relevant_rows = [
        a for a in answers_cache
        if a["id_simulation"] == sim_id and
           interested_roles.__contains__(role_by_pid.get(a["id_participant"], ""))
    ]

    if relevant_rows:
        # 3) Build inject -> list[answer_text]
        #    (consistent with what apply_vital_consequences expects)
        answers_for_effects = {}
        for row in relevant_rows:
            inject = row.get("inject")
            text   = row.get("answer_text")
            if inject and text is not None:
                answers_for_effects.setdefault(inject, []).append(text)

        # 4) Conditional recompute of vital consequences
        # Cache a hash of relevant answers to avoid recomputing needlessly
        new_sig = tuple(sorted(
            (inj, tuple(sorted(vals)))
            for inj, vals in answers_for_effects.items()
        ))
        last_sig = st.session_state.get("vitals_last_signature")
        if new_sig != last_sig:
            try:
                apply_vital_consequences(answers_for_effects)
                st.session_state.vitals_last_signature = new_sig
            except Exception as e:
                st.error(f"❌ Vital consequences update failed: {e}")
        else:
            st.caption("Vital consequences unchanged since last update.")

    # 5) Render simulation vitals / outputs
    try:
        data_simulation.run(sim_name)  # or pass sim_id if you refactor
    except Exception as e:
        st.error(f"❌ Error rendering simulation data: {e}")

    st.markdown("---")

    # 6) Teamwork gating
    submitted = teamwork_submitted(sim_id)
    if not submitted:
        st.warning("🔒 Team Results will be available after the teamwork assessment is submitted.")
        return

    # (Optional) Check if simulation is finished (if you want gating)
    status = st.session_state.get("simulation_status")
    if status != "finished":
        st.info("Simulation not marked finished yet.")
        return

    if st.button("🏆 View Team Results"):
        nav_to("certify_and_results")

    
    return

def page_one():
    """Landing page for TEAM assessment."""
    role = st.session_state.get("user_role")
    if role not in ("supervisor", "administrator"):
        st.error("Only supervisors / administrators can access the TEAM assessment.")
        if st.button("Back to Main Menu"):
            nav_to("welcome")
        return

    st.title("Team Emergency Assessment Measure (TEAM)")
    st.write("""
The TEAM tool allows you (the supervisor) to evaluate the crew's performance
across three domains:

**Leadership**, **Teamwork**, and **Task Management**,
plus a global performance rating and optional comments.
    """)

    if st.button("Start the Questionnaire"):
        nav_to("teamwork_survey")

    if st.button("Back"):
        nav_to("menu_iniciar_simulação_supervisor")


def page_teamwork_survey():
    role = st.session_state.get("user_role")
    if role not in ("supervisor", "administrator"):
        st.error("Only supervisors / administrators can fill the TEAM assessment.")
        if st.button("Back"):
            nav_to("welcome")
        return

    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name")
    if not sim_id or not sim_name:
        st.error("❌ Simulation context missing — please join a simulation first.")
        if st.button("Back"):
            nav_to("welcome")
        return

    st.subheader(f"TEAM Questionnaire – Simulation: **{sim_name}**")

    teams = ["Mcc crew", "Astronaut crew", "All crew"]

    # persist a nested dict of responses
    if "teamwork_responses" not in st.session_state:
        st.session_state.teamwork_responses = {team: {} for team in teams}
    resp = st.session_state.teamwork_responses

    try:
        existing_rows = (
            supabase
            .from_("teamwork")
            .select("team")
            .eq("id_simulation", sim_id)
            .execute()
            .data or []
        )
    except Exception:
        st.info("⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
    teams_done = {row["team"] for row in existing_rows}

    # 3) Se já tiver as 3, bloqueie o form
    if teams_done == set(teams):
        st.success("✅ As 3 avaliações TEAM já foram submetidas.")
        if st.button("Ver Resultados"):
            nav_to("certify_and_results")
        return

    # 4) Estado para armazenar respostas
    if "teamwork_responses" not in st.session_state:
        st.session_state.teamwork_responses = {team: {} for team in teams}
    resp = st.session_state.teamwork_responses


    likert_options = [
        "Please select an option",
        "0 – Never/Hardly ever",
        "1 – Seldom",
        "2 – About as often as not",
        "3 – Often",
        "4 – Always/Nearly always"
    ]

    def get_score(choice: str) -> int:
        """Extract numeric value from 'N – description'."""
        return int(choice.split('–')[0].strip())

    # --- Leadership ---
    for team in teams:
        st.markdown(f"## Assessment for **{team}**")
        responses = resp[team]

        # Leadership
        st.markdown("### 🧭 Leadership")
        responses['Q1'] = st.selectbox(
            f"{team} – 1. The team leader let the team know what was expected…",
            likert_options,
            index=likert_options.index(responses.get('Q1', likert_options[0])),
            key=f"{team}_Q1",
        )
        responses['Q2'] = st.selectbox(
            f"{team} – 2. The team leader maintained a global perspective…",
            likert_options,
            index=likert_options.index(responses.get('Q2', likert_options[0])),
            key=f"{team}_Q2",
        )

        # Teamwork (Q3–Q9)
        st.markdown("### 🤝 Teamwork")
        teamwork_qs = {
            3: "3. The team communicated effectively",
            4: "4. The team worked together to complete tasks…",
            5: "5. The team acted with composure and control",
            6: "6. The team morale was positive…",
            7: "7. The team adapted to changing situations",
            8: "8. The team monitored and reassessed the situation",
            9: "9. The team anticipated potential actions"
        }
        for i in range(3, 10):
            responses[f'Q{i}'] = st.selectbox(
                f"{team} – {teamwork_qs[i]}",
                likert_options,
                index=likert_options.index(responses.get(f'Q{i}', likert_options[0])),
                key=f"{team}_Q{i}",
            )

        # Task Management (Q10–Q11)
        st.markdown("### 🛠️ Task Management")
        responses['Q10'] = st.selectbox(
            f"{team} – 10. The team prioritised tasks",
            likert_options,
            index=likert_options.index(responses.get('Q10', likert_options[0])),
            key=f"{team}_Q10",
        )
        responses['Q11'] = st.selectbox(
            f"{team} – 11. The team followed approved standards…",
            likert_options,
            index=likert_options.index(responses.get('Q11', likert_options[0])),
            key=f"{team}_Q11",
        )

        # Overall (Q12)
        st.markdown("### 🌟 Overall Performance")
        default_overall = int(responses.get('Q12', '5'))
        overall_val = st.slider(
            f"{team} – 12. Global rating of the team’s performance (1–10)",
            1, 10, default_overall,
            key=f"{team}_Q12_SLIDER",
        )
        responses['Q12'] = str(overall_val)

        # Comments
        responses["COMMENTS"] = st.text_area(
            f"{team} – 📝 Comments (optional):",
            value=responses.get("COMMENTS", ""),
            key=f"{team}_COMMENTS",
            height=100,
        )

        st.markdown("---")


    st.markdown("---")
    col_submit, col_reset, col_cancel = st.columns(3)
    with col_submit:
        submit_clicked = st.button("✅ Submit All Assessments")
    with col_reset:
        if st.button("↩️ Reset Form"):
            for k in list(resp.keys()):
                resp[k] = likert_options[0] if k.startswith("Q") and k != "Q12" else ""
            resp["Q12"] = "5"
            st.session_state.TEAM_Q12_SLIDER = 5
            st.rerun()
    with col_cancel:
        if st.button("❌ Cancel"):
            st.session_state.pop("teamwork_edit_mode", None)
            nav_to("menu_iniciar_simulação_supervisor")
            return

    if submit_clicked:
        missing = []
        for team in teams:
            r = resp[team]
            missing += [f"{team} Q{i}" 
                        for i in range(1,12) 
                        if r.get(f"Q{i}", likert_options[0]) == likert_options[0]]
        if missing:
            st.error("⚠️ Please answer every question for each team before submitting:")
            for m in missing: st.write("- " + m)
            return

        # 2) Build payloads and insert
        for team in teams:
            r = resp[team]
            leadership = get_score(r['Q1']) + get_score(r['Q2'])
            teamwork   = sum(get_score(r[f'Q{i}']) for i in range(3,10))
            task       = get_score(r['Q10']) + get_score(r['Q11'])
            overall    = int(r['Q12'])
            total      = leadership + teamwork + task + overall

            payload = {
                "id_simulation":       sim_id,
                "simulation_name":     sim_name,
                "team":                team,
                "leadership":          leadership,
                "teamwork":            teamwork,
                "task_management":     task,
                "overall_performance": overall,
                "total":               total,
                "comments":            r.get("COMMENTS", "")
            }
            try:
                ins_res = (
                    supabase
                    .from_("teamwork")
                    .insert(payload)
                    .execute()
                )
                # If it didn’t raise, you can also inspect ins_res.data:
                st.write("🔍 Insert response:", ins_res.__dict__)
            except APIError as e:  # the full PostgREST JSON error
                st.info("Could not insert TEAM record.⏳ Loading… please wait a moment.")
                st_autorefresh(interval=2000, limit=None, key="retry_answers")
                return   

        st.success("✅ All three TEAM assessments submitted!")
        nav_to("certify_and_results")

        
@st.cache_data(ttl=5)
def fetch_teamwork(sim_id: int):
    try:
        res = (supabase
               .from_("teamwork")
               .select("id, leadership, teamwork, task_management, overall_performance, total, comments")
               .eq("id_simulation", sim_id)
               .maybe_single()
               .execute())
        return res.data
    except Exception:
        return None

@st.cache_data(ttl=5)
def fetch_sim_status(sim_id: int):
    try:
        res = (supabase
               .from_("simulation")
               .select("status, certified_at")
               .eq("id", sim_id)
               .maybe_single()
               .execute())
        return res.data
    except Exception:
        return None


def page_certify_and_results():
    st.header("Certification & Combined Results")
    st.write("Finalize the simulation and view aggregated team results.")

    # --- Guards ---
    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name", "")
    role     = st.session_state.get("user_role")

    if not sim_id:
        st.error("No simulation selected in session.")
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
        return

    if role not in ("supervisor", "administrator"):
        st.error("Only a supervisor / administrator can certify the simulation.")
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
        return

    # Navigation buttons
    nav_cols = st.columns([1,1,3])
    with nav_cols[0]:
        if st.button("⬅️ Back"):
            nav_to("menu_iniciar_simulação_supervisor")
            return
    with nav_cols[1]:
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
            return

    st.markdown(f"**Simulation:** `{sim_name}` (id={sim_id})")

    # --- Load TEAM Assessment ---
    try:
        res = (
            supabase
            .from_("teamwork")
            .select("team, leadership, teamwork, task_management, overall_performance, total, comments")
            .eq("id_simulation", sim_id)
            .execute()
        )
        teamwork_rows = res.data or []
    except APIError as e:
        st.info("Could not fetch TEAM assessments.⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
    if len(teamwork_rows) < 3:
        st.warning(f"🔒 Only {len(teamwork_rows)}/3 TEAM assessments submitted. Please complete all three before certification.")
        if st.button("Go to TEAM Form"):
            nav_to("teamwork_survey")
        return

    # --- Expand to show each team's scores plus combined averages ---
    with st.expander("View TEAM Assessment Summary", expanded=False):
        # Show each team’s individual scores
        for row in teamwork_rows:
            st.markdown(f"**{row['team']}**")
            st.write(f"- Leadership: **{row['leadership']}**")
            st.write(f"- Teamwork: **{row['teamwork']}**")
            st.write(f"- Task Mgmt: **{row['task_management']}**")
            st.write(f"- Overall: **{row['overall_performance']}**")
            st.write(f"- Total: **{row['total']}**")
            if row.get("comments"):
                st.write(f"- Comments: _{row['comments']}_")
            st.markdown("---")

        # And now a simple average across all teams:
        avg = lambda key: round(sum(r[key] for r in teamwork_rows) / len(teamwork_rows), 2)
        st.markdown("**Combined Averages**")
        st.write(f"- Leadership: **{avg('leadership')}**")
        st.write(f"- Teamwork: **{avg('teamwork')}**")
        st.write(f"- Task Mgmt: **{avg('task_management')}**")
        st.write(f"- Overall: **{avg('overall_performance')}**")
        st.write(f"- Total: **{avg('total')}**")

    # --- Load Simulation Status ---
    try:
        res = (
            supabase
            .from_("simulation")
            .select("status")
            .eq("id", sim_id)
            .single()
            .execute()
        )
        sim_meta = res.data or {}
    except APIError as e:
        st.info("Could not read simulation meta.⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return
        
    
    status       = sim_meta.get("status")

    st.markdown(f"**Current Simulation Status:** `{status}`")

    
    if status in ("pending","running"):
        finish_checkbox = st.checkbox("Mark simulation as finished on certification", value=True)
        if st.button("✅ Certify & View Team Results", type="primary"):
            updates = {}
            if finish_checkbox:
                updates["status"] = "finished"
            try:
                supabase.from_("simulation") \
                    .update(updates) \
                    .eq("id", sim_id) \
                    .execute()
            except Exception:
                st.info("⏳ Loading… please wait a moment.")
                st_autorefresh(interval=2000, limit=None, key="retry_answers")
                return
            st.session_state.simulation_certified = True
            st.success("✅ Simulation certified.")
            st.rerun()
            return

    # ─── 4) Once certified, show the results button ────────────────────────
    if status=="finished" and len(teamwork_rows) == 3:
        if st.button("🏆 View Team Results"):
            nav_to("team_results")
            return

def upload_pdf_to_storage(pdf_bytes: bytes, filename: str, bucket: str = "reports"):
    """
    Upload pdf_bytes to storage at `bucket/filename`.
    Returns (ok: bool, public_url: str|None, debug: str)
    """
    storage = supabase.storage.from_(bucket)
    debug = []

    # normalize
    filename = filename.lstrip("/")

    # 1) try native upsert
    try:
        debug.append("→ upload(upsert=True)")
        storage.upload(
            path=filename,
            file=pdf_bytes,
            file_options={"content-type": "application/pdf"},
            upsert=True
        )
    except TypeError as e:
        debug.append(f" ✖ upload(upsert) TypeError: {e}")
        # fallback: delete + upload
        try:
            debug.append("→ remove(old)")
            storage.remove([filename])
        except Exception as e2:
            debug.append(f" ✖ remove(): {e2}")
        try:
            debug.append("→ upload(replace)")
            storage.upload(
                path=filename,
                file=pdf_bytes,
                file_options={"content-type": "application/pdf"}
            )
        except Exception as e3:
            msg = str(e3)
            debug.append(f" ✖ upload() after remove: {msg}")
            # if it's Duplicate, treat as success
            if "Duplicate" in msg:
                debug.append("   • treating Duplicate as OK")
            else:
                return False, None, "\n".join(debug)
    except Exception as e:
        debug.append(f" ✖ upload(upsert) failed: {repr(e)}")
        return False, None, "\n".join(debug)

    # 2) get the public URL
    try:
        url = storage.get_public_url(filename)
        debug.append(f"✓ public_url={url}")
        return True, url, "\n".join(debug)
    except Exception as e:
        debug.append(f" ✖ get_public_url: {e}")
        return False, None, "\n".join(debug)



def page_team_results():
    """Display aggregated team performance, max comparisons, TEAM assessment, and export report."""
    import io
    import re
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import streamlit as st

    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name", "")
    if not sim_id:
        st.error("No simulation selected.")
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
        return

    st.header("🏆 Team Performance Results")
    st.subheader(f"Simulation: {sim_name} (id={sim_id})")

    # ---------- helpers ----------
    def normalize(label: str) -> str:
        if not label:
            return ""
        m = re.match(r"^(Decision \d+|Inject \d+|Initial Situation)", label.strip())
        return m.group(1) if m else label.strip()

    # ---------- ensure snapshot (optional, but you already use it elsewhere) ----------
    sync_simulation_state(sim_id)
    participants_cache = st.session_state.get("participants_cache", [])
    answers_cache      = st.session_state.get("answers_cache", [])

    # ---------- simulation status ----------
    @st.cache_data(ttl=5)
    def fetch_sim_status(sim_id_):
        try:
            res = (supabase
                   .from_("simulation")
                   .select("status,name")
                   .eq("id", sim_id_)
                   .maybe_single()
                   .execute())
            return res.data
        except Exception:
            return None

    sim_row = fetch_sim_status(sim_id)
    if not sim_row:
        st.error("Could not load simulation status.")
        return
    if sim_row.get("status") != "finished":
        st.info("⏳ Simulation not yet marked finished.")
        if st.button("⬅️ Back"):
            nav_to("certify_and_results")
        return

    # ---------- FD id ----------
    # participants_cache may be list or dict; handle both
    if isinstance(participants_cache, dict):
        plist = list(participants_cache.values())
    else:
        plist = participants_cache

    fd_id = next((p["id"] for p in plist if p.get("participant_role") == "FD"), None)
    if not fd_id:
        # fallback: query
        try:
            fd_q = (supabase.from_("participant")
                    .select("id")
                    .eq("id_simulation", sim_id)
                    .eq("participant_role", "FD")
                    .maybe_single()
                    .execute())
            fd_id = fd_q.data["id"] if fd_q.data else None
        except Exception:
            fd_id = None

    if not fd_id:
        st.error("Flight Director not found.")
        return

    # ---------- FD key answers & scenario code ----------
    @st.cache_data(ttl=10)
    def fetch_fd_answers_map(sim_id_, fd_pid):
        rows = (supabase
                .from_("answers")
                .select("inject,answer_text")
                .eq("id_simulation", sim_id_)
                .eq("id_participant", fd_pid)
                .execute()).data or []
        wanted = {"Decision 12","Decision 15","Decision 23","Decision 34"}
        out = {}
        for r in rows:
            pref = normalize(r["inject"])
            if pref in wanted and r.get("answer_text"):
                out[pref] = r["answer_text"]
        return out

    fd_map = fetch_fd_answers_map(sim_id, fd_id)

    missing = [k for k in ["Decision 12","Decision 15"] if k not in fd_map]
    if missing:
        st.error(f"Missing FD key decisions: {', '.join(missing)}")
        return

    def scenario_token(dec_label: str, ans_text: str) -> str:
        base = ans_text.split(".")[0].strip().lower()
        letter = base[0] if base else "x"
        number = dec_label.split()[-1]
        return f"{letter}{number}"

    scenario_code = ",".join([
        scenario_token("Decision 12",  fd_map["Decision 12"]),
        scenario_token("Decision 15", fd_map["Decision 15"]),
    ])
    st.caption(f"**Scenario code:** `{scenario_code}`")

    # ---------- load individual_results ----------
    @st.cache_data(ttl=10)
    def fetch_individual(sim_id_):
        res = (supabase
               .from_("individual_results")
               .select("basic_life_support, primary_survey, secondary_survey, "
                       "definitive_care, crew_roles_communication, systems_procedural_knowledge")
               .eq("simulation_id", sim_id_)
               .execute())
        return res.data or []

    ind_rows = fetch_individual(sim_id)
    if not ind_rows:
        st.info("No individual aggregate results yet.")
        return

    df_ind = pd.DataFrame(ind_rows)

    MED_CATS  = ["basic_life_support", "primary_survey", "secondary_survey", "definitive_care"]
    PROC_CATS = ["crew_roles_communication", "systems_procedural_knowledge"]
    ALL_CATS  = MED_CATS + PROC_CATS

    actual_totals = df_ind[ALL_CATS].sum().to_dict()

    # ---------- max_scores for scenario ----------
    RAW_TO_TOTAL = {
        "basic_life_support":             "basic_life_support_total",
        "primary_survey":                 "primary_survey_total",
        "secondary_survey":               "secondary_survey_total",
        "definitive_care":                "definitive_care_total",
        "crew_roles_communication":       "crew_roles_communication_total",
        "systems_procedural_knowledge":   "systems_procedural_knowledge_total",
    }

    @st.cache_data(ttl=10)
    def fetch_max_scores(code: str):
        res = (supabase
               .from_("max_scores")
               .select("role,category,max_value,scenario_code")
               .eq("scenario_code", code)
               .execute())
        return res.data or []

    ms_rows = fetch_max_scores(scenario_code)
    if not ms_rows:
        st.warning("No max_scores rows found for this scenario code.")
        team_max_by_cat = {c: 0.0 for c in ALL_CATS}
    else:
        df_ms = pd.DataFrame(ms_rows)
        df_ms["category"] = df_ms["category"].str.lower()
        team_max_by_cat = {}
        for raw_cat, total_cat in RAW_TO_TOTAL.items():
            m = df_ms[df_ms["category"] == total_cat.lower()]["max_value"].sum()
            team_max_by_cat[raw_cat] = float(m) if not pd.isna(m) else 0.0

    # ---------- table Team vs Max ----------
    rows = []
    for cat in ALL_CATS:
        actual = actual_totals.get(cat, 0.0)
        mval   = team_max_by_cat.get(cat, 0.0)
        pct    = f"{(100*actual/mval):.1f}%" if mval else "—"
        rows.append([cat.replace("_"," ").title(), actual, mval, pct])

    med_actual_sum  = sum(actual_totals[c] for c in MED_CATS)
    med_max_sum     = sum(team_max_by_cat.get(c, 0.0) for c in MED_CATS)
    proc_actual_sum = sum(actual_totals[c] for c in PROC_CATS)
    proc_max_sum    = sum(team_max_by_cat.get(c, 0.0) for c in PROC_CATS)
    grand_actual    = med_actual_sum + proc_actual_sum
    grand_max       = med_max_sum + proc_max_sum

    rows += [
        ["Medical Knowledge", med_actual_sum, med_max_sum,
         f"{100*med_actual_sum/med_max_sum:.1f}%" if med_max_sum else "—"],
        ["Procedural Knowledge", proc_actual_sum, proc_max_sum,
         f"{100*proc_actual_sum/proc_max_sum:.1f}%" if proc_max_sum else "—"],
        ["Total", grand_actual, grand_max,
         f"{100*grand_actual/grand_max:.1f}%" if grand_max else "—"]
    ]

    df_team_vs_max = pd.DataFrame(rows, columns=["Category", "Team Score", "Max Score", "% of Maximum"])
    st.subheader("📊 Team Scores vs Maximum")
    st.dataframe(df_team_vs_max, use_container_width=True)

    import matplotlib.pyplot as plt
    import numpy as np

    cats   = df_team_vs_max["Category"].tolist()
    scores = df_team_vs_max["Team Score"].tolist()
    maxes  = df_team_vs_max["Max Score"].tolist()

    x = np.arange(len(cats))
    width = 0.35
    fig_team_scores, ax = plt.subplots(figsize=(6,3))            # <<< NEW
    ax.bar(x - width/2, scores, width, label="Team")
    ax.bar(x + width/2, maxes,  width, label="Max")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Points")
    ax.legend(fontsize=8)
    fig_team_scores.tight_layout()

    st.pyplot(fig_team_scores, use_container_width=True)

    # ---------- TEAM assessments ----------
    @st.cache_data(ttl=10)
    def fetch_teamwork_all(sim_id_):
        res = (supabase
               .from_("teamwork")
               .select("team, leadership, teamwork, task_management, overall_performance, total, comments, created_at")
               .eq("id_simulation", sim_id_)
               .execute())
        return res.data or []

    tw_rows = fetch_teamwork_all(sim_id)
    team_figs = [] 

    if not tw_rows:
        st.info("No TEAM assessments found.")
    else:
        st.subheader("🔹 TEAM Assessments (by crew)")
        TW_LABELS = ["Leadership", "Teamwork", "Task Mgmt", "Overall", "Total"]
        TW_KEYS   = ["leadership", "teamwork", "task_management", "overall_performance", "total"]
        TW_MAXES  = [8, 28, 8, 10, 54]

        figs = []
        for row in tw_rows:
            values = [row[k] for k in TW_KEYS]
            x = np.arange(len(TW_LABELS))
            width = 0.35
            fig, ax = plt.subplots(figsize=(4,3))
            ax.bar(x - width/2, values, width, label="Score")
            ax.bar(x + width/2, TW_MAXES, width, label="Max")
            ax.set_xticks(x)
            ax.set_xticklabels(TW_LABELS, fontsize=8)
            ax.set_ylabel("Points")
            ax.set_title(row['team'])
            ax.legend(fontsize=6)
            fig.tight_layout()
            figs.append((fig, row))
            team_figs.append((f"TEAM – {row['team']}", fig))

        # show side-by-side (3 per row)
        cols = st.columns(min(3, len(figs)))
        for i, (fig, row) in enumerate(figs):
            cols[i % 3].pyplot(fig, use_container_width=True)
            with cols[i % 3].expander("Details"):
                st.write(f"- Leadership: **{row['leadership']}** / 8")
                st.write(f"- Teamwork: **{row['teamwork']}** / 28")
                st.write(f"- Task Mgmt: **{row['task_management']}** / 8")
                st.write(f"- Overall: **{row['overall_performance']}** / 10")
                st.write(f"- Total: **{row['total']}** / 54")
                if row.get("comments"):
                    st.write(f"_Comments:_ {row['comments']}")

    # ---------- NASA TLX (combined radar) ----------
    # ---------- NASA TLX (team avg + role picker) ----------
    @st.cache_data(ttl=10)
    def fetch_tlx_all(sim_id_):
        return (
            supabase
            .from_("taskload_responses")
            .select("participant_role, mental, physical, temporal, performance, effort, frustration")
            .eq("id_simulation", sim_id_)
            .execute()
        ).data or []

    tlx_rows = fetch_tlx_all(sim_id)
    fig_team_avg_tlx = None
    fig_role_tlx_map = {}

    if not tlx_rows:
        st.info("No TLX responses to aggregate.")
    else:
        import numpy as np, pandas as pd, matplotlib.pyplot as plt

        dims = ["mental","physical","temporal","performance","effort","frustration"]
        nice = [d.title() for d in dims]

        def _radar(values, title, size=(4,4)):
            # values: list of len(dims)
            vals = values + values[:1]
            angles = np.linspace(0, 2*np.pi, len(dims), endpoint=False).tolist()
            angles += angles[:1]
            fig, ax = plt.subplots(subplot_kw={"polar": True}, figsize=size)
            ax.plot(angles, vals, linewidth=2)
            ax.fill(angles, vals, alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(nice, fontsize=8)
            ax.set_ylim(0, 20)
            ax.set_title(title, fontsize=10)
            fig.tight_layout()
            return fig

        df_tlx = pd.DataFrame(tlx_rows)

        # Left: team average
        team_avg = df_tlx[dims].mean().tolist()

        col_left, col_right = st.columns([1,1])

        with col_left:
            st.subheader("🧠 TLX – Team Average")
            fig_team_avg_tlx = _radar(team_avg, "Team Average")
            st.pyplot(fig_team_avg_tlx, use_container_width=True)

        # Right: role picker
        roles = sorted(df_tlx["participant_role"].dropna().unique().tolist())
        with col_right:
            st.subheader("🔍 TLX – By Role")
            roles = sorted(df_tlx["participant_role"].dropna().unique().tolist())
            picked = st.selectbox("Choose a role", roles, index=0)
            for r in roles:
                r_vals = df_tlx[df_tlx["participant_role"] == r][dims].mean().tolist()
                fig_role = _radar(r_vals, r)
                fig_role_tlx_map[r] = fig_role

            st.pyplot(fig_role_tlx_map[picked], use_container_width=True)

    figs_to_embed = [("Team Scores vs Max", fig_team_scores)]
    figs_to_embed.extend(team_figs)          # from TEAM assessments

    from reportlab.platypus import Image as RLImage
    import io

    import io
    def fig_to_png(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
        buf.seek(0)
        return buf

    # team scores vs max table figure (optional small bar chart)
    # If you already have a figure for df_team_vs_max, build it, else skip
    fig_team_scores = None
    try:
        # quick bar chart for the totals row
        import matplotlib.pyplot as plt
        cats_plot = df_team_vs_max.iloc[:-3, 0].tolist()  # skip the last 3 summary rows
        team_vals = df_team_vs_max.iloc[:-3, 1].astype(float).tolist()
        max_vals  = df_team_vs_max.iloc[:-3, 2].astype(float).tolist()

        x = np.arange(len(cats_plot))
        w = 0.4
        fig_team_scores, ax = plt.subplots(figsize=(5,3))
        ax.bar(x - w/2, team_vals, width=w, label="Team")
        ax.bar(x + w/2, max_vals,  width=w, label="Max")
        ax.set_xticks(x)
        ax.set_xticklabels(cats_plot, rotation=30, fontsize=8, ha="right")
        ax.set_ylabel("Points")
        ax.set_title("Team Scores vs Max (by category)")
        ax.legend(fontsize=8)
        fig_team_scores.tight_layout()
    except Exception:
        fig_team_scores = None

    png_team_scores = fig_to_png(fig_team_scores) if fig_team_scores else None
    png_team_avg_tlx = fig_to_png(fig_team_avg_tlx) if fig_team_avg_tlx else None
    png_role_tlx_all = [(r, fig_to_png(f)) for r, f in fig_role_tlx_map.items()]
    png_team_figs = [(title, fig_to_png(fig)) for title, fig in team_figs]
    # ---------- PDF ----------
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table as RLTable, TableStyle, Image)
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor

    def build_team_pdf(df_scores, scenario_code, sim_name,
                    png_team_scores, png_team_avg_tlx,
                    png_role_tlx_all, png_team_figs):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()

        elems = [
            Paragraph("Team Performance Report", styles["Title"]),
            Paragraph(f"Simulation: {sim_name}", styles["Normal"]),
            Paragraph(f"Scenario Code: {scenario_code}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph("Team Scores vs Maximum", styles["Heading2"]),
        ]

        data = [df_scores.columns.tolist()] + df_scores.values.tolist()
        tbl = RLTable(data, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),HexColor("#1F4E78")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),0.25,colors.grey),
            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),
            ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 18))

        # add team score chart
        if png_team_scores:
            elems.append(Image(png_team_scores, width=430, height=260))
            elems.append(Spacer(1,12))

        # TEAM charts
        if png_team_figs:
            elems.append(Paragraph("TEAM Assessments", styles["Heading2"]))
            for title, pbuf in png_team_figs:
                elems.append(Paragraph(title, styles["Heading3"]))
                elems.append(Image(pbuf, width=360, height=220))
                elems.append(Spacer(1,10))

        # TLX charts
        if png_team_avg_tlx:
            elems.append(Paragraph("NASA TLX", styles["Heading2"]))
            elems.append(Paragraph("Team Average", styles["Heading3"]))
            elems.append(Image(png_team_avg_tlx, width=320, height=320))
            elems.append(Spacer(1,12))

        if png_role_tlx_all:
            elems.append(Paragraph("By Role", styles["Heading3"]))
            for role, pbuf in png_role_tlx_all:
                elems.append(Paragraph(role, styles["Normal"]))
                elems.append(Image(pbuf, width=260, height=260))
                elems.append(Spacer(1,8))

        doc.build(elems)
        buf.seek(0)
        return buf

    pdf_team_buf = build_team_pdf(df_team_vs_max, scenario_code, sim_name,
                                png_team_scores, png_team_avg_tlx,
                                png_role_tlx_all, png_team_figs)

    team_filename = f"team/{sim_id}/{sim_name.replace(' ','_')}_team_report.pdf"

    if not st.session_state.get("_team_pdf_uploaded"):
        ok, url, dbg = upload_pdf_to_storage(pdf_team_buf.getvalue(), team_filename)
        if ok:
            st.session_state["_team_pdf_uploaded"] = True
            st.success("📤 PDF stored in Database.")
        else:
            st.warning("❌ Could not upload team PDF to storage.")
            

    col_pdf, col_nav = st.columns([1,1])
    with col_pdf:
        st.download_button("⬇️ Download Team PDF",
                        data=pdf_team_buf,
                        file_name=team_filename.split('/')[-1],
                        mime="application/pdf",
                        key="dl_team_pdf")

    with col_nav:
        if st.button("🏠 Main Menu"):
            nav_to("welcome")





def page_simulation_menu():
    st.header("Supervisor Menu")

    sim_id = st.session_state.get("simulation_id")
    if not sim_id:
        st.error("❗ No simulation selected. Please ask your supervisor to create one first.")
        return

    # 1) Show the simulation name
    st.subheader(f"Simulation: **{st.session_state.simulation_name}**")

    if st.button("Go back to the Main Menu"):
        nav_to("welcome")
        return

    if st.button("▶️ Go to Vital-Signs Dashboard"):
            nav_to("dashboard")

    if st.button("▶️ Go to Supervisor Dashboard"):
        nav_to("live_dashboard")
    
    if st.button("▶️ Go to Teamwork Assessment"):
        nav_to("page_one")

@st.cache_data(ttl=10)
def fetch_my_answers_full(sim_id: int, part_id: int):
    return (
        supabase
        .from_("answers")
        .select(
            "inject,answer_text,"
            "basic_life_support,primary_survey,secondary_survey,definitive_care,"
            "crew_roles_communication,systems_procedural_knowledge,"
            "response_seconds,penalty"
        )
        .eq("id_simulation", sim_id)
        .eq("id_participant", part_id)
        .execute()
    ).data or []

from reportlab.platypus import Image as RLImage
import io

def fig_to_rl_image(fig, width=480):
    """Return a ReportLab Image from a matplotlib figure."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    buf.seek(0)
    img = RLImage(buf)
    # scale keeping aspect ratio
    w, h = img.wrap(0, 0)
    scale = width / w
    img._restrictSize(width, h * scale)
    return img


def page_individual_results():
    """Show the current participant's individual performance summary."""
    import re, numpy as np, pandas as pd
    import matplotlib.pyplot as plt

    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name", "")
    part_id  = st.session_state.get("participant_id")
    dm_role  = st.session_state.get("dm_role")
    user_role = st.session_state.get("user_role")

    if not (sim_id and part_id and dm_role):
        st.error("Simulation context or participant context missing.")
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
        return

    st.header("📈 Your Individual Results")
    st.caption(f"Simulation: **{sim_name}** | Role: **{dm_role}**")

    # ---------- snapshot ----------
    sync_simulation_state(sim_id)
    answers_cache      = st.session_state.get("answers_cache", [])
    participants_cache = st.session_state.get("participants_cache", [])

    if user_role not in ("supervisor", "administrator"):
        if not any(p["id"] == part_id for p in participants_cache):
            st.error("Your participant record was not found.")
            return

    # ---------- FD keys & scenario code ----------
    def norm_inject(lbl: str) -> str:
        if not lbl: return ""
        m = re.match(r"^(Decision \d+|Inject \d+|Initial Situation)", lbl.strip())
        return m.group(1) if m else lbl.strip()

    fd_id = next((p["id"] for p in participants_cache if p.get("participant_role") == "FD"), None)
    if not fd_id:
        st.error("Flight Director not present in this simulation.")
        return

    key_needed = {"Decision 12", "Decision 15"}
    fd_key_answers = {}
    for row in answers_cache:
        if row["id_simulation"] != sim_id or row["id_participant"] != fd_id:
            continue
        pref = norm_inject(row["inject"])
        if pref in key_needed and row.get("answer_text"):
            fd_key_answers[pref] = row["answer_text"]

    missing = [k for k in key_needed if k not in fd_key_answers]
    if missing:
        st.warning(f"Waiting for FD decisions: {', '.join(missing)}")
        return

    def scenario_token(decision_label: str, ans_text: str) -> str:
        base = ans_text.split(".")[0].strip().lower()
        letter = base[0] if base else "x"
        number = decision_label.split()[-1]
        return f"{letter}{number}"

    scenario_code = ",".join([
        scenario_token("Decision 12",  fd_key_answers["Decision 12"]),
        scenario_token("Decision 15", fd_key_answers["Decision 15"]),
    ])
    st.caption(f"Scenario code: {scenario_code}")

    # ---------- individual_results row ----------
    @st.cache_data(ttl=10)
    def fetch_individual_row(sim_id_, participant_id_):
        try:
            res = (supabase
                   .from_("individual_results")
                   .select("*")
                   .eq("simulation_id", sim_id_)
                   .eq("participant_id", participant_id_)
                   .maybe_single()
                   .execute())
            return res.data
        except Exception:
            return None

    ind = fetch_individual_row(sim_id, part_id)
    if not ind:
        st.info("No aggregated individual results yet. Please complete more decisions.")
        return

    MED_CATS  = ["basic_life_support", "primary_survey", "secondary_survey", "definitive_care"]
    PROC_CATS = ["crew_roles_communication", "systems_procedural_knowledge"]

    try:
        med_actuals  = [float(ind[c]) for c in MED_CATS]
        proc_actuals = [float(ind[c]) for c in PROC_CATS]
        med_subtot   = float(ind.get("medical_knowledge_total", sum(med_actuals)))
        proc_subtot  = float(ind.get("procedural_knowledge_total", sum(proc_actuals)))
        actual_total = float(ind.get("score", med_subtot + proc_subtot))
    except (TypeError, ValueError) as e:
        st.error(f"Malformed numeric data in individual_results: {e}")
        return

    # ---------- max_scores lookup ----------
    @st.cache_data(ttl=10)
    def fetch_role_maxes(role_, scen_code):
        try:
            res = (supabase
                   .from_("max_scores")
                   .select("category,max_value,scenario_code,role")
                   .eq("role", role_)
                   .eq("scenario_code", scen_code)
                   .execute())
            return res.data or []
        except Exception:
            return []

    max_rows = fetch_role_maxes(dm_role, scenario_code)
    st.write("DBG max_rows:", max_rows)

    RAW_TO_TOTAL = {
        "basic_life_support":             "basic_life_support_total",
        "primary_survey":                 "primary_survey_total",
        "secondary_survey":               "secondary_survey_total",
        "definitive_care":                "definitive_care_total",
        "crew_roles_communication":       "crew_roles_communication_total",
        "systems_procedural_knowledge":   "systems_procedural_knowledge_total",
    }
    role_max_map = {r["category"].lower(): float(r["max_value"]) for r in max_rows}

    def cat_max(cat):
        key = RAW_TO_TOTAL[cat].lower()
        return role_max_map.get(key, 0.0)

    med_maxs  = [cat_max(c) for c in MED_CATS]
    proc_maxs = [cat_max(c) for c in PROC_CATS]
    med_max_sub  = sum(med_maxs)
    proc_max_sub = sum(proc_maxs)
    max_total    = med_max_sub + proc_max_sub

    # ---------- TLX ----------
    @st.cache_data(ttl=10)
    def fetch_tlx(sim_id_, participant_id_):
        try:
            res = (supabase
                   .from_("taskload_responses")
                   .select("mental,physical,temporal,performance,effort,frustration")
                   .eq("id_simulation", sim_id_)
                   .eq("id_participant", participant_id_)
                   .maybe_single()
                   .execute())
            return res.data
        except Exception:
            return None

    tlx_row = fetch_tlx(sim_id, part_id)

    # ---------- RAW ANSWERS (with penalties etc.) ----------
    st.markdown("---")
    st.subheader("📝 Your Raw Answers")

    my_answers = fetch_my_answers_full(sim_id, part_id)

    import pandas as pd, re
    df_raw = pd.DataFrame(my_answers)

    if df_raw.empty:
        st.info("No answers recorded yet.")
    else:
        ORDER = [
            "Initial Situation","Inject 1",
            *[f"Decision {i}" for i in range(1,14)],
            "Inject 2",
            *[f"Decision {i}" for i in range(14,24)],
            "Inject 3",
            *[f"Decision {i}" for i in range(24,29)],
            "Inject 4",
            *[f"Decision {i}" for i in range(29,35)],
            *[f"Decision {i}" for i in range(35,44)],
        ]
        def norm(lbl):
            m = re.match(r"^(Initial Situation|Inject \d+|Decision \d+)", str(lbl))
            return m.group(1) if m else str(lbl)

        df_raw["prefix"]   = df_raw["inject"].map(norm)
        df_raw["order_no"] = pd.Categorical(df_raw["prefix"], ORDER, ordered=True)
        df_raw = df_raw.sort_values("order_no").drop(columns=["order_no","prefix"])

        wanted_cols = ["inject","answer_text","response_seconds","penalty",
                    "basic_life_support","primary_survey","secondary_survey",
                    "definitive_care","crew_roles_communication","systems_procedural_knowledge"]
        show_cols = [c for c in wanted_cols if c in df_raw.columns]

        st.dataframe(df_raw[show_cols], use_container_width=True)

    # totals for penalties
    total_penalty = float(df_raw.get("penalty", pd.Series(dtype=float)).fillna(0).sum())
    score_after_penalty = actual_total - total_penalty


    # ---------- Charts ----------
    col_med, col_proc = st.columns(2)
    with col_med:
        st.subheader("🩺 Medical Knowledge")
        labels = MED_CATS + ["Subtotal"]
        your   = med_actuals + [med_subtot]
        mx     = med_maxs    + [med_max_sub]
        x = np.arange(len(labels))
        fig_med, ax_med = plt.subplots(figsize=(5,3))
        w = 0.4
        ax_med.bar(x - w/2, your, width=w, label="You")
        ax_med.bar(x + w/2, mx,   width=w, label="Max")
        ax_med.set_xticks(x)
        ax_med.set_xticklabels([l.replace("_"," ").title() for l in labels],
                               rotation=30, ha="right")
        ax_med.set_ylabel("Points")
        ax_med.legend(fontsize=8)
        fig_med.tight_layout()
        st.pyplot(fig_med, use_container_width=True)
        fig_med_obj = fig_med 

    with col_proc:
        st.subheader("⚙️ Procedural Knowledge")
        labels = PROC_CATS + ["Subtotal"]
        your   = proc_actuals + [proc_subtot]
        mx     = proc_maxs    + [proc_max_sub]
        x = np.arange(len(labels))
        fig_proc, ax_proc = plt.subplots(figsize=(5,3))
        ax_proc.bar(x - w/2, your, width=w, label="You")
        ax_proc.bar(x + w/2, mx,   width=w, label="Max")
        ax_proc.set_xticks(x)
        ax_proc.set_xticklabels([l.replace("_"," ").title() for l in labels],
                                 rotation=30, ha="right")
        ax_proc.set_ylabel("Points")
        ax_proc.legend(fontsize=8)
        fig_proc.tight_layout()
        st.pyplot(fig_proc, use_container_width=True)
        fig_proc_obj  = fig_proc 

    # ---------- Summary table ----------
    col_table, col_tlx = st.columns(2)

    rows = []
    for c, a, m in zip(MED_CATS, med_actuals, med_maxs):
        pct = f"{100*a/m:.1f}%" if m else "—"
        rows.append([c.replace("_"," ").title(), a, m, pct])
    for c, a, m in zip(PROC_CATS, proc_actuals, proc_maxs):
        pct = f"{100*a/m:.1f}%" if m else "—"
        rows.append([c.replace("_"," ").title(), a, m, pct])

    rows += [
        ["Medical Knowledge",    med_subtot,  med_max_sub,  f"{100*med_subtot/med_max_sub:.1f}%" if med_max_sub else "—"],
        ["Procedural Knowledge", proc_subtot, proc_max_sub, f"{100*proc_subtot/proc_max_sub:.1f}%" if proc_max_sub else "—"],
        ["Total",                actual_total, max_total,   f"{100*actual_total/max_total:.1f}%" if max_total else "—"],
        ["Penalties",           -total_penalty, "", ""],
        ["Total (after pen.)",   score_after_penalty, max_total,
            f"{100*score_after_penalty/max_total:.1f}%" if max_total else "—"]
    ]

    df_summary = pd.DataFrame(rows, columns=["Category","Your Score","Max Score","% of Max"])

    with col_table:
        st.subheader("📋 Score Summary")
        st.table(df_summary)

    with col_tlx:
        st.subheader("💼 Task Load (NASA TLX)")
        if tlx_row:
            tlx_cols = ["mental","physical","temporal","performance","effort","frustration"]
            tlx_vals = [tlx_row[c] for c in tlx_cols]
            angles = np.linspace(0, 2*np.pi, len(tlx_cols), endpoint=False)
            angles = np.concatenate([angles, angles[:1]])
            vals_wrap = tlx_vals + [tlx_vals[0]]
            fig_tlx, ax_tlx = plt.subplots(subplot_kw={"polar":True}, figsize=(4,4))
            ax_tlx.plot(angles, vals_wrap, linewidth=2)
            ax_tlx.fill(angles, vals_wrap, alpha=0.25)
            ax_tlx.set_xticks(angles[:-1])
            ax_tlx.set_xticklabels([c.title() for c in tlx_cols], fontsize=8)
            ax_tlx.set_ylim(0, max(vals_wrap)*1.1 if any(vals_wrap) else 1)
            fig_tlx.tight_layout()
            st.pyplot(fig_tlx, use_container_width=True)
            fig_tlx_obj  = fig_tlx 
        else:
            st.info("No TLX responses submitted.")

    # ---------- PDF ----------
    # ---------- PDF (build, save, auto-upload) ----------
    st.markdown("---")

    import io
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table as RLTable, TableStyle, Image)
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor

    def _fig_to_png_bytes(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
        buf.seek(0)
        return buf

    # keep the figs you already created above
    fig_med_png  = _fig_to_png_bytes(fig_med)
    fig_proc_png = _fig_to_png_bytes(fig_proc)
    fig_tlx_png  = _fig_to_png_bytes(fig_tlx) if tlx_row else None

    def build_pdf(df_summary, sim_name, dm_role, scenario_code,
                fig_med_png, fig_proc_png, fig_tlx_png):
        pdf_buf = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buf, pagesize=letter)
        styles = getSampleStyleSheet()

        elems = [
            Paragraph("Individual Performance Report", styles["Title"]),
            Paragraph(f"Simulation: {sim_name}", styles["Normal"]),
            Paragraph(f"Role: {dm_role}", styles["Normal"]),
            Paragraph(f"Scenario Code: {scenario_code}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph("Score Summary", styles["Heading2"])
        ]

        # table
        data = [df_summary.columns.tolist()] + df_summary.values.tolist()
        tbl = RLTable(data, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),HexColor("#1F4E78")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),0.25,colors.grey),
            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),
            ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 18))

        # charts
        elems.append(Paragraph("Charts", styles["Heading2"]))
        elems.append(Image(fig_med_png, width=400, height=240))
        elems.append(Spacer(1,12))
        elems.append(Image(fig_proc_png, width=400, height=240))
        if fig_tlx_png:
            elems.append(Spacer(1,12))
            elems.append(Image(fig_tlx_png, width=320, height=320))

        doc.build(elems)
        pdf_buf.seek(0)
        return pdf_buf

    # build once
    pdf_buf = build_pdf(df_summary, sim_name, dm_role, scenario_code,
                    fig_med_png, fig_proc_png, fig_tlx_png)

    file_name = f"individual/{sim_id}/{sim_name.replace(' ','_')}_{dm_role.replace(' ','_')}_results.pdf"

    if not st.session_state.get("_ind_pdf_uploaded"):
        ok, url, dbg = upload_pdf_to_storage(pdf_buf.getvalue(), file_name)
        if ok:
            st.session_state["_ind_pdf_uploaded"] = True
            st.success("📤 PDF stored in Supabase.")
        else:
            st.warning("❌ Could not upload PDF to storage.")
            st.code(dbg) 

    col_pdf, col_nav = st.columns([1,1])
    with col_pdf:
        st.download_button("⬇️ Download PDF",
                        data=pdf_buf,
                        file_name=file_name.split('/')[-1],
                        mime="application/pdf",
                        key="dl_ind_pdf")

    with col_nav:
        if st.button("🏠 Main Menu"):
            nav_to("welcome")

          



def safe_query(callable_fn, retries: int = 2, base_delay: float = 0.15):
    """
    Retry transient DB (or HTTP) errors like Errno 11 “Resource temporarily unavailable”.
    - callable_fn: a zero‑arg function that does your supabase.from(...).select(...).execute()
    - retries: how many times to retry before giving up
    - base_delay: initial backoff (in seconds); doubles each retry, plus a bit of jitter
    """
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return callable_fn()
        except Exception as e:
            last_exc = e
            # If it’s our “busy” error, retry; otherwise bubble up immediately
            msg = str(e)
            if ("Resource temporarily unavailable" not in msg
                and "Errno 11" not in msg) or attempt == retries:
                raise
            # exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.05)
            time.sleep(delay)
    # if we somehow exit loop, re‑raise the last exception
    raise last_exc


def fetch_simulations_with_retry():
    return safe_query(lambda: supabase
                      .from_("simulation")
                      .select("*")
                      .execute())


def page_running_simulations():
    st.header("🏃 Running Simulations")
    if st.button("Go back to the Main Menu"):
        nav_to("welcome")
        return

    with st.spinner("Loading simulation…"):
        try:
            resp = fetch_simulations_with_retry()
        except Exception:
            st.info("Still loading… please wait a moment.")
            st_autorefresh(interval=1000, limit=None, key="wait")
            return
    sims = resp.data or []
    # filter only running sims, newest first
    running = sorted(
        (s for s in sims if s.get("status") == "running"),
        key=lambda s: s.get("started_at") or "",
        reverse=True
    )

    if not running:
        st.info("No simulations currently running.")
        return

    # table header
    cols = st.columns([1,3,3,2])
    style_h = (
        "background-color:#004080;color:white;padding:8px;"
        "border:1px solid #ddd;text-align:center;"
    )
    headers = ["Join", "Name", "Started At", "Roles Logged"]
    for c, h in zip(cols, headers):
        c.markdown(f"<div style='{style_h}'><strong>{h}</strong></div>", unsafe_allow_html=True)

    # iterate sims
    for sim in running:
        c0, c1, c2, c3 = st.columns([1,3,3,2])
        # join button
        with c0:
            st.markdown(f"<div style='background-color:#e6f7ff;padding:8px;"
                        "border:1px solid #ddd;text-align:center;'>", unsafe_allow_html=True)
            join = st.button("▶️ Join", key=f"join_{sim['id']}")
            st.markdown("</div>", unsafe_allow_html=True)
        c1.markdown(f"<div style='padding:8px;border:1px solid #ddd;'>{sim['name']}</div>", unsafe_allow_html=True)

        ts = pd.to_datetime(sim.get("started_at"))
        started = ts.strftime("%Y-%m-%d %H:%M:%S") if pd.notna(ts) else "—"
        c2.markdown(f"<div style='padding:8px;border:1px solid #ddd;'>{started}</div>", unsafe_allow_html=True)
        c3.markdown(f"<div style='padding:8px;border:1px solid #ddd;'>{sim.get('roles_logged','—')}</div>", unsafe_allow_html=True)

        if not join:
            continue

        # set session state defaults
        ss = st.session_state
        ss.simulation_id = sim['id']
        ss.simulation_name = sim['name']
        ss.setdefault('answers_cache', [])
        ss.setdefault('answers_delta', [])
        ss.setdefault('participants_cache', {})
        ss.setdefault('last_answer_id', 0)
        ss.setdefault('last_snapshot_ts', 0.0)

        role = ss.user_role
        if role in ('supervisor','administrator'):
            nav_to('menu_iniciar_simulação_supervisor')
            return

        if role != 'participant':
            st.error('Only supervisors or participants can join a running simulation.')
            return

        # fetch participant record
        try:
            part_res = (supabase.from_('participant')
                        .select('id, participant_role')
                        .eq('id_profile', ss.user.id)
                        .eq('id_simulation', sim['id'])
                        .maybe_single().execute())
        except Exception:
            st.info("⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")
            return
        part = getattr(part_res, 'data', None)
        if not part:
            st.error('You have not joined this simulation.')
            return

        ss.participant_id = part['id']
        ss.dm_role = part['participant_role']

        # build question flow based on new simulation structure
        from questionnaire1 import (
            decisions1to15, decision16_12A,
            decisions17to18_12B, decisions17to19_12C,
            decisions17to26, get_role_decision_answer
        )
        # key FD answers
        a12 = get_role_decision_answer('Decision 12','FD') or ''
        a15 = get_role_decision_answer('Decision 15','FD') or ''

        # define blocks
        core = decisions1to15[:]
        if a12.startswith('A'):
            branch = decision16_12A[:]
        elif a12.startswith('B'):
            branch = decisions17to18_12B[:]
        elif a12.startswith('C'):
            branch = decisions17to19_12C[:]
        else:
            branch = []
        st.write("🔍 [DEBUG final key]", repr(a12), repr(a15))
        st.write("🔍 [DEBUG final keys available]", len(decisions17to26), "combinations")

        final = decisions17to26.get((a12,a15), [])
        st.write("🔍 [DEBUG final length]", len(final))

        # assemble all_steps
        all_steps = ['Initial Situation']
        all_steps += [q['inject'] for q in core]
        all_steps += ['Inject 2']
        all_steps += [q['inject'] for q in branch]
        all_steps += ['Inject 3']
        all_steps += [q['inject'] for q in final]

        # fetch answered injects for this participant
        try:
            ans_resp = (
                supabase
                .from_("answers")
                # fetch both the label *and* the answer text
                .select("inject, answer_text")
                .eq("id_simulation",  sim["id"])
                .eq("id_participant", part["id"])
                .execute()
            )
        except Exception:
            st.info("⏳ Loading… please wait a moment.")
            st_autorefresh(interval=2000, limit=None, key="retry_answers")
            return
        raw = getattr(ans_resp, 'data', []) or []

        # normalize helper
        import re
        def norm(x):
            m = re.match(r'^(Initial Situation|Inject \d+|Decision \d+)', x.strip())
            return m.group(1) if m else x.strip()

        seen = set()
        for r in raw:
            label = norm(r['inject'])
            ans_txt = r.get('answer_text') or ""
            if label == "Initial Situation" or label.startswith("Inject"):
                if ans_txt == "DONE":
                    seen.add(label)
            else:
                # a real decision answer
                if ans_txt and ans_txt.upper() != "SKIP":
                    seen.add(label)
        # include FD-only decisions as answered
        for fd in ("Decision 12", "Decision 15"):
            if get_role_decision_answer(fd, "FD") is not None:
                seen.add(fd)
        if ss.dm_role != "FD":
            seen |= {"Decision 12", "Decision 15"}

        # find next_step
        seen.add("Initial Situation")
        next_step = None
        for step in all_steps:
            if norm(step) not in seen:
                next_step = norm(step)
                break

        # map next_step to dm_stage and build question list
        if next_step == "Initial Situation":
            dm_stage, questions = 0, []
        elif next_step and next_step.startswith("Inject"):
            # Inject 2 → stage 2; Inject 3 → stage 4
            num = int(next_step.split()[1])
            dm_stage = 2 if num == 2 else 4
            questions = []
        elif next_step:
            # Decision… find which block it belongs to
            # core decisions → stage 1
            if any(norm(q["inject"]) == next_step for q in core):
                dm_stage, questions = 1, core
            # branch decisions → stage 3
            elif any(norm(q["inject"]) == next_step for q in branch):
                dm_stage, questions = 3, branch
            # final decisions → stage 5
            else:
                dm_stage, questions = 5, final
        else:
            # everyone done
            dm_stage, questions = 6, [] 

        # store state
        ss.all_questions = questions
        ss.current_decision_index = (
            None if not questions else
            # +1 so that run()’s `index - 1` lands on the right question
            next(i for i, q in enumerate(questions) if norm(q["inject"]) == next_step) + 1
        )

        ss.dm_stage = dm_stage
        ss._stage_locked = True
        nav_to("dm_questionnaire")
        return



def page_past_simulations():
    st.header("📜 Past Simulations")
    if st.button("🏠 Main Menu"):
        nav_to("welcome"); return

    # 1) Get only 'finished' sims
    try:
        res = (
            supabase
            .from_("simulation")
            .select("id,name,status,started_at,finished_at")
            .eq("status", "finished")          # ← only 'finished'
            .order("finished_at", desc=True)
            .execute()
        )
    except Exception as e:
        st.info("Failed to load simulations from Supabase.⏳ Loading… please wait a moment.")
        st_autorefresh(interval=2000, limit=None, key="retry_answers")
        return

    if getattr(res, "error", None):
        st.error("Supabase error loading simulations:")
        st.write(res.error)
        return

    sims = res.data or []
    if not sims:
        st.info("No finished simulations.")
        return

    # 2) Render the list
    for sim in sims:
        finished = (sim.get("finished_at") or "")[:10]
        st.subheader(f"{sim['name']} (finished on {finished})")

        # Stash basic sim info in state
        st.session_state.simulation_id   = sim["id"]
        st.session_state.simulation_name = sim["name"]

        role = st.session_state.get("user_role")
        profile_id = st.session_state.get("profile_id")
        if not profile_id:
            st.error("⚠️ You must be logged in to view past results.")
            return

        if role == "participant":
            col1, col2 = st.columns(2)

            with col1:
                if st.button("👤 My Results", key=f"ind_{sim['id']}"):
                    # fetch this participant row
                    try:
                        part_resp = (
                            supabase
                            .from_("participant")
                            .select("id, participant_role")
                            .eq("id_simulation", sim["id"])
                            .eq("id_profile", profile_id)
                            .maybe_single()
                            .execute()
                        )
                    except Exception:
                        st.info("⏳ Loading… please wait a moment.")
                        st_autorefresh(interval=2000, limit=None, key="retry_answers")
                        return
                    if not part_resp.data:
                        st.error("You did not participate in this simulation.")
                        return
                    st.session_state.participant_id = part_resp.data["id"]
                    st.session_state.dm_role        = part_resp.data["participant_role"]
                    nav_to("individual_results")

            with col2:
                if st.button("👥 Team Results", key=f"team_{sim['id']}"):
                    nav_to("team_results")

        elif role == "supervisor":
            col1, col2 = st.columns(2)

            with col1:
                if st.button("👥 Team Results", key=f"team_{sim['id']}"):
                    nav_to("team_results")

            with col2:
                # choose a role to inspect
                try:
                    part_resp = (
                        supabase
                        .from_("participant")
                        .select("id, participant_role")
                        .eq("id_simulation", sim["id"])
                        .execute()
                    )
                except Exception:
                    st.info("⏳ Loading… please wait a moment.")
                    st_autorefresh(interval=2000, limit=None, key="retry_answers")
                    return
                if part_resp.error:
                    st.error(f"Couldn’t load participants: {part_resp.error.message}")
                    return

                participants = part_resp.data or []
                if not participants:
                    st.info("No participants in that simulation.")
                    return

                role_map = {p["participant_role"]: p["id"] for p in participants}
                choice = st.selectbox("Pick a role", list(role_map.keys()),
                                      key=f"sup_select_{sim['id']}")
                if st.button("👤 View Individual Results", key=f"sup_view_{sim['id']}"):
                    st.session_state.participant_id = role_map[choice]
                    st.session_state.dm_role        = choice
                    nav_to("individual_results")

        elif role == "manager":
            if st.button("📊 Dashboard", key=f"dash_{sim['id']}"):
                nav_to("dashboard")
        else:  # administrator
            if st.button("🛠 Control Center", key=f"cc_{sim['id']}"):
                nav_to("control_center")



#
# ——— Main routing ——————————————————————————————————————————————————————————————
#
def init_state():
    """Initialize persistent bits once per session."""
    st.session_state.setdefault('simulation_certified', False)
    st.session_state.setdefault('role', None)
    st.session_state.setdefault('simulation_name', '')
    st.session_state.setdefault("dm_stage",0)
    st.session_state.setdefault("dm_started_marker", False)
    st.session_state.setdefault('teamwork_submitted', False)
    st.session_state.setdefault('dm_finished', False)
    st.session_state.setdefault('page', 'welcome')
    st.session_state.setdefault('answers', {})
    st.session_state.setdefault("answer_times",      {})
    st.session_state.setdefault("question_text_map", {})
    st.session_state.setdefault('roles', [])
    st.session_state.setdefault('tlx_answers', {})
    st.session_state.setdefault("dashboard_shown", False)
    st.session_state.setdefault('simulation_id', None)
    st.session_state.setdefault('participant_id', None)
    st.session_state.setdefault("teamwork", False)

    st.session_state.setdefault("answers_cache", [])        # lista acumulada de respostas (delta merge)
    st.session_state.setdefault("last_answer_id", 0)        # maior ID recebido até agora
    st.session_state.setdefault("participants_cache", [])   # cache de participantes da simulação
    st.session_state.setdefault("vitals_cache", [])         # cache de vitals (se aplicável)
    st.session_state.setdefault("last_snapshot_ts", 0.0)

def main():
    init_state()
    st.session_state.setdefault("simulation_id", None)
    st.session_state.setdefault("participant_id", None)
    st.session_state.setdefault("user_role", None)

    # 1) Must log in first
    if "user" not in st.session_state:
        page_login()
        return

    # 2) Compute which pages this role may see before selecting/creating a simulation
    base_open = {"welcome", "page_login", "running_simulations", "past_simulations","participant_new_simulation"}
    role_open = {
        "administrator": {"supervisor_menu", "admin_panel"},
        "supervisor":    {"supervisor_menu"},
        "manager":       {"supervisor_menu"},  # or whatever your manager sees
        "participant":   {"dm_role_claim"},
    }
    open_pages = base_open.union(role_open.get(st.session_state.user_role, set()))

    page = st.session_state.page

    # 3) If this is a supervisor/manager page, go there immediately
    if page == "supervisor_menu":
        page_create_new_simulation()
        return

    # 4) For any other page not in open_pages, ensure we have a simulation
    if page not in open_pages and st.session_state.simulation_id is None:
        st.error("⛔ You need to create or select a simulation first.")
        if st.button("Go to Supervisor Setup"):
            nav_to("supervisor_menu")
        return
    
    pages = {
        'welcome':             page_welcome,
        'page_login':          page_login,
        'supervisor_menu':     page_create_new_simulation,
        'roles_claimed_supervisor': roles_claimed_supervisor,
        'page_supervisor_menu': page_supervisor_menu,
        'participant_new_simulation': participant_new_simulation,
        'dm_role_claim':       page_dm_role_claim,
        'dm_questionnaire':    page_dm_questionnaire,
        'live_dashboard':      page_live_dashboard,
        'override_interface':  page_override_interface,
        'teamwork_survey':     page_teamwork_survey,
        'page_one':            page_one,
        'certify_and_results': page_certify_and_results,
        'team_results':        page_team_results,
        'individual_results':  page_individual_results,
        'menu_iniciar_simulação_supervisor': page_simulation_menu,
        'dashboard':           page_dashboard,
        'running_simulations': page_running_simulations,
        'past_simulations':    page_past_simulations,
        'control_center':      page_dashboard,
    }
    pages.get(page, page_welcome)()

if __name__ == '__main__':
    main()




