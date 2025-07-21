# chiron_control_center.py
import streamlit as st
import data_simulation          # your wrapper now exposes run(simulation_name)               # sets st.session_state['teamwork_submitted']=True
import questionnaire1           # sets st.session_state['dm_finished']=True
import os, json
import pandas as pd
from questionnaire1 import  decisions1to13, decisions14to23, decisions24to28, decisions29to32, decisions33to34, decisions35to43
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
from datetime import datetime, timedelta
from questionnaire1 import get_inject_text
from reportlab.platypus import Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table as RLTable
from reportlab.platypus import Image as RLImage
from typing import Dict
import time, random


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
    answers_delta = (supabase
        .from_("answers")
        .select("id,id_simulation, simulation_name, id_participant, participant_role, inject,answer_text, basic_life_support, primary_survey, secondary_survey, definitive_care, crew_roles_communication, systems_procedural_knowledge, response_time")
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
        questionnaire1.decisions1to13,
        *questionnaire1.decisions14to23.values(),
        *questionnaire1.decisions24to28.values(),
        *questionnaire1.decisions29to32.values(),
        *questionnaire1.decisions33to34.values(),
        *questionnaire1.decisions35to43.values(),
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
                    prof = supabase.from_("profiles") \
                                .select("email") \
                                .eq("username", login_id) \
                                .single().execute()
                    if prof.error or not prof.data:
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
                    st.error(f"Could not load profile: {e}")
                
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
                else:
                    code = int(role_code)
                    role_map = {140:"administrator", 198:"supervisor", 220:"participant"}
                    if code not in role_map:
                        st.error("Invalid profile type code.")
                    else:
                        try:
                            auth_res = auth.sign_up({
                                "email":    signup_email,
                                "password": signup_password
                            })
                            st.write(auth_res.user.id)
                        except Exception as e:
                            st.error(f"Sign‑up failed: {e}")
                        else:
                            sup_res = supabase.from_("profiles")\
                                .insert({
                                    "id":                auth_res.user.id,
                                    "username":          signup_user,
                                    "email":             signup_email,
                                    "role":              role_map[code],
                                    "profile_type_code": code
                                })\
                                .execute()
                            if sup_res.error:
                                st.error("Profile insert failed: " + sup_res.error.message)
                                return
                            else:
                                st.success("✅ Registered! Check your email, then come back to log in.")
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
    st.error(f"❌ Erro na ligação ao Supabase: {e}")


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
                    st.error(f"❌ Could not create simulation: {e}")
                    return

                st.success(f"✅ Created '{new_name}' (id={created['id']})")
                st.session_state.simulation_id   = created["id"]
                st.session_state.simulation_name = new_name
                st.success(f"✅ Created '{sim_name}' (id={created['id']})")
                st.session_state.simulation_id   = created["id"]
                st.session_state.simulation_name = sim_name
                # reset caches for fresh sim context
                st.session_state.answers_cache      = []
                st.session_state.last_answer_id     = 0
                st.session_state.participants_cache = []
                st.session_state.last_snapshot_ts   = 0.0
                # Invalidar cache de pending para que desapareça imediatamente
                load_pending.clear()
                nav_to("roles_claimed_supervisor")

def roles_claimed_supervisor():
    role = st.session_state.user_role
    if role not in ("supervisor", "administrator"):
        st.warning("🔒 Please wait for the Supervisor to create a simulation first.")
        return

    sim_id = st.session_state.get("simulation_id")
    sim_id = st.session_state.get("simulation_id")
    if not sim_id:
        st.error("No simulation selected.")
        return
    

    # now sim_id is set; fetch the roles_logged
    @st.cache_data(ttl=3)
    def load_sim_roles(sim_id: str):
        resp = (supabase
                .from_("simulation")
                .select("status, roles_logged, name, started_at")
                .eq("id", sim_id)
                .single()
                .execute())
        return resp.data

    sim_row = load_sim_roles(sim_id)
    if not sim_row:
        st.error("❌ Could not load simulation (empty response).")
        return
    name         = sim_row.get("name","")
    roles_logged = sim_row.get("roles_logged") or []
    status       = sim_row.get("status")
    
    st.subheader(f"New Simulation: **{name}**")

    #roles_logged = sim_res.data.get("roles_logged") or []

    st.subheader("Roles Claimed")
    if not roles_logged:
        st.write("_None yet_")
    else:
        missing = [r for r in ("FD","FS","CAPCOM")
                   if r not in roles_logged]
        st.markdown("**Current:** " + ", ".join(roles_logged))
        if missing:
            st.markdown("**Missing:** " + ", ".join(missing))
        st.progress(len(roles_logged)/8)
    
    if st.button("🔄 Refresh"):
        load_sim_roles.clear()
        st.rerun()
    
    can_start = (len(roles_logged) == 8)
    if st.button("▶️ Start Simulation", disabled=not can_start):
        # Use a proper timestamp; let backend set started_at via RPC or now in Python:
        from datetime import datetime, timezone
        started_at = datetime.now(timezone.utc).isoformat()
        try:
            supabase.from_("simulation") \
                .update({"status": "running", "started_at": started_at}) \
                .eq("id", sim_id) \
                .execute()
        except Exception as e:
            st.error(f"❌ Failed to start simulation: {e}")
            return
        # Reset live caches for new phase
        st.session_state.answers_cache      = []
        st.session_state.last_answer_id     = 0
        st.session_state.participants_cache = []
        st.session_state.last_snapshot_ts   = 0.0
        st.session_state.dm_stage     = 0
        st.session_state.dm_finished  = False
        load_sim_roles.clear()
        nav_to("menu_iniciar_simulação_supervisor")

    if st.button("Go back to the Main Menu"):
            nav_to("welcome")

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
            st.error(f"❌ Could not look up new simulations: {e}")
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
    in_other = (current_sim_id is not None) and (current_sim_id != sim["id"])

    # Disabled final TEM de ser bool
    disabled_join = bool(is_full or in_other)

    if is_full:
        help_text = f"Simulation full ({claimed}/{MAX_ROLES})."
    elif in_other:
        help_text = "You are already in another simulation. Leave it first."
    else:
        help_text = f"{claimed}/{MAX_ROLES} roles claimed."


    if st.button("Join this Simulation", disabled=disabled_join, help=help_text):
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


def page_dm_role_claim(key_prefix: str = ""):
    st.header("Claim Your Role")

    # 1) Poll while we’re still waiting to join
    sim_id = st.session_state.get("simulation_id")
    if not sim_id:
        st.warning("🔒 No simulation selected yet — waiting for supervisor.")
        st_autorefresh(interval=5000, key=f"{key_prefix}-wait")
        return

    st_autorefresh(interval=5000, key=f"{key_prefix}-poll")

    try:
        sim_row, parts = _load_sim_and_participants(sim_id)
        if not sim_row:
            st.error("❌ Simulation not found.")
            return
    except Exception as e:
        st.error(f"❌ Could not load simulation or participants: {e}")
        return

    name = sim_row.get("name","")
    roles_logged = sim_row.get("roles_logged") or []
    taken_set = set(roles_logged)
    claimed_count = len(roles_logged)

    st.subheader(f"Simulation: **{name}**")
    if st.button("Go back to the Main Menu", key=f"{key_prefix}-back"):
            nav_to("welcome")

    # 3) Show roles already taken
    st.subheader("Roles Status")
    st.write(f"Roles claimed: **{claimed_count}/8**")
    if roles_logged:
        missing = [r for r in ALL_ROLES if r not in taken_set]
        st.markdown("**Claimed:** " + ", ".join(roles_logged))
        if missing:
            st.markdown("**Available:** " + ", ".join(missing))
    else:
        st.info("No roles claimed yet.")
    if st.button("🔄 Refresh", key=f"{key_prefix}-refresh"):
        _load_sim_and_participants.clear()
        st.rerun()

    # 4) Have I already claimed one?
    user_id = st.session_state.user.id
    me_row = next((p for p in parts if p["id_profile"] == user_id), None)
    if me_row:
        st.success(f"✅ You are **{me_row['participant_role']}**.")
        st.session_state.participant_id = me_row["id"]
        st.session_state.dm_role = me_row["participant_role"]
        if claimed_count == MAX_ROLES and st.button("▶️ Start Simulation", key=f"{key_prefix}-start"):
            st.session_state.answers_cache = []
            st.session_state.last_answer_id = 0
            st.session_state.participants_cache = []
            st.session_state.last_snapshot_ts = 0.0
            nav_to("dm_questionnaire")
        else:
            st.info(f"Waiting for all roles… ({claimed_count}/{MAX_ROLES})")
        return

    # 5) Otherwise show the “pick a role” form
    st.markdown("---")
    st.subheader("Select Your Role")
    available = [r for r in ALL_ROLES if r not in taken_set]
    choice = st.selectbox("Choose your role", options=available, key=f"{key_prefix}-role_choice")

    # 6) Show its description immediately
    st.write(questionnaire1.roles.get(choice, "_No description available._"))

    if st.button("Submit Role", key=f"{key_prefix}-submit_role"):
        _load_sim_and_participants.clear()
        latest_sim, latest_parts = _load_sim_and_participants(sim_id)
        latest_roles = set(latest_sim.get("roles_logged") or [])
        if choice in latest_roles:
            st.warning(f"Role **{choice}** was just taken. Pick another.")
            st.rerun()
            return
        try:
            ins = (supabase
                   .from_("participant")
                   .insert({
                       "id_simulation": sim_id,
                       "participant_role": choice,
                       "id_profile": user_id
                   })
                   .execute())
            new_pid = ins.data[0]["id"]
            st.session_state.participant_id = new_pid
            st.session_state.dm_role = choice
        except Exception as e:
            st.error(f"❌ Could not register you as participant: {e}")
            return
        try:
            new_roles = list(latest_roles) + [choice]
            up = (supabase
                  .from_("simulation")
                  .update({"roles_logged": new_roles})
                  .eq("id", sim_id)
                  .execute())
            if not up.data:
                raise RuntimeError("Empty update response.")
        except Exception as e:
            st.error(f"❌ Could not update simulation roles: {e}")
            return
        st.success(f"✅ Role **{choice}** claimed!")
        _load_sim_and_participants.clear()
        st.rerun()

    # 7) Fallback “waiting” UI if they somehow fall through
    if claimed_count == 8:
        st.markdown("---")
        if st.button("▶️ Start Simulation", key=f"{key_prefix}-fallback_start"):
            st.session_state.dm_stage = 0
            st.session_state.dm_finished = False
            nav_to("dm_questionnaire")
    else:
        st.info(f"Waiting for all roles ({claimed_count}/8 claimed)…")

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
    sync_simulation_state(sim_id)
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
            st.warning(f"⚠️ Could not mark start (continuing): {e}")

        st.session_state.dm_started_marker = True

    # —————————————————————
    # 2) Run the questionnaire engine
  
    stage = st.session_state.dm_stage
    # only default to 1 on actual decision stages, not injects
    if stage not in (1, 3, 5, 7) \
    and not isinstance(st.session_state.get("current_decision_index"), int):
        st.session_state.current_decision_index = 1

    # def _cache_append_answer(row):
    #     st.session_state.answers_cache.append(row)
    #     st.session_state.last_answer_id = max(
    #         st.session_state.last_answer_id,
    #         row.get("id", st.session_state.last_answer_id)
    #     )

    questionnaire1.run(
        supabase,
        simulation_name=st.session_state.simulation_name,
        role=role # ignored if not implemented
    )

    st.session_state.roles = [
      "FE-3 (EVA2)", "Commander (CMO,IV2)", "FE-1 (EVA1)", "FE-2 (IV1)",
      "FD", "FS", "BME", "CAPCOM",
    ]

    if st.session_state.get("dm_stage") == 13 and st.button("✅ Submit and Continue", key=f"{key_prefix}-submit_continue"):
        # 1) mark this participant finished
        try:
            finish_iso = datetime.utcnow().isoformat() + "Z"
            supabase.from_("participant").update(
                {"finished_at": finish_iso}
            ).eq("id", part_id).execute()
            st.success("✅ Finish time recorded!")
        except Exception as e:
            st.error(f"❌ Could not mark finished: {e}")
            return

        # 4) onward to individual results
        nav_to("individual_results")
        return


#----------------------------------------------------Page 4 - Supervisor---------------------------------------------------------------
# at the top of questionnaire1.py (or wherever render_participant_live lives)
from questionnaire1 import (
    decisions1to13,
    decisions14to23,
    decisions24to28,
    decisions29to32,
    decisions33to34,
    decisions35to43,
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

    # (Optional) simulation status kept outside; if you still need it,
    # ensure you cached `status` when you fetched the simulation.
    sim_status = st.session_state.get("simulation_status", "running")
    if sim_status != "running":
        st.write("⏳ Waiting for simulation to start…")
        return

    # Gather all answers for this simulation
    answers_by_part = build_answers_by_part(sim_id)
    my_answers = answers_by_part.get(pid, [])
    # Build quick lookups
    my_answer_map = {normalize_inject(a["inject"]): a for a in my_answers}

    # FD Key decisions from FD participant (found once)
    fd_id = None
    for p in st.session_state.participants_cache:
        if p["participant_role"] == "FD":
            fd_id = p["id"]
            break

    fd_answers = {}
    if fd_id:
        for a in answers_by_part.get(fd_id, []):
            pref = normalize_inject(a["inject"])
            if pref in {"Decision 7", "Decision 13", "Decision 23", "Decision 34"}:
                fd_answers[pref] = a.get("answer_text")

    ans7  = fd_answers.get("Decision 7")
    ans13 = fd_answers.get("Decision 13")
    ans23 = fd_answers.get("Decision 23")
    ans34 = fd_answers.get("Decision 34")

    # Resolve dynamic blocks
    block1 = decisions1to13
    block2 = decisions14to23.get((ans7, ans13), [])
    block3 = decisions24to28.get((ans7, ans13), [])
    block4 = decisions29to32.get((ans7, ans13), [])
    block5 = decisions33to34.get((ans7, ans13, ans23), [])
    block6 = decisions35to43.get((ans7, ans13, ans23, ans34), [])

    # Canonical ordered step list (inject markers included)
    steps = []
    steps.append("Inject 1")
    steps.extend(d["inject"] for d in block1)
    steps.append("Inject 2")
    steps.extend(d["inject"] for d in block2)
    steps.append("Inject 3")
    steps.extend(d["inject"] for d in block3)
    steps.append("Inject 4")
    steps.extend(d["inject"] for d in block4)
    steps.extend(d["inject"] for d in block5)
    steps.extend(d["inject"] for d in block6)

    # Count logic using cache only
    # Precompute per-step counts (all participants)
    # We need answer rows of all participants in sim:
    sim_answers = [a for a in st.session_state.answers_cache if a["id_simulation"] == sim_id]
    step_counts = {}
    for a in sim_answers:
        pref = normalize_inject(a["inject"])
        # Determine “countable”
        if pref.startswith("Inject"):
            if a.get("answer_text") == "DONE":
                step_counts[pref] = step_counts.get(pref, 0) + 1
        else:
            # decision counts any answer not SKIP
            if a.get("answer_text") and a["answer_text"] != "SKIP":
                step_counts[pref] = step_counts.get(pref, 0) + 1

    key_decisions = {"Decision 7", "Decision 13", "Decision 23", "Decision 34"}

    # Decide current step
    current = "Finished"
    for s in steps:
        pref = normalize_inject(s)
        needed = 1 if pref in key_decisions else 8
        if step_counts.get(pref, 0) < needed:
            current = pref
            break

    st.markdown(f"**Current stage:** {current}")

    if current == "Initial Situation":
        # If you have a special initial situation text function
        txt = questionnaire1.initial_situation_text if hasattr(questionnaire1, "initial_situation_text") else "Initial Situation"
        st.write(txt)
        return
    if current == "Finished":
        st.success("✅ All steps completed.")
        return

    # Lookup a step's question definition
    def lookup(pref: str):
        for blk in (block1, block2, block3, block4, block5, block6):
            for d in blk:
                if normalize_inject(d["inject"]) == pref:
                    # Resolve role-specific override
                    txt = d.get("text", "")
                    opts = d.get("options", [])
                    rs = d.get("role_specific", {})
                    if role in rs:
                        txt = rs[role].get("text", txt)
                        opts = rs[role].get("options", opts)
                    return d["inject"], txt, opts
        return pref, "_Prompt not found_", []

    # Render logic
    if current in key_decisions:
        inject_label, prompt, opts = lookup(current)
        st.markdown(f"### {inject_label}")
        if role == "FD":
            st.info("FD decision panel (read-only here). Use questionnaire view to answer.")
        fd_ans = fd_answers.get(current)
        if fd_ans:
            st.success(f"FD answered: **{fd_ans}**")
        else:
            st.warning("FD has not answered yet.")
        return

    if current.startswith("Inject"):
        st.markdown(f"### {current}")
        my_row = my_answer_map.get(current)
        my_done = (my_row and my_row.get("answer_text") == "DONE")
        cnt = step_counts.get(current, 0)
        if my_done:
            st.info(f"You marked DONE. Waiting others… ({cnt}/8)")
        else:
            st.warning("The participant hasn't clicked next yet.")
        return

    # Regular decision
    inject_label, prompt, opts = lookup(current)
    st.markdown(f"### {inject_label}")
    st.write(prompt)
    if opts:
        st.markdown("**Options:**")
        for o in opts:
            st.write(f"- {o}")

    my_dec = my_answer_map.get(current)
    cnt = step_counts.get(current, 0)
    if my_dec:
        st.success(f"Your answer: **{my_dec.get('answer_text','')}**")
        if cnt < 8:
            st.info(f"Waiting others… ({cnt}/8)")
        else:
            st.info("All participants answered. Advancing…")
    else:
        st.warning("You have not answered yet (use questionnaire page).")


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
    

def page_live_dashboard():
    st.header("Supervisor Live Dashboard")

    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name", "")

    if not sim_id:
        st.error("No simulation selected.")
        if st.button("Go back to Main Menu"):
            nav_to("welcome")
        return

    # 1) Sync snapshot FIRST (answers + participants)
    sync_simulation_state(sim_id)          # respects ttl
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
        if st.button("🔄 Hard Refresh", key="refresh_force"):
            fetch_snapshot.clear()
            sync_simulation_state(sim_id)
            st.rerun()

    st.subheader(f"Simulation: {sim_name}")
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=2000, limit=None, key="vitals_autorefresh")

    # 2) Build roster from participants_cache (no new query)
    participants_cache = st.session_state.get("participants_cache", [])
    roster = {p["participant_role"]: p["id"] for p in participants_cache if p.get("participant_role")}

    EXPECTED_ROLES = [
        "FE-3 (EVA2)", "Commander (CMO,IV2)", "FE-1 (EVA1)", "FE-2 (IV1)",
        "FD", "FS", "BME", "CAPCOM",
    ]

    # 3) Dashboard grid
    st.markdown("### Roles")
    top_row  = EXPECTED_ROLES[:4]
    bottom_row = EXPECTED_ROLES[4:]

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
                if pref in {"Decision 7", "Decision 13", "Decision 23", "Decision 34"}:
                    fd_answers[pref] = a.get("answer_text")

    ans7  = fd_answers.get("Decision 7")
    ans13 = fd_answers.get("Decision 13")
    ans23 = fd_answers.get("Decision 23")
    ans34 = fd_answers.get("Decision 34")

    # 4) Build active blocks (same logic used elsewhere)
    block1 = decisions1to13
    block2 = decisions14to23.get((ans7, ans13), [])
    block3 = decisions24to28.get((ans7, ans13), [])
    block4 = decisions29to32.get((ans7, ans13), [])
    block5 = decisions33to34.get((ans7, ans13, ans23), [])
    block6 = decisions35to43.get((ans7, ans13, ans23, ans34), [])

    active_blocks = [block1, block2, block3, block4, block5, block6]

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
            st.error(f"❌ Override failed: {e}")

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
                st.error(f"❌ Delete failed: {e}")



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
        if st.button("🔄 Hard Refresh"):
            fetch_snapshot.clear()
            sync_simulation_state(sim_id)
            st.rerun()

    st.subheader(f"Decision Support Dashboard — {sim_name}")

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

    # Prevent duplicates: see if one already exists
    @st.cache_data(ttl=5)
    def _load_existing_teamwork(sim_id_: int):
        try:
            res = (supabase
                   .from_("teamwork")
                   .select("id, leadership, teamwork, task_management, overall_performance, total, comments")
                   .eq("id_simulation", sim_id_)
                   .maybe_single()
                   .execute())
            return res.data
        except Exception:
            return None

    existing = _load_existing_teamwork(sim_id)

    if existing and "teamwork_edit_mode" not in st.session_state:
        st.success("An assessment already exists for this simulation.")
        with st.expander("View Existing Assessment", expanded=True):
            st.write(f"**Leadership:** {existing['leadership']}")
            st.write(f"**Teamwork:** {existing['teamwork']}")
            st.write(f"**Task Mgmt:** {existing['task_management']}")
            st.write(f"**Overall:** {existing['overall_performance']}")
            st.write(f"**Total:** {existing['total']}")
            if existing.get("comments"):
                st.write(f"**Comments:** {existing['comments']}")
        # If you want to allow editing, add a button:
        if st.button("Edit Assessment"):
            st.session_state.teamwork_edit_mode = True
            st.rerun()
        if st.button("Go to Results"):
            nav_to("certify_and_results")
        return

    # ---- Form State (persist across reruns) ----
    if "teamwork_responses" not in st.session_state:
        st.session_state.teamwork_responses = {}

    resp: Dict[str, str] = st.session_state.teamwork_responses

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
    st.markdown("### 🧭 Leadership")
    st.caption("If no leader emerges allocate ‘0’ to Q1 & Q2.")
    resp['Q1'] = st.selectbox(
        "1. The team leader let the team know what was expected through direction and command",
        likert_options,
        index=likert_options.index(resp.get('Q1', likert_options[0])) if resp.get('Q1') else 0,
        key="TEAM_Q1"
    )
    resp['Q2'] = st.selectbox(
        "2. The team leader maintained a global perspective (monitoring, delegation)",
        likert_options,
        index=likert_options.index(resp.get('Q2', likert_options[0])) if resp.get('Q2') else 0,
        key="TEAM_Q2"
    )

    # --- Teamwork ---
    st.markdown("### 🤝 Teamwork")
    teamwork_questions = {
        3: "3. The team communicated effectively",
        4: "4. The team worked together to complete tasks in a timely manner",
        5: "5. The team acted with composure and control",
        6: "6. The team morale was positive (support, confidence, spirit)",
        7: "7. The team adapted to changing situations",
        8: "8. The team monitored and reassessed the situation",
        9: "9. The team anticipated potential actions (e.g. equipment/drugs ready)"
    }
    for i in range(3, 10):
        resp[f'Q{i}'] = st.selectbox(
            teamwork_questions[i],
            likert_options,
            index=likert_options.index(resp.get(f'Q{i}', likert_options[0])) if resp.get(f'Q{i}') else 0,
            key=f"TEAM_Q{i}"
        )

    # --- Task Management ---
    st.markdown("### 🛠️ Task Management")
    resp['Q10'] = st.selectbox(
        "10. The team prioritised tasks",
        likert_options,
        index=likert_options.index(resp.get('Q10', likert_options[0])) if resp.get('Q10') else 0,
        key="TEAM_Q10"
    )
    resp['Q11'] = st.selectbox(
        "11. The team followed approved standards/guidelines",
        likert_options,
        index=likert_options.index(resp.get('Q11', likert_options[0])) if resp.get('Q11') else 0,
        key="TEAM_Q11"
    )

    # --- Overall ---
    st.markdown("### 🌟 Overall Performance")
    # Keep slider value persistent
    default_overall = int(resp.get('Q12', 5)) if str(resp.get('Q12', '')).isdigit() else 5
    overall_val = st.slider(
        "12. Global rating of the team's performance (1–10)",
        1, 10, default_overall, key="TEAM_Q12_SLIDER"
    )
    resp['Q12'] = str(overall_val)

    comments_prev = resp.get("COMMENTS", "")
    comments_val = st.text_area("📝 Comments (optional):", value=comments_prev, key="TEAM_COMMENTS", height=120)
    resp["COMMENTS"] = comments_val

    st.markdown("---")
    col_submit, col_reset, col_cancel = st.columns(3)
    with col_submit:
        submit_clicked = st.button("✅ Submit Assessment")
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
        # Validate
        missing = [f"Q{i}" for i in range(1, 12) if resp.get(f"Q{i}", likert_options[0]) == likert_options[0]]
        if missing:
            st.error("⚠️ Please answer all Likert questions (Q1–Q11) before submitting.")
            return

        try:
            leadership = get_score(resp['Q1']) + get_score(resp['Q2'])
            teamwork   = sum(get_score(resp[f'Q{i}']) for i in range(3, 10))
            task       = get_score(resp['Q10']) + get_score(resp['Q11'])
            overall    = int(resp['Q12'])
            total      = leadership + teamwork + task + overall
        except Exception as e:
            st.error(f"Scoring error: {e}")
            return

        payload = {
            "id_simulation":       sim_id,
            "simulation_name":     sim_name,
            "leadership":          leadership,
            "teamwork":            teamwork,
            "task_management":     task,
            "overall_performance": overall,
            "total":               total,
            "comments":            resp.get("COMMENTS", "")
        }

        try:
            if existing:
                # Update (edit mode)
                (supabase
                 .from_("teamwork")
                 .update(payload)
                 .eq("id_simulation", sim_id)
                 .execute())
                st.success("✅ TEAM assessment updated.")
            else:
                (supabase
                 .from_("teamwork")
                 .insert(payload)
                 .execute())
                st.success("✅ TEAM assessment saved.")
        except Exception as e:
            st.error(f"❌ Failed to persist assessment: {e}")
            return

        # Clear edit mode & navigate
        st.session_state.pop("teamwork_edit_mode", None)
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
    teamwork_row = fetch_teamwork(sim_id)
    if not teamwork_row:
        st.warning("🔒 Teamwork (TEAM) assessment not submitted yet. Please complete it before certification.")
        if st.button("Go to TEAM Form"):
            nav_to("page_one")
        return

    with st.expander("View TEAM Assessment Summary", expanded=False):
        st.write(f"- Leadership: **{teamwork_row['leadership']}**")
        st.write(f"- Teamwork: **{teamwork_row['teamwork']}**")
        st.write(f"- Task Mgmt: **{teamwork_row['task_management']}**")
        st.write(f"- Overall: **{teamwork_row['overall_performance']}**")
        st.write(f"- Total: **{teamwork_row['total']}**")
        if teamwork_row.get("comments"):
            st.write(f"- Comments: _{teamwork_row['comments']}_")

    # --- Load Simulation Status ---
    sim_status_row = fetch_sim_status(sim_id)
    if not sim_status_row:
        st.error("Could not load simulation status.")
        return

    status        = sim_status_row.get("status")
    certified_at  = sim_status_row.get("certified_at")

    st.markdown(f"**Current Simulation Status:** `{status}`")
    if certified_at:
        st.info(f"Already certified at: {certified_at}")
    elif st.session_state.get("simulation_certified"):
        st.info("Certified in this session (pending page refresh).")

    # --- Allow finishing if still running/pending ---
    can_finish = status in ("running", "pending")
    finish_checkbox = False
    if can_finish and not certified_at:
        finish_checkbox = st.checkbox(
            "Mark simulation as finished upon certification",
            value=True
        )

    # --- Final Certification Action ---
    if not certified_at and st.button("✅ Certify & View Team Results", type="primary"):
        # 1) Optionally mark simulation finished
        updates = {}
        if can_finish and finish_checkbox:
            updates["status"] = "finished"
        # If you added certified_at column, set it
        if "certified_at" in (sim_status_row.keys()):
            # Use python UTC timestamp (or create RPC for now())
            updates["certified_at"] = datetime.utcnow().isoformat() + "Z"

        try:
            if updates:
                (supabase
                 .from_("simulation")
                 .update(updates)
                 .eq("id", sim_id)
                 .execute())
            st.session_state.simulation_certified = True
            st.success("✅ Simulation certified.")
            nav_to("team_results")
            return
        except Exception as e:
            st.error(f"❌ Certification failed: {e}")
            return

    # If already certified, just show button to go to results
    if certified_at or st.session_state.get("simulation_certified"):
        if st.button("🏆 View Team Results"):
            nav_to("team_results")


def page_team_results():
    """Display aggregated team performance, max comparisons, TEAM assessment, and export report."""
    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name", "")
    if not sim_id:
        st.error("No simulation selected.")
        if st.button("🏠 Main Menu"):
            nav_to("welcome")
        return

    st.header("🏆 Team Performance Results")
    st.subheader(f"Simulation: {sim_name} (id={sim_id})")

    # --- Sync snapshot (participants & answers) ---
    sync_simulation_state(sim_id)

    # --- Check simulation finished (light cached fetch) ---
    @st.cache_data(ttl=5)
    def fetch_sim_status(sim_id_):
        try:
            res = (supabase
                   .from_("simulation")
                   .select("status,name,certified_at")
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

    # --- Helpers ---
    def normalize_inject(label: str) -> str:
        import re
        if not label:
            return ""
        m = re.match(r"^(Decision \d+|Inject \d+|Initial Situation)", label.strip())
        return m.group(1) if m else label.strip()

    # --- Gather FD key decisions from cache ---
    participants_cache = st.session_state.get("participants_cache", [])
    answers_cache      = st.session_state.get("answers_cache", [])

    fd_id = next((p["id"] for p in participants_cache if p.get("participant_role") == "FD"), None)
    if not fd_id:
        st.error("Flight Director not found in participant list.")
        return

    key_needed = {"Decision 7", "Decision 13", "Decision 23", "Decision 34"}
    fd_key_answers = {}
    for a in answers_cache:
        if a["id_simulation"] != sim_id or a["id_participant"] != fd_id:
            continue
        pref = normalize_inject(a["inject"])
        if pref in key_needed and a.get("answer_text") is not None:
            fd_key_answers[pref] = a["answer_text"]

    missing = [k for k in key_needed if k not in fd_key_answers]
    if missing:
        st.error(f"Missing FD key decisions: {', '.join(missing)}")
        return

    # --- Derive scenario code (replicate existing logic) ---
    def scenario_token(dec_label: str, ans_text: str) -> str:
        """
        Turn FD answer_text into the letter-token used in scenario_code.
        Original logic took the part before '.' and first char lowercased.
        """
        base = ans_text.split(".")[0].strip().lower()  # e.g. 'b something' → 'b something'
        letter = base[0] if base else 'x'
        number = dec_label.split()[-1]  # 'Decision 7' -> '7'
        return f"{letter}{number}"

    scenario_code = ",".join([
        scenario_token("Decision 7",  fd_key_answers["Decision 7"]),
        scenario_token("Decision 13", fd_key_answers["Decision 13"]),
        scenario_token("Decision 23", fd_key_answers["Decision 23"]),
        scenario_token("Decision 34", fd_key_answers["Decision 34"]),
    ])

    st.caption(f"**Scenario code derived:** `{scenario_code}`")

    # --- Fetch individual_results (cached) ---
    @st.cache_data(ttl=10)
    def fetch_individual(sim_id_):
        try:
            res = (supabase
                   .from_("individual_results")
                   .select("basic_life_support, primary_survey, secondary_survey, "
                           "definitive_care, crew_roles_communication, systems_procedural_knowledge")
                   .eq("simulation_id", sim_id_)
                   .execute())
            return res.data or []
        except Exception:
            return []

    ind_rows = fetch_individual(sim_id)
    if not ind_rows:
        st.info("No individual aggregate results yet.")
        return

    df_ind = pd.DataFrame(ind_rows)

    MED_CATS  = ["basic_life_support", "primary_survey", "secondary_survey", "definitive_care"]
    PROC_CATS = ["crew_roles_communication", "systems_procedural_knowledge"]
    ALL_CATS  = MED_CATS + PROC_CATS

    actual_totals = df_ind[ALL_CATS].sum().to_dict()

    # --- Fetch max_scores for scenario ---
    @st.cache_data(ttl=10)
    def fetch_max_scores(code: str):
        try:
            res = (supabase
                   .from_("max_scores")
                   .select("role, category, max_value, scenario_code")
                   .eq("scenario_code", code)        # if exact match works; use .ilike if pattern
                   .execute())
            return res.data or []
        except Exception:
            return []

    ms_rows = fetch_max_scores(scenario_code)
    if not ms_rows:
        st.warning("No max_scores rows found for this scenario code.")
        team_max_by_cat = {c: 0 for c in ALL_CATS}
    else:
        df_ms = pd.DataFrame(ms_rows)
        df_ms["category"] = df_ms["category"].str.lower()
        team_max_by_cat = df_ms.groupby("category")["max_value"].sum().to_dict()
        # Ensure all categories present
        for c in ALL_CATS:
            team_max_by_cat.setdefault(c, 0)

    # --- Build table rows ---
    rows = []
    for cat in ALL_CATS:
        actual = actual_totals.get(cat, 0)
        mval   = team_max_by_cat.get(cat, 0)
        pct    = f"{(100*actual/mval):.1f}%" if mval else "—"
        rows.append([
            cat.replace("_", " ").title(),
            actual,
            mval,
            pct
        ])

    med_actual_sum  = sum(actual_totals[c] for c in MED_CATS)
    med_max_sum     = sum(team_max_by_cat.get(c, 0) for c in MED_CATS)
    proc_actual_sum = sum(actual_totals[c] for c in PROC_CATS)
    proc_max_sum    = sum(team_max_by_cat.get(c, 0) for c in PROC_CATS)
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

    # --- TEAM (supervisor) assessment ---
    @st.cache_data(ttl=10)
    def fetch_teamwork(sim_id_):
        try:
            res = (supabase
                   .from_("teamwork")
                   .select("leadership, teamwork, task_management, overall_performance, total, comments, created_at")
                   .eq("id_simulation", sim_id_)
                   .maybe_single()
                   .execute())
            return res.data
        except Exception:
            return None

    tw_row = fetch_teamwork(sim_id)
    if tw_row:
        st.subheader("🔹 Supervisor’s TEAM Assessment")
        tw_labels  = ["Leadership", "Teamwork", "Task Mgmt", "Overall", "Total"]
        tw_cols    = ["leadership", "teamwork", "task_management", "overall_performance", "total"]
        tw_values  = [tw_row[c] for c in tw_cols]
        tw_maxes   = [8, 28, 8, 10, 54]  # domain maxima

        x = np.arange(len(tw_labels))
        width = 0.35
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(x - width/2, tw_values, width, label="Score")
        ax.bar(x + width/2, tw_maxes,  width, label="Max")
        ax.set_xticks(x)
        ax.set_xticklabels(tw_labels, rotation=0)
        ax.set_ylabel("Points")
        ax.set_title("TEAM Scores vs Max")
        ax.legend()
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

        with st.expander("TEAM Details"):
            st.write(f"- Leadership: **{tw_row['leadership']}** / 8")
            st.write(f"- Teamwork: **{tw_row['teamwork']}** / 28")
            st.write(f"- Task Mgmt: **{tw_row['task_management']}** / 8")
            st.write(f"- Overall: **{tw_row['overall_performance']}** / 10")
            st.write(f"- Total: **{tw_row['total']}** / 54")
            if tw_row.get("comments"):
                st.write(f"_Comments:_ {tw_row['comments']}")

    else:
        st.info("No TEAM assessment found.")

    st.markdown("---")

    # --- PDF Generation (Lazy) ---
    def build_team_pdf(df_scores: pd.DataFrame,
                       team_assessment: dict | None,
                       scenario_code_: str) -> io.BytesIO:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table as RLTable, TableStyle, Image as RLImage
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.colors import HexColor

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        elems = [
            Paragraph("Team Performance Report", styles["Title"]),
            Paragraph(f"Simulation: {sim_name}", styles["Normal"]),
            Paragraph(f"Scenario Code: {scenario_code_}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph("Team Scores vs Maximum", styles["Heading2"])
        ]

        data = [df_scores.columns.tolist()] + df_scores.values.tolist()
        tbl = RLTable(data, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), HexColor("#1F4E78")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
            ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 18))

        if team_assessment:
            elems.append(Paragraph("TEAM Assessment", styles["Heading2"]))
            elems.append(Paragraph(
                f"Leadership: {team_assessment['leadership']} / 8, "
                f"Teamwork: {team_assessment['teamwork']} / 28, "
                f"Task Mgmt: {team_assessment['task_management']} / 8, "
                f"Overall: {team_assessment['overall_performance']} / 10, "
                f"Total: {team_assessment['total']} / 54",
                styles["Normal"]
            ))
            if team_assessment.get("comments"):
                elems.append(Paragraph(f"Comments: {team_assessment['comments']}", styles["Italic"]))
            elems.append(Spacer(1, 12))

        doc.build(elems)
        buf.seek(0)
        return buf

    col_pdf, col_nav = st.columns([1,1])
    with col_pdf:
        if st.button("📄 Generate PDF Report"):
            pdf_buffer = build_team_pdf(df_team_vs_max, tw_row, scenario_code)
            st.download_button(
                "⬇️ Download Report",
                data=pdf_buffer,
                file_name=f"{sim_name}_team_report.pdf",
                mime="application/pdf"
            )

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


def page_individual_results():
    """Show the current participant's individual performance summary."""
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

    # --- Sync snapshot (answers + participants) once ---
    sync_simulation_state(sim_id)
    answers_cache      = st.session_state.get("answers_cache", [])
    participants_cache = st.session_state.get("participants_cache", [])

    # Guard: ensure participant exists (or allow supervisor to inspect?)
    if user_role not in ("supervisor", "administrator"):
        if not any(p["id"] == part_id for p in participants_cache):
            st.error("Your participant record was not found.")
            return

    # --- Locate FD participant id (from snapshot) ---
    fd_id = next((p["id"] for p in participants_cache
                  if p.get("participant_role") == "FD"), None)
    if not fd_id:
        st.error("Flight Director not present in this simulation.")
        return

    # --- Normalize helper ---
    import re
    def norm_inject(lbl: str) -> str:
        if not lbl:
            return ""
        m = re.match(r"^(Decision \d+|Inject \d+|Initial Situation)", lbl.strip())
        return m.group(1) if m else lbl.strip()

    # --- Extract FD key decisions from answers_cache (no extra queries) ---
    key_needed = {"Decision 7", "Decision 13", "Decision 23", "Decision 34"}
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

    # --- Build scenario code (same convention as team results page) ---
    def scenario_token(decision_label: str, ans_text: str) -> str:
        base = ans_text.split(".")[0].strip().lower()
        letter = base[0] if base else "x"
        number = decision_label.split()[-1]
        return f"{letter}{number}"

    scenario_code = ",".join([
        scenario_token("Decision 7",  fd_key_answers["Decision 7"]),
        scenario_token("Decision 13", fd_key_answers["Decision 13"]),
        scenario_token("Decision 23", fd_key_answers["Decision 23"]),
        scenario_token("Decision 34", fd_key_answers["Decision 34"]),
    ])
    st.caption(f"Scenario code: `{scenario_code}`")

    # --- Load individual_results row (cached) ---
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

    # Actual scores (floats for safety)
    try:
        med_actuals  = [float(ind[c]) for c in MED_CATS]
        proc_actuals = [float(ind[c]) for c in PROC_CATS]
        med_subtot   = float(ind.get("medical_knowledge_total", sum(med_actuals)))
        proc_subtot  = float(ind.get("procedural_knowledge_total", sum(proc_actuals)))
        actual_total = float(ind.get("score", med_subtot + proc_subtot))
    except (TypeError, ValueError) as e:
        st.error(f"Malformed numeric data in individual_results: {e}")
        return

    # --- Fetch role-specific max scores for this scenario (cached) ---
    @st.cache_data(ttl=10)
    def fetch_role_maxes(role_, scen_code):
        try:
            res = (supabase
                   .from_("max_scores")
                   .select("category, max_value, scenario_code, role")
                   .eq("role", role_)
                   .eq("scenario_code", scen_code)  # use ilike if needed
                   .execute())
            return res.data or []
        except Exception:
            return []

    max_rows = fetch_role_maxes(dm_role, scenario_code)
    if not max_rows:
        st.warning("No max_scores found for your role & scenario. Percentages unavailable.")
    # Map categories (normalize lowercase)
    role_max_map = {}
    for r in max_rows:
        cat = r["category"].lower()
        role_max_map[cat] = float(r["max_value"])

    # Compute max for each atomic category; fall back to 0 if missing
    med_maxs  = [role_max_map.get(c, 0.0) for c in MED_CATS]
    proc_maxs = [role_max_map.get(c, 0.0) for c in PROC_CATS]
    med_max_sub  = sum(med_maxs)
    proc_max_sub = sum(proc_maxs)
    max_total    = med_max_sub + proc_max_sub

    # --- TLX (taskload) load (cached) ---
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

    # --- Layout: Medical & Procedural side-by-side ---
    col_med, col_proc = st.columns(2)
    import numpy as np
    import matplotlib.pyplot as plt

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
        ax_med.set_xticklabels([l.replace("_"," ").title() for l in labels], rotation=30, ha="right")
        ax_med.set_ylabel("Points")
        ax_med.legend(fontsize=8)
        fig_med.tight_layout()
        st.pyplot(fig_med, use_container_width=True)

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
        ax_proc.set_xticklabels([l.replace("_"," ").title() for l in labels], rotation=30, ha="right")
        ax_proc.set_ylabel("Points")
        ax_proc.legend(fontsize=8)
        fig_proc.tight_layout()
        st.pyplot(fig_proc, use_container_width=True)

    # --- Summary Table & TLX ---
    col_table, col_tlx = st.columns(2)

    # Build summary table rows
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
        ["Total",                actual_total, max_total,   f"{100*actual_total/max_total:.1f}%" if max_total else "—"]
    ]

    import pandas as pd
    df_summary = pd.DataFrame(rows, columns=["Category", "Your Score", "Max Score", "% of Max"])

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
        else:
            st.info("No TLX responses submitted.")

    st.markdown("---")
    st.subheader("📝 Your Raw Answers")

    # Filter this participant’s answers (from cache)
    my_answers = [a for a in answers_cache
                  if a["id_simulation"] == sim_id
                  and a["id_participant"] == part_id]

    if not my_answers:
        st.info("No answers recorded yet.")
    else:
        # Optional: order by numeric decision/inject sequence if you stored that mapping
        df_raw = pd.DataFrame(my_answers)
        # Exclude inject steps if you only want decisions
        df_show = df_raw[~df_raw["inject"].str.startswith("Inject")]
        st.dataframe(df_show[["inject", "answer_text"]], use_container_width=True)

    # --- PDF (Lazy Build) ---
    def build_pdf():
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table as RLTable, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.colors import HexColor
        import io as _io

        buf = _io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        elems = [
            Paragraph(f"Individual Performance Report", styles["Title"]),
            Paragraph(f"Simulation: {sim_name}", styles["Normal"]),
            Paragraph(f"Role: {dm_role}", styles["Normal"]),
            Paragraph(f"Scenario Code: {scenario_code}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph("Score Summary", styles["Heading2"])
        ]

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

        # (Optional) embed static summary of TLX:
        if tlx_row:
            elems.append(Paragraph("TLX Scores", styles["Heading2"]))
            tlx_text = ", ".join(f"{k.title()}: {v}" for k,v in tlx_row.items())
            elems.append(Paragraph(tlx_text, styles["Normal"]))
            elems.append(Spacer(1,12))

        doc.build(elems)
        buf.seek(0)
        return buf

    col_pdf, col_nav = st.columns([1,1])
    with col_pdf:
        if st.button("📄 Generate PDF"):
            pdf_buf = build_pdf()
            st.download_button(
                "⬇️ Download PDF",
                data=pdf_buf,
                file_name=f"{dm_role.replace(' ','_')}_results.pdf",
                mime="application/pdf"
            )

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
    st.header("🏃 Ongoing Simulations")
    if st.button("Go back to the Main Menu"):
        nav_to("welcome")
        return

    with st.spinner("Loading simulation…"):
        try:
            resp = fetch_simulations_with_retry()
        except Exception:
            st.info("Still loading… please wait a moment.")
            return
    sims = resp.data or []
    sims = [s for s in sims if s.get("status") == "running"]
    sims = sorted(
        sims,
        key=lambda s: s.get("started_at") or "",
        reverse=True
    )

    if not sims:
        st.info("No simulations currently running.")
        return

    # 2) Render header row
    header_cols = st.columns([1, 3, 3, 2])
    header_style = (
        "background-color:#004080;"
        "color:white;"
        "padding:8px;"
        "border:1px solid #ddd;"
        "text-align:center;"
    )
    header_cols[0].markdown(
        f"<div style='{header_style}'><strong>Join</strong></div>",
        unsafe_allow_html=True
    )
    header_cols[1].markdown(
        f"<div style='{header_style}'><strong>Name</strong></div>",
        unsafe_allow_html=True
    )
    header_cols[2].markdown(
        f"<div style='{header_style}'><strong>Started At</strong></div>",
        unsafe_allow_html=True
    )
    header_cols[3].markdown(
        f"<div style='{header_style}'><strong>Roles Logged</strong></div>",
        unsafe_allow_html=True
    )

    # 3) Render each simulation as a styled “row”
    cell_base = "padding:8px;border:1px solid #ddd;"
    first_col_style = "background-color:#e6f7ff;" + cell_base + "text-align:center;"
    other_col_style = cell_base

    for sim in sims:
        c0, c1, c2, c3 = st.columns([1, 3, 3, 2])

        # ── Join button in a shaded cell ──
        with c0:
            st.markdown(f"<div style='{first_col_style}'>", unsafe_allow_html=True)
            join_clicked = st.button("▶️ Join", key=f"join_{sim['id']}")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Name, Started At, Roles Logged ──
        c1.markdown(
            f"<div style='{other_col_style}'>{sim['name']}</div>",
            unsafe_allow_html=True
        )
        raw = sim.get("started_at")
        ts  = pd.to_datetime(raw)

        if pd.notna(ts):
            started = ts.strftime("%Y-%m-%d %H:%M:%S")
        else:
            started = "—"

        c2.markdown(
            f"<div style='{other_col_style}'>{started}</div>",
            unsafe_allow_html=True
        )
        c3.markdown(
            f"<div style='{other_col_style}'>{sim.get('roles_logged','—')}</div>",
            unsafe_allow_html=True
        )

        # ── Handle the join click ──
        if join_clicked:
            # set the chosen simulation in session state
            st.session_state.simulation_id   = sim["id"]
            st.session_state.simulation_name = sim["name"]
            role = st.session_state.user_role
            ss = st.session_state
            ss.setdefault("answers_cache", [])          # deve ser lista se usas .extend
            ss.setdefault("answers_delta", [])          # lista de novos
            ss.setdefault("participants_cache", {})     # dict id_participant -> info
            ss.setdefault("last_answer_id", 0)
            ss.setdefault("last_snapshot_ts", 0.0)

            if role in ("supervisor", "administrator"):
                nav_to("menu_iniciar_simulação_supervisor")
                return


            if role == "participant":
                # find this user’s participant record
                part_res = (
                    supabase
                    .from_("participant")
                    .select("id, participant_role")
                    .eq("id_profile", st.session_state.user.id)
                    .eq("id_simulation", sim["id"])
                    .maybe_single()
                    .execute()
                )
                part = getattr(part_res, "data", None)
                if not part:
                    st.error("You have not joined this simulation.")
                    return

                # set participant state
                st.session_state.participant_id = part["id"]
                st.session_state.dm_role        = part["participant_role"]

                # rebuild the question‐sequence for this scenario
                from questionnaire1 import (
                    decisions1to13, decisions14to23, decisions24to28,
                    decisions29to32, decisions33to34, decisions35to43,
                    get_role_decision_answer
                )
                ans7  = get_role_decision_answer("Decision 7",  "FD")
                ans13 = get_role_decision_answer("Decision 13", "FD")
                ans23 = get_role_decision_answer("Decision 23", "FD")
                ans34 = get_role_decision_answer("Decision 34", "FD")

                # 2) Build the three “conds” you care about
                cond1 = (ans7,  ans13)             # have we done 7 & 13 yet?
                cond2 = (ans7,  ans13, ans23)      # have we done 7,13 & 23 yet?
                cond3 = (ans7,  ans13, ans23, ans34)  # have we done all four?
                ans28 = get_role_decision_answer("Decision 28", st.session_state.dm_role)
                ans32 = get_role_decision_answer("Decision 32", st.session_state.dm_role)

                # 3) Rebuild each block based on those conds
                b1 = decisions1to13
                b2 = decisions14to23.get(cond1, [])
                b3 = decisions24to28.get(cond1, [])
                b4 = decisions29to32.get(cond1, [])
                b5 = decisions33to34.get(cond2, [])
                b6 = decisions35to43.get(cond3, [])

                next_step = None
                current_decision_index = None
                q = None


                if not all(cond1):
                    flat_questions = b1
                    inject_marker  = "Initial Situation" if not any(cond1) else "Inject 1"

                elif cond1 and not cond2[2]:
                    flat_questions = b2
                    inject_marker  = "Inject 2"

                elif cond2 and not ans28:
                    flat_questions = b3
                    inject_marker  = "Inject 3"

                elif ans28 and not ans34:
                    flat_questions = b4
                    inject_marker  = "Inject 4"

                elif ans32 and not ans34:
                    flat_questions = b5
                    inject_marker  = flat_questions[0]["inject"] if flat_questions else None

                elif cond3:
                    flat_questions = b6
                    inject_marker  = flat_questions[0]["inject"] if flat_questions else None
                    st.session_state.loaded_35to43 = True

                else:
                    inject_marker  = None

                
                #all_steps = [f"Inject {dm_stage//2}"] + [q["inject"] for q in flat_questions]
                if inject_marker:
                    all_steps = [inject_marker] + [q["inject"] for q in flat_questions]
                else:
                    all_steps = [q["inject"] for q in flat_questions]



                # 3) get the very last answered inject from your answers table
                ans_resp = (
                    supabase
                    .from_("answers")
                    .select("inject")
                    .eq("id_simulation",  sim["id"])
                    .eq("id_participant", part["id"])
                    .execute()
                )
                # helper to normalize any step-label into just its “prefix” (Decision X or Inject Y)
                import re

                def normalize(key: str) -> str:
                    key = key.strip()
                    m = re.match(r'^(Initial Situation|Inject \d+|Decision \d+)', key)
                    return m.group(1) if m else key
                
                # build a set of the step-prefixes they’ve already seen
                rows = getattr(ans_resp, "data", []) or []
                answered_raw = [r["inject"] for r in rows]
                answered      = { normalize(r["inject"]) for r in rows }

                # also mark off any FD‑only decision they did:
                KEY = { normalize(d) for d in ["Decision 7","Decision 13","Decision 23","Decision 34"] }
                for fd_pref in KEY:
                    if get_role_decision_answer(fd_pref, "FD") is not None:
                        answered.add(fd_pref)

                if st.session_state.dm_role != "FD":
                    answered |= KEY


                # after flat_questions…
                scenario_prefixes = {
                    normalize(d["inject"])
                    for d in flat_questions
                }

                inspect = []                
                next_step = None
                for step in all_steps:
                    if normalize(step) not in answered:
                        next_step = normalize(step)
                        inspect.append({
                        "step": step,
                        "pref": next_step,
                        "answered?": next_step in answered,
                        "in scenario?": (not next_step.startswith("Decision")) or (next_step in scenario_prefixes)
                    })
                        break

                st.write("DEBUG step inspection:", inspect)

                # special-case the Initial Situation inject
                if next_step == "Initial Situation":
                    dm_stage = 0
                    current_decision_index = None

                elif next_step is None:
                    dm_stage = 12
                    current_decision_index = None

                elif next_step.startswith("Inject"):
                    # e.g. "Inject 2" → stage 3
                    dm_stage = int(next_step.split()[1]) + 1
                    current_decision_index = None

                else:
                    # it really is a Decision X
                    # find it in flat_questions…
                    for rel_idx, q in enumerate(flat_questions):
                        if normalize(q["inject"]) == next_step:
                            rel = rel_idx + 1
                            break
                    else:
                        st.error(f"⚠️ Couldn't locate {next_step!r} in flat_questions")
                        return

                    # decide your stage + index
                    if flat_questions == b1:
                        dm_stage, current_decision_index = 2, rel_idx + 1
                    elif flat_questions == b2:
                        dm_stage, current_decision_index = 4, rel_idx + 1
                    elif flat_questions ==  b3:
                        dm_stage, current_decision_index = 6, rel_idx + 1
                    elif flat_questions ==  b4:
                        dm_stage, current_decision_index = 8, rel_idx + 1
                    elif flat_questions == b5:
                        dm_stage, current_decision_index = 9, rel_idx + 1
                    elif flat_questions == b6:
                        dm_stage, current_decision_index = 10, rel_idx + 1
                        st.session_state.loaded_35to43 = True
                    else:
                        dm_stage, current_decision_index = 12, rel_idx + 1

        
                # (plus mark off FD‐only decisions the same way you already do…)
                
                st.write("ALL_STEPS:", all_steps)
                st.write("ANSWERED:", answered)
                st.write("next_step:", next_step)



                # 6) stash and navigate
                # sanity check:
                # sanity check
                if not flat_questions or not isinstance(flat_questions[0], dict):
                    st.error("⚠️ `all_questions` must be a list of dicts but isn’t – please check your decision blocks.")
                    return
                
                # st.write("DEBUG chosen next_step:", next_step)
                # st.write("DEBUG dm_stage, current_decision_index:", dm_stage, current_decision_index)
                # st.write("DEBUG all_steps:", all_steps)
                # st.write("DEBUG answered prefixes:", answered)
                # st.write("DEBUG cond (FD key decisions):", cond)
                # st.write("DEBUG raw answers payload:", ans_resp.data)
                # st.write("DEBUG raw_ans list of inject labels:", raw_ans)
                # st.write("DEBUG normalized answered prefixes:", answered)
                # st.write("DEBUG scenario_prefixes (allowed decision labels):", scenario_prefixes)

                st.write("DEBUG stage", dm_stage)
                st.write("DEBUG current_decision_index", current_decision_index)
                #st.write("DEBUG flat_questions", flat_questions)
                # st.write ("DEBUG b2",b2)


                st.session_state.all_questions          = flat_questions
                st.session_state.current_decision_index = current_decision_index
                st.session_state.dm_stage               = dm_stage
                # st.write("🔍 debugging all_questions:", st.session_state.all_questions[:5])
                idx = st.session_state.current_decision_index
                st.write("🔍 debug current_decision_index:", idx)
                if idx is not None:
                    q = st.session_state.all_questions[idx]
                    st.write("🔍 debug question:", q["inject"])
                else:
                    st.write("🔍 currently at an inject, no question index to show")
                
                ans12 = get_role_decision_answer("Decision 12", st.session_state.dm_role)
                ans22 = get_role_decision_answer("Decision 22", st.session_state.dm_role)

                if (st.session_state.dm_role != "FD" and ans12 is not None and ans13 is None) or (st.session_state.dm_role != "FD" and ans22 is not None and ans23 is None):
                    st.warning("⏳ Wait for FD to answer the key decision to try to join again")
                    return

                #nav_to("dm_questionnaire")
                return

            st.error("Only supervisors or participants can join a running simulation.")
            return




def page_past_simulations():
    st.header("📜 Past Simulations")
    # Fetch all simulations whose status is “finished”
    if st.button("Go back to the Main Menu"):
            nav_to("welcome")
    
    try:
        response = (
            supabase
            .from_("simulation")
            .select("id,name,finished_at")
            .eq("status", "finished")
            .order("finished_at", desc=True)
            .execute()
        )
        sims = response.data
    except Exception as e:
        st.error(f"Error loading history: {e}")
        return

    # 2) No completed sims?
    if not sims:
        st.info("No completed simulations yet.")
        return

    # 3) List them with a View Results button
    for sim in sims:
        finished = sim["finished_at"][:10]  # just the YYYY-MM-DD
        st.write(f"**{sim['name']}** (finished on {finished})")
        st.session_state.simulation_id   = sim["id"]
        st.session_state.simulation_name = sim["name"]
        role = st.session_state.user_role
        pid = st.session_state.get("profile_id")
        if "profile_id" not in st.session_state:
            st.error("⚠️ You must be logged in to view past results.")
            return
        if role == "participant":
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button("👤 My Results", key=f"ind_{sim['id']}"):
                        # stash sim + lookup this participant
                    st.session_state.simulation_id   = sim["id"]
                    st.session_state.simulation_name = sim["name"]

                        # find participant row
                    part = (
                        supabase
                        .from_("participant")
                        .select("…")
                        .maybe_single()
                        .execute()
                    )
                    # If data comes back empty, supabase returns data=None
                    if part_resp.data is None:
                        st.error("You have not joined this simulation.")
                        return

                    st.session_state.participant_id = part["id"]
                    st.session_state.dm_role         = part["participant_role"]
                    nav_to("individual_results")

            with col2:
                if st.button("👥 Team Results", key=f"team_{sim['id']}"):
                    st.session_state.simulation_id   = sim["id"]
                    st.session_state.simulation_name = sim["name"]
                    nav_to("team_results")

        elif role == "supervisor":
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button("👥 Team Results", key=f"team_{sim['id']}"):
                    st.session_state.simulation_id   = sim["id"]
                    st.session_state.simulation_name = sim["name"]
                    nav_to("team_results")
            
            with col2:  
                part_resp = (
                        supabase
                        .from_("participant")
                        .select("id, participant_role")
                        .eq("id_simulation", sim["id"])
                        .execute()
                    )
                if part_resp.error:
                    st.error(f"Couldn’t load participants: {part_resp.error.message}")
                    return

                participants = part_resp.data or []
                if not participants:
                    st.info("No one participated in that simulation.")
                    return

                    # 2) build a mapping and a selectbox
                role_map = { p["participant_role"]: p["id"] for p in participants }
                choice = st.selectbox(
                    "Pick a role to inspect:",
                    options=list(role_map.keys()),
                    key=f"sup_select_{sim['id']}"
                )

                    # 3) when they click, navigate
                if st.button("👤 View Individual Results", key=f"sup_view_{sim['id']}"):
                    st.session_state.participant_id = role_map[choice]
                    st.session_state.dm_role         = choice
                    nav_to("individual_results")
        elif role == "manager":
            nav_to("dashboard")
        else:  # administrator
            nav_to("control_center")

#
# ——— Main routing ——————————————————————————————————————————————————————————————
#
def init_state():
    """Initialize persistent bits once per session."""
    st.session_state.setdefault('simulation_certified', False)
    st.session_state.setdefault('role', None)
    st.session_state.setdefault('simulation_name', '')
    st.session_state.setdefault("dm_stage",           1)
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




