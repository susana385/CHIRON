# chiron_control_center.py
import streamlit as st
import data_simulation          # your wrapper now exposes run(simulation_name)
import teamwork                 # sets st.session_state['teamwork_submitted']=True
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
from dotenv import load_dotenv
from supabase_client import supabase
from datetime import datetime, timedelta
from questionnaire1 import get_inject_text
from reportlab.platypus import Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table as RLTable
from reportlab.platypus import Image as RLImage
from supabase import create_client

st.set_page_config(
    page_title="CHIRON Control Center",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# local fallback
load_dotenv()

url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)
auth = supabase.auth

# Build a global map: inject ID → question text
# build a map from inject → generic prompt, and (inject, role) → role-specific prompt
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
    st.write("This system lets you **participate in**, **supervise**, **manage** or **administer** CHIRON simulations.")

    st.header("Login or Sign Up")
    email    = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # adicionado: profile type code para o sign-up
    role_code = st.text_input(
        "Profile type code (1=admin, 2=supervisor, 3=manager, 1234=participant)",
        value=""
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log In"):
            try:
                signin = auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
            except Exception as e:
                st.error(f"Sign-in failed: {e}")
            else:
                # fetch exactly one profile row
                try:
                    res = (
                        supabase
                        .from_("profiles")
                        .select("*")
                        .eq("id", signin.user.id)
                        .single()
                        .execute()
                    )
                except Exception as e:
                    st.error(f"Could not load profile: {e}")
                else:
                    profile = res.data
                    if profile:
                        st.session_state.user      = signin.user
                        st.session_state.user_role = profile["role"]
                        st.session_state.simulation_id   = None
                        st.session_state.simulation_name = None
                        st.session_state.participant_id  = None
                        st.session_state.profile   = profile
                        st.session_state.profile_id = signin.user.id
                        nav_to("welcome")
                    else:
                        st.error("❌ No profile found for this user.")

    with col2:
        if st.button("Sign Up"):
            # apenas no sign-up é obrigatório preencher o código
            if not role_code.strip():
                st.error("❗ Você deve informar o profile type code para registar.")
            else:
                if not role_code.strip():
                    st.error("You must enter a profile type code.")
                else:
                    code = int(role_code)
                    role_map = {1:"administrator", 2:"supervisor", 3:"manager", 1234:"participant"}
                    if code not in role_map:
                        st.error("Invalid code.")
                    else:
                        try:
                            auth_res = auth.sign_up({"email": email, "password": password})
                        except Exception as e:
                            st.error(f"Sign-up failed: {e}")
                        else:
                            try:
                                sup_res = supabase\
                                    .from_("profiles")\
                                    .insert({
                                        "id":   auth_res.user.id,
                                        "username": email,
                                        "role":     role_map[code],
                                        "profile_type_code": code
                                    })\
                                    .execute()
                            except Exception as e:
                                st.error(f"Could not create profile row: {e}")
                            else:
                                # success if sup_res.data is non-empty
                                if sup_res.data:
                                    st.success("✅ Registered! Please confirm your email then Sign In.")
                                else:
                                    st.error("❌ Profile insert returned no data!")
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

# ── single-value store for the “live” simulation ──
SIM_FILE = "current_simulation.txt"
ROLES_FILE = "selected_roles.json"
FRESH_FLAG = "fresh_start"

def load_selected_roles() -> list[str]:
    if os.path.exists(ROLES_FILE):
        return json.load(open(ROLES_FILE))
    return []

def save_selected_role(role: str):
    roles = load_selected_roles()
    if role not in roles:
        roles.append(role)
        json.dump(roles, open(ROLES_FILE, "w"))

def save_current(name: str):
    with open(SIM_FILE, "w") as f:
        f.write(name)

def load_current() -> str:
    if os.path.exists(SIM_FILE):
        return open(SIM_FILE).read().strip()
    return ""

def nav_to(page_name: str):
    """Helper: set the app’s current page in session_state and rerun."""
    st.session_state.page = page_name
    st.rerun()


#
# ——— Page implementations ——————————————————————————————————————————————————————————
#

#------------------------------------------------------ Page 2 - Welcome to CHIRON System ----------------------------------------------
def page_welcome():
    """
    Main menu after login. Branches on user_role:
      - participant / supervisor / manager all see New, Running & Past simulations
      - administrator gets an extra Control Center button
    """
    # clear any on-disk state on first visit in this session
    if FRESH_FLAG not in st.session_state:
        for f in (SIM_FILE, ROLES_FILE):
            if os.path.exists(f):
                os.remove(f)
        st.session_state[FRESH_FLAG] = True

    # render your logos
    show_logos([
        ("Logo_CHIRON.png", 90),
        ("IDEAS_LAB.png", 180),
        ("Novologofct2021.png", 150)
    ])

    st.title("Welcome to CHIRON System")
    st.write("This system lets you **participate in**, **supervise* *or **administer** CHIRON simulations.")

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
    try:
        resp = (
            supabase
            .from_("simulation")
            .select("id, name, roles_logged, created_at")
            .eq("status", "pending")
            .order("created_at", desc=True)
            .execute()
        )
        pending = resp.data or []
    except Exception as e:
        st.error(f"❌ Could not load pending simulations: {e}")
        return

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
                try:
                    ins = (
                        supabase
                        .from_("simulation")
                        .insert({
                            "name":         new_name,
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
                nav_to("roles_claimed_supervisor")

def roles_claimed_supervisor():
    role = st.session_state.user_role
    if role not in ("supervisor", "administrator"):
        st.warning("🔒 Please wait for the Supervisor to create a simulation first.")
        return

    sim_id = st.session_state.get("simulation_id")
    

    # now sim_id is set; fetch the roles_logged
    try:
        sim_res = (
            supabase
            .from_("simulation")
            .select("roles_logged,name")
            .eq("id", sim_id)
            .single()
            .execute()
        )
        name = sim_res.data["name"]
    except Exception as e:
        st.error(f"❌ Could not load simulation roles: {e}")
        return
    
    st.subheader(f"New Simulation: **{name}**")

    roles_logged = sim_res.data.get("roles_logged") or []

    st.subheader("Roles Claimed")
    if not roles_logged:
        st.write("_None yet_")
    else:
        for r in roles_logged:
            st.write(f"- {r}")
    
    if st.button("🔄 Refresh"):
        st.rerun()
    
    if len(roles_logged) == 8 and st.button("▶️ Start Simulation"):
        supabase.from_("simulation") \
            .update({"status": "running", "started_at": "now()"}) \
            .eq("id", sim_id) \
            .execute()
        st.session_state.dm_stage = 0
        st.session_state.dm_finished = False
        nav_to("page_supervisor_menu")

    if st.button("Go back to the Main Menu"):
            nav_to("welcome")

def page_supervisor_menu():

    sim_id = st.session_state.get("simulation_id")
    try:
        sim_res = (
            supabase
            .from_("simulation")
            .select("roles_logged")
            .eq("id", sim_id)
            .single()
            .execute()
        )
    except Exception as e:
        st.error(f"❌ Could not load simulation roles: {e}")
        return
    
    role = st.session_state.user_role
    roles_logged = sim_res.data.get("roles_logged") or []
    if role not in ("supervisor", "administrator"):
        st.warning("🔒 Please wait for the Supervisor to create a simulation first.")
        return
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("▶️ Go to Supervisor Dashboard"):
            nav_to("live_dashboard")
    
    with c2:
        if st.button("▶️ Go to Decision Suport Dashboard"):
            nav_to("dashboard")

    with c3:
        if st.button("▶️ Go to Team Assessment Form", disabled=len(roles_logged) != 8):
            nav_to("teamwork_survey")
    



# --------------------------------------------------------- Page 3 Participant----------------------------------------------------

from streamlit_autorefresh import st_autorefresh

def participant_new_simulation():
    """
    Picks the single pending simulation created in the last 5 minutes (if any).
    """
    if st.button("Go back to the Main Menu"):
            nav_to("welcome")

    five_min_ago = (datetime.utcnow() - timedelta(minutes=30)).isoformat() + "Z"
    res = (
        supabase
        .from_("simulation")
        .select("id, name, roles_logged, created_at, status")
        .eq("status", "pending")
        .gte("created_at", five_min_ago)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    # supabase-py no longer has res.error; use try/except
    try:
        sims = res.data or []
    except Exception as e:
        st.error(f"❌ Could not look up new simulations: {e}")
        return

    if not sims:
        st.info("No *very recent* pending simulations—please wait for a supervisor.")
        return

    sim = sims[0]
    if len(sim["roles_logged"]) >= 8:
        st.info("The most recent pending simulation is already full—please wait for a new one.")
        return

    st.subheader("Join the newest pending simulation:")
    st.write(f"**{sim['name']}**  (created at {sim['created_at']})")
    if st.button("Join this Simulation"):
        st.session_state.simulation_id   = sim["id"]
        st.session_state.simulation_name = sim["name"]
        nav_to("dm_role_claim")



def page_dm_role_claim(key_prefix: str = ""):
    st.header("Claim Your Role")

    # 1) Poll while we’re still waiting to join
    if (st.session_state.get("simulation_id") is None
        or st.session_state.get("participant_id") is None):
        st_autorefresh(interval=5_000, key=f"{key_prefix}-dm_wait")

    sim_id = st.session_state.get("simulation_id")
    if sim_id is None:
        st.warning("🔒 Waiting for the Supervisor to create a simulation…")
        return

    # 2) Load simulation name + all participants
    try:
        sim = supabase.from_("simulation") \
                      .select("name") \
                      .eq("id", sim_id) \
                      .single() \
                      .execute().data
        parts = supabase.from_("participant") \
                        .select("id, participant_role, id_profile") \
                        .eq("id_simulation", sim_id) \
                        .execute().data or []
    except Exception as e:
        st.error(f"❌ Could not load simulation or participants: {e}")
        return

    name = sim["name"]
    st.subheader(f"Simulation: **{name}**")
    if st.button("Go back to the Main Menu", key=f"{key_prefix}-back"):
            nav_to("welcome")

    # 3) Show roles already taken
    roles_taken = [p["participant_role"] for p in parts]
    st.subheader("Roles Already Taken")

    if st.button("🔄 Refresh", key=f"{key_prefix}-refresh"):
        st.rerun()
        
    if roles_taken:
        for r in roles_taken:
            st.write(f"- **{r}**")
    else:
        st.write("_None yet_")

    # 4) Have I already claimed one?
    me = st.session_state.user.id
    me_row = next((p for p in parts if p["id_profile"] == me), None)
    if me_row:
        st.success(f"✅ You are already **{me_row['participant_role']}** in this simulation.")
        st.session_state.participant_id = me_row["id"]
        # only enable “Start” once all 8 are in
        if len(roles_taken) == 8 and st.button("▶️ Start Simulation", key=f"{key_prefix}-start"):
            st.session_state.dm_stage = 0
            st.session_state.dm_finished = False
            nav_to("dm_questionnaire")
        else:
            st.info(f"Waiting for all roles ({len(roles_taken)}/8 claimed)…")
        return

    # 5) Otherwise show the “pick a role” form
    st.markdown("---")
    st.subheader("Select Your Role")
    all_roles = list(questionnaire1.roles.keys())
    available = [r for r in all_roles if r not in roles_taken]
    choice = st.selectbox("Choose your role", options=available, key=f"{key_prefix}-role_choice")

    # 6) Show its description immediately
    st.write(questionnaire1.roles.get(choice, "_No description available._"))

    if st.button("Submit Role", key=f"{key_prefix}-submit_role"):
        # a) Insert this participant row
        try:
            ins = supabase.from_("participant") \
                          .insert({
                              "id_simulation":    sim_id,
                              "participant_role": choice,
                              "id_profile":       me
                          }) \
                          .execute()
            pid = ins.data[0]["id"]
            st.session_state.participant_id = pid
            st.session_state.dm_role = choice 
        except Exception as e:
            st.error(f"❌ Could not register you as a participant: {e}")
            return

        # b) Append locally and update the simulation
        new_roles = roles_taken + [choice]
        try:
            up = supabase.from_("simulation") \
                         .update({"roles_logged": new_roles}) \
                         .eq("id", sim_id) \
                         .execute()
            if not up.data:
                raise RuntimeError("no data returned")
        except Exception as e:
            st.error(f"❌ Could not update simulation roles: {e}")
            return

        st.success(f"✅ You claimed **{choice}**!")
        st.rerun()  # now we hit the “already claimed” branch next

    # 7) Fallback “waiting” UI if they somehow fall through
    if len(roles_taken) == 8:
        st.markdown("---")
        if st.button("▶️ Start Simulation", key=f"{key_prefix}-fallback_start"):
            st.session_state.dm_stage = 0
            st.session_state.dm_finished = False
            nav_to("dm_questionnaire")
    else:
        st.info(f"Waiting for all roles ({len(roles_taken)}/8 claimed)…")

# ------------------------------------------------------- Page 4 Participant ----------------------------------------------------------

def page_dm_questionnaire(key_prefix: str = ""):
    sim_id  = st.session_state.simulation_id   # BIGINT PK of simulation
    part_id = st.session_state.participant_id  # BIGINT PK of this participant

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
            supabase.from_("simulation") \
                .update({"status":"running", "started_at": "now()"}) \
                .eq("id", sim_id) \
                .execute()
        except Exception as e:
            st.error(f"❌ Couldn’t mark simulation as running: {e}")
            return

        # 1b) Update this participant
        try:
            supabase.from_("participant") \
                .update({"started_at": "now()"}) \
                .eq("id", part_id) \
                .execute()
        except Exception as e:
            st.error(f"❌ Couldn’t mark participant as started: {e}")
            return

        st.session_state.dm_started_marker = True

    # —————————————————————
    # 2) Run the questionnaire engine
    # —————————————————————

    # ────────── Resume logic ─────────

    questionnaire1.run(
        supabase, simulation_name=st.session_state.simulation_name,
        role=st.session_state.dm_role
    )

    st.session_state.roles = [
      "FE-3 (EVA2)", "Commander (CMO, IV2)", "FE-1 (EVA1)", "FE-2 (IV1)",
      "FD", "FS", "BME", "CAPCOM",
    ]

    if st.session_state.dm_stage == 13 and st.button("Submit and Continue", key=f"{key_prefix}-submit_continue"):
        # 1) mark this participant finished
        now = datetime.utcnow().isoformat()
        try:
            supabase \
            .from_("participant") \
            .update({"finished_at": now}) \
            .eq("id", part_id) \
            .execute()
        except Exception as e:
            st.error(f"❌ Couldn’t record participant finish time: {e}")
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

def render_participant_live(pid: int, sim_id: int):
    # Fetch role & simulation status
    row = questionnaire1.supabase.from_("participant").select("participant_role") \
                .eq("id", pid).single().execute().data
    role = row["participant_role"]
    st.markdown(f"#### {role} — Participant #{pid}")

    status = questionnaire1.supabase.from_("simulation").select("status") \
                .eq("id", sim_id).single().execute().data["status"]
    if status != "running":
        st.write("⏳ Waiting for simulation to start…")
        return

    # Resolve blocks based on prior special decisions
    ans7  = st.session_state.answers.get("Decision 7")
    ans13 = st.session_state.answers.get("Decision 13")
    ans23 = st.session_state.answers.get("Decision 23")
    ans34 = st.session_state.answers.get("Decision 34")

    block1 = decisions1to13
    block2 = decisions14to23.get((ans7, ans13), [])
    block3 = decisions24to28.get((ans7, ans13), [])
    block4 = decisions29to32.get((ans7, ans13), [])
    block5 = decisions33to34.get((ans7, ans13, ans23), [])
    block6 = decisions35to43.get((ans7, ans13, ans23, ans34), [])

    all_questions = [*block1, *block2, *block3, *block4, *block5, *block6]

    # Initialize session state on first run
    if "all_questions" not in st.session_state:
        st.session_state.all_questions = all_questions
        st.session_state.current_decision_index = 1

    # Select current decision
    decision = st.session_state.all_questions[st.session_state.current_decision_index - 1]

    # -- Inline display logic replacing separate display_decision() --
    inject = decision.get("inject", "")
    # Determine text and options, including role-specific overrides
    text = decision.get("text", "")
    options = decision.get("options", [])
    role_specific = decision.get("role_specific", {})
    if role in role_specific:
        rs = role_specific[role]
        text = rs.get("text", text)
        options = rs.get("options", options)

    # Render prompt
    st.subheader(f"{inject}  {text}")

    # Special handling for key FD decisions
    key_decisions = ("Decision 7", "Decision 13", "Decision 23", "Decision 34")
    if inject in key_decisions:
        # Flight Director gets input; others wait
        if role == "FD":
            answer = st.radio("Your choice:", options, key=f"dec_{inject}")
            if st.button("Submit ➡", key=f"submit_{inject}"):
                # (record answer logic here)
                st.session_state.answers[inject] = answer
                st.session_state.current_decision_index += 1
                st.rerun()
        else:
            st.info("⏳ Waiting for Flight Director’s decision…")
        return

    # Standard decision rendering
    if options:
        choice_key = f"dec_{inject}"
        answer = st.radio("Select an option:", ["--"] + options, key=choice_key)
        if answer != "--" and st.button("Submit ➡", key=f"submit_{inject}"):
            # (record answer logic here)
            st.session_state.answers[inject] = answer
            st.session_state.current_decision_index += 1
            st.rerun()
    else:
        # Inject or informational step
        idx = st.session_state.current_decision_index
        button_key = f"next_{pid}_{idx}"
        if st.button("Next ➡", key=button_key):
            st.session_state.current_decision_index += 1
            st.rerun()


def render_participant_live(pid: int, sim_id: int):
    
    try:
        fd_row = (
        supabase
            .from_("participant")
            .select("id")
            .eq("id_simulation", sim_id)
            .eq("participant_role", "FD")
            .execute()
        )
        fd_rows = fd_row.data or []
        fd_id = fd_rows[0]["id"] if fd_rows else None
    except Exception as e:
        st.warning(f"⚠️ Could not find Flight Director in simulation: {e}")
        return

    # —————————————————————————————————————
    # Helper: fetch FD’s answer by prefixing inject_name
    # —————————————————————————————————————
    def _get_fd_answer(inject_name: str) -> str | None:
            """
            Returns the Flight Director's answer_text for the inject
            whose text _starts with_ inject_name, or None if not yet answered.
            """
            try:
                resp = (
                    supabase
                    .from_("answers")
                    .select("answer_text")
                    .eq("id_simulation", sim_id)
                    .eq("id_participant", fd_id)
                    .like("inject", f"{inject_name}%")   # prefix search
                    .execute()
                )
            except Exception as e:
                st.error(f"❌ Could not fetch FD’s answer for {inject_name}: {e}")
                return None

            rows = resp.data or []
            if not rows:
                # simply not answered yet
                return None

            # if for some reason there are multiple, we just pick the first
            return rows[0]["answer_text"]

    # —————————————————————————————————————
    # 1) Grab the FD’s decisions (with fallback to None)
    # —————————————————————————————————————
    try:
        ans7  = _get_fd_answer("Decision 7")
        ans13 = _get_fd_answer("Decision 13")
        ans23 = _get_fd_answer("Decision 23")
        ans34 = _get_fd_answer("Decision 34")
        # Optionally mirror into session_state for downstream code
        st.session_state.answers["Decision 7"]  = ans7
        st.session_state.answers["Decision 13"] = ans13
        st.session_state.answers["Decision 23"] = ans23
        st.session_state.answers["Decision 34"] = ans34
    except Exception as e:
        st.error(f"❌ Error initializing FD’s decision answers: {e}")
        return

    # 3) pick each block using .get()
    block1 = decisions1to13            # always the same
    block2 = decisions14to23.get((ans7, ans13), [])
    block3 = decisions24to28.get((ans7, ans13), [])
    block4 = decisions29to32.get((ans7, ans13), [])
    block5 = decisions33to34.get((ans7, ans13, ans23), [])
    block6 = decisions35to43.get((ans7, ans13, ans23, ans34), [])

    all_blocks = [block1, block2, block3, block4, block5, block6]
    all_questions = [q for block in all_blocks for q in block]

    key_decisions = ("Decision 7", "Decision 13", "Decision 23", "Decision 34")
    try:
        row = (
            supabase
            .from_("participant")
            .select("participant_role")
            .eq("id", pid)
            .single()
            .execute()
        ).data
        role = row["participant_role"]
    except Exception as e:
        st.error(f"❌ Couldn’t load participant #{pid}: {e}")
        return

    st.markdown(f"#### {role} — Participant #{pid}")

    # —————————————————————————————————————
    # 2) Fetch simulation status
    # —————————————————————————————————————
    try:
        sim = (
            supabase
            .from_("simulation")
            .select("status")
            .eq("id", sim_id)
            .single()
            .execute()
        ).data
        sim_status = sim["status"]
    except Exception as e:
        st.error(f"❌ Couldn’t load simulation #{sim_id}: {e}")
        return

    # —————————————————————————————————————
    # 3) Load all answers by this participant
    # —————————————————————————————————————
    try:
        resp = (
            supabase
            .from_("answers")
            .select("inject,answer_text")
            .eq("id_simulation", sim_id)
            .eq("id_participant", pid)
            .execute()
        )
        answered = resp.data or []
    except Exception as e:
        st.error(f"❌ Could not load answers for participant #{pid}: {e}")
        return

    answered_set = {r["inject"] for r in answered}
    answered_map = {r["inject"]: r["answer_text"] for r in answered}

    # —————————————————————————————————————
    # 4) Define your full ordered workflow
    # —————————————————————————————————————
    all_blocks = [block1, block2, block3, block4, block5, block6]
    all_steps = [d["inject"] for block in all_blocks for d in block]

    # —————————————————————————————————————
    # 5) Decide which step we should be showing
    # —————————————————————————————————————

    all_steps = []

    #  1️⃣ Inject 1
    all_steps.append("Inject 1")

    #  2️⃣ Decisions 1–13
    all_steps += [d["inject"] for d in block1]

    #  3️⃣ Inject 2
    all_steps.append("Inject 2")

    #  4️⃣ Decisions 14–23
    # assume block2 is List[ dict ]  where each dict has an "inject" key
    all_steps.extend(q["inject"] for q in block2)

    #  5️⃣ Inject 3
    all_steps.append("Inject 3")

    #  6️⃣ Decisions 24–28
    # assume block2 is List[ dict ]  where each dict has an "inject" key
    all_steps.extend(q["inject"] for q in block3)


    #  7️⃣ Inject 4
    all_steps.append("Inject 4")

    #  8️⃣ Decisions 29–32
    # assume block2 is List[ dict ]  where each dict has an "inject" key
    all_steps.extend(q["inject"] for q in block4)


    #  9️⃣ Decisions 33–34
    # assume block2 is List[ dict ]  where each dict has an "inject" key
    all_steps.extend(q["inject"] for q in block5)


    # 🔟 Decisions 35–43
    # assume block2 is List[ dict ]  where each dict has an "inject" key
    all_steps.extend(q["inject"] for q in block6)

    
    def count_for(step):
            q = (
                supabase
                .from_("answers")
                .select("id", count="exact")
                .eq("id_simulation", sim_id)
                .eq("inject", step)
            )
            if step.startswith("Inject"):
                q = q.eq("answer_text", "DONE")
            else:
                q = q.neq("answer_text", "SKIP")
            return q.execute().count or 0
    

    try:
        total = (
                supabase
                .from_("answers")
                .select("id", count="exact")
                .eq("id_simulation", sim_id)
                .execute()
        ).count or 0
    except Exception:
        total = 0
    
    if sim_status != "running":
        st.write("⏳ Waiting for participants to start…")
        return
    
    if total == 0:
        current = "Initial Situation"
    else:
        current = "Finished"
        for step in all_steps:
            cnt = count_for(step)
            q = (
                supabase
                .from_("answers")
                .select("id", count="exact")
                .eq("id_simulation", sim_id)
                .eq("inject", step)
            )
            # for injects we only count “DONE”
            if step.startswith("Inject"):
                q = q.eq("answer_text", "DONE")
            # for decisions we count anything that isn’t “SKIP”
            else:
                q = q.neq("answer_text", "SKIP")

            needed = 1 if any(step.startswith(k) for k in key_decisions) else 8
            if cnt < needed:
                current = step
                break

    st.markdown(f"**Current stage:** {current}")


    if current == "Initial Situation":
        questionnaire1.show_initial_situation()
        return

    if current == "Finished":
        st.success("✅ Completed all steps!")
        return

    # helper to pull text & options for any inject/decision
    def lookup(step_id):
        txt, opts = "_No prompt found_", []
        for block in all_blocks:
            for d in block:
                if d["inject"] == step_id:
                    # generic
                    txt = d.get("text", "")
                    opts = d.get("options", [])
                    rs = d.get("role_specific", {})
                    if role in rs:
                        txt = rs[role].get("text", txt)
                        opts = rs[role].get("options", opts)
                    return txt, opts
        return txt, opts

    try:
        q = supabase.from_("answers").select("id", count="exact") \
                .eq("id_simulation", sim_id) \
                .eq("inject", current)
        # filter according to inject vs decision
        if current.startswith("Inject"):
            q = q.eq("answer_text", "DONE")
        else:
            q = q.neq("answer_text", "SKIP")
        cnt = q.execute().count or 0
    except Exception:
        cnt = 0
    
    if current in key_decisions:
        # 1) Load FD’s answer (if any)
        try:
            fd_row = (
                supabase
                .from_("participant")
                .select("id")
                .eq("id_simulation", sim_id)
                .eq("participant_role", "FD")
                .single()
                .execute()
            ).data
            fd_id = fd_row["id"]
        except Exception as e:
            st.warning("⚠️ Flight Director not yet in simulation…")
            return

        try:
            ans = (
                supabase
                .from_("answers")
                .select("answer_text")
                .eq("id_simulation", sim_id)
                .eq("id_participant", fd_id)
                .eq("inject", current)
                .single()
                .execute()
            ).data
            fd_answer = ans["answer_text"] if ans else None
        except Exception:
            fd_answer = None

        # 2a) FD’s own panel → they get the normal question + submit status
        if role == "FD":
            prompt, options = lookup(current)
            st.markdown(f"### {current}")
            st.write(prompt)
            for o in options:
                st.write(f"- {o}")

            if fd_answer is None:
                st.info("⏳ You (FD) have not yet submitted this decision.")
            else:
                st.markdown(f"**Your answer:** {fd_answer}")
                st.info("Waiting for the rest of the simulation to proceed…")
        # 2b) Everyone else → read-only “Waiting for FD”
        else:
            st.markdown(f"### {current}")
            st.write("⏳ Waiting for Flight Director’s decision…")
            if fd_answer:
                st.success(f"FD chose: **{fd_answer}**")
        return
    
    prompt, options = lookup(current)

    if current.startswith("Inject"):
        # — Inject UI (read-only) —
        prompt1 = get_inject_text(current)
        st.write(prompt1)
        if answered_map.get(current) == "DONE":
            st.info(f"Waiting for all roles to advance past {current}… ({cnt}/8)")
        else:
            st.warning(f"⏳ Participant hasn’t clicked Next on {current} yet.")

    else:
        # — Decision UI (read-only) —
        st.write(prompt)
        for o in options:
            st.write(f"- {o}")
        if current in answered_map:
            st.markdown(f"**Your answer:** {answered_map[current]}")
            if cnt < 8:
                st.info(f"Waiting for everyone… ({cnt}/8)")
            else:
                st.success("✅ All participants answered—advancing to next step.")
        else:
            st.info("⏳ Participant has not answered this decision yet.")

    # —————————————————————————————————————
    # 7) Once all 8 are in, rerun to advance everybody
    # —————————————————————————————————————
    if sim_status == "running" and cnt == 8:
        st.rerun() 



    

def page_live_dashboard():
    #from streamlit_autorefresh import st_autorefresh
    st.header("Supervisor Live Dashboard")
    sim_id   = st.session_state.simulation_id
    sim_name = st.session_state.simulation_name
    st.subheader(f"Simulation: {sim_name}")

    if st.button("Go back to the Main Menu"):
        nav_to("welcome")
        return
    
    if st.button("Go back"):
        nav_to("menu_iniciar_simulação_supervisor")
        return
    
    if st.button("Refresh Dashboard", key="refresh"):
        st.rerun()

    # 1) Fetch the static roster from 'participant'
    #st_autorefresh(interval=5_000, key="dashboard_autorefresh")
    try:
        p_res = (
            supabase
            .from_("participant")
            .select("participant_role,id")
            .eq("id_simulation", sim_id)
            .execute()
        )
        roster = {r["participant_role"]: r["id"] for r in (p_res.data or [])}
    except Exception as e:
        st.error(f"❌ Could not load roster: {e}")
        return

    expected = [
      "FE-3 (EVA2)", "Commander (CMO, IV2)", "FE-1 (EVA1)", "FE-2 (IV1)",
      "FD", "FS", "BME", "CAPCOM",
    ]

    for row in [expected[:4], expected[4:]]:
        cols = st.columns(4, gap="small")
        for role, col in zip(row, cols):
            with col:
                #st.subheader(role)
                pid = roster.get(role)
                if not pid:
                    st.write("_Not yet joined_")
                else:
                    render_participant_live(pid, sim_id)

    if st.button("Go to Teamwork Assessment"):
        nav_to("teamwork_survey")

def page_override_interface():
    st.header("Supervisor Override")

    # 1) Who are we overriding for?
    pid = st.session_state.get("override_for")
    if not pid:
        st.error("No participant selected for override.")
        return
    sim_id = st.session_state.simulation_id

    # 2) Lookup that participant’s role so we can show it
    p_res = (
        supabase
        .from_("participant")
        .select("participant_role")
        .eq("id", pid)
        .single()
        .execute()
    )
    if p_res.error:
        st.error(f"Couldn't load participant: {p_res.error.message}")
        return
    role = p_res.data["participant_role"]
    st.subheader(f"Override for: {role}")

    # 3) Let supervisor pick _which_ inject to override.
    #    We’ll pull the full list of injects from your question bank.
    injects = [d["inject"] for d in questionnaire1.decisions1to13] \
             + [i for block in questionnaire1.decisions14to23.values() for i in [d["inject"] for d in block]] \
             + [i for block in questionnaire1.decisions24to28.values() for i in [d["inject"] for d in block]] \
             + [i for block in questionnaire1.decisions29to32.values() for i in [d["inject"] for d in block]] \
             + [i for block in questionnaire1.decisions33to34.values() for i in [d["inject"] for d in block]] \
             + [i for block in questionnaire1.decisions35to43.values() for i in [d["inject"] for d in block]]
    inject = st.selectbox("Select Inject to override", sorted(set(injects)))

    # 4) Enter the “new” answer
    answer = st.text_input("Override answer")

    if st.button("Submit Override"):
        payload = {
            "id_simulation":   sim_id,
            "id_participant":  pid,
            "inject":          inject,
            "question_text":   "",            # or fill from session_state.question_text_map[inject]
            "answer_text":     answer,
            "score":           0,             # you can recompute if you like
            "response_time":   None
        }
        resp = supabase.from_("answers").upsert([payload]).execute()
        if resp.error:
            st.error(f"❌ Override failed: {resp.error.message}")
        else:
            st.success(f"Override applied: {role} → {inject} = “{answer}”")
            # clear override flag & go back
            del st.session_state.override_for
            nav_to("live_dashboard")



# -------------------------------------------- 
def page_dashboard():

    sim = st.session_state.simulation_name
    if st.button("Back"):
        nav_to("menu_iniciar_simulação_supervisor")


    try:
        resp = (
            supabase
            .from_("answers")
            .select("inject, answer_text")
            .eq("simulation_name", sim)
            .in_("participant_role", ["FD", "FS"])
            .execute()
        )
        rows = resp.data
    except Exception as e:
        st.error(f"❌ Error fetching quiz results: {e}")
        return

    answers = st.session_state.setdefault("answers", {})
    for row in rows:
        inj = row["inject"]
        ans = row["answer_text"]
        answers.setdefault(inj, []).append(ans)
    # ─── 2) Recalcula os EFFECTS com base nessas answers ───
    apply_vital_consequences(answers)

    # ─── 3) Agora chama o run(), que vai ler de st.session_state["vital_effects"] ───
    data_simulation.run(sim)

    # **Interrompe aqui**, nada mais deve desenhar nesta página
    st.markdown("---")
    if st.session_state.teamwork_submitted:
        # once the supervisor has done their form, let anyone jump to team_results
        if st.button("🏆 View Team Results"):
            nav_to('team_results')
    else:
        st.info("🔒 Team Results will become available after the supervisor submits the teamwork assessment.")
    
    return
    

def page_teamwork_survey():
    teamwork.run(simulation_name=st.session_state.simulation_name)

    if st.session_state.teamwork_submitted:
        st.success("✅ Supervisor scores saved.")
        nav_to('certify_and_results')
    #     sim    = st.session_state.simulation_name
    #     supv   = st.session_state.supervisor               # the supervisor’s identifier
    #     comments = st.session_state.get("teamwork_feedback_text", "")
    #     scores   = st.session_state.get("teamwork_scores", {})

    #     # Build the payload matching your `supervisor` table columns
    #     payload = {
    #         "simulation_name": sim,
    #         "leadership":            scores.get("Leadership"),
    #         "teamwork":              scores.get("Teamwork"),
    #         "task_management":       scores.get("Task_Management"),
    #         "overall":               scores.get("Overall"),
    #         "total_teamwork":        scores.get("Total_Teamwork"),
    #         "comments":              comments,
    #         "situation_awareness_comments": scores.get("Situation_Awareness_Comments")
    #     }
    #     # Insert into Supabase
    #     try:
    #         supabase.from_("supervisor").insert(payload).execute()
    #     except Exception as e:
    #         st.error(f"❌ Failed to save supervisor scores: {e}")
    #     else:

    if st.button("Back"):
        nav_to("menu_iniciar_simulação_supervisor")

def page_certify_and_results():
    st.header("Certification & Combined Results")
    st.write("Make sure the simulation ran and the teamwork form is complete.")

    # 1) Has the supervisor actually submitted the TEAM form?
    if not st.session_state.get("teamwork_submitted", False):
        st.warning("Teamwork form not submitted yet.")
        return

    # 2) Is the simulation already marked 'finished' in Supabase?
    sim = (
        supabase
        .from_("simulation")
        .select("status")
        .eq("id", st.session_state.simulation_id)
        .maybe_single()
        .execute()
    )
    if not sim.data or sim.data.get("status") != "finished":
        st.info("Waiting for the system to mark this simulation as finished.")
        return

    # 3) Now that both are true, show the certify button
    if st.button("✅ Certify Simulation Completed and View Team Results"):
        st.session_state.teamwork=True
        nav_to("team_results")

def page_team_results():
    # 1) Guard: must have certified the simulation
    sim = (
        supabase
        .from_("simulation")
        .select("status, name")
        .eq("id", st.session_state.simulation_id)
        .maybe_single()
        .execute()
    )
    if not sim.data or sim.data.get("status") != "finished":
        st.info("Waiting for the system to mark this simulation as finished.")
        return
    
    sim_name = sim.data.get("name")
    sim_id = st.session_state.simulation_id
    st.header("🏆 Team Performance Results")
    st.subheader(f"Simulation: {sim_name}")

    # 3) Load per-role aggregates from the `individual_results` view
    try:
        ind_res = (
            supabase
            .from_("individual_results")
            .select(
                "basic_life_support, primary_survey, secondary_survey, definitive_care, "
                "crew_roles_communication, systems_procedural_knowledge"
            )
            .eq("simulation_id", sim_id)
            .execute()
        )
        ind_data = ind_res.data or []
    except Exception as e:
        st.error(f"❌ Couldn’t load decision-maker results: {e}")
        ind_data = []
    
    try:
        # 0a) find the Flight Director’s participant.id
        fd_part = (
            supabase
            .from_("participant")
            .select("id")
            .eq("id_simulation", sim_id)
            .eq("participant_role", "FD")
            .maybe_single()
            .execute()
        )
        fd_id = fd_part.data and fd_part.data.get("id")
    except Exception as e:
        st.error(f"❌ Could not load Flight Director’s ID: {e}")
        return

    if not fd_id:
        st.error("❌ Flight Director not found in this simulation.")
        return

    def fetch_fd_answer(prefix: str) -> str | None:
        """Grab the one FD answer whose inject starts with prefix."""
        try:
            ans = (
                supabase
                .from_("answers")
                .select("answer_text")
                .eq("id_simulation", sim_id)
                .eq("id_participant", fd_id)
                .like("inject", f"{prefix}%")
                .maybe_single()
                .execute()
            )
            return ans.data and ans.data.get("answer_text")
        except Exception:
            return None

    a7  = fetch_fd_answer("Decision 7")
    a13 = fetch_fd_answer("Decision 13")
    a23 = fetch_fd_answer("Decision 23")
    a34 = fetch_fd_answer("Decision 34")

    if None in (a7, a13, a23, a34):
        st.error("❌ Could not determine scenario code: missing one of FD’s key decisions.")
        return

    scenario_code = f"7({a7})&13({a13})&23({a23})&34({a34})"

    if ind_data:
        df_ind = pd.DataFrame(ind_data)
        # Sum across all roles for each category
        med_cats  = ["basic_life_support", "primary_survey", "secondary_survey", "definitive_care"]
        proc_cats = ["crew_roles_communication", "systems_procedural_knowledge"]
        med_cats_total  = ["basic_life_support_total", "primary_survey_total", "secondary_survey_total", "definitive_care_total"]
        proc_cats_total = ["crew_roles_communication_total", "systems_procedural_knowledge_total"]
        med_totals  = df_ind[med_cats].sum().to_dict()
        proc_totals = df_ind[proc_cats].sum().to_dict()
        team_actuals = {**med_totals, **proc_totals}

        # 2) fetch every max_score for this scenario
        try:
            ms = (
                supabase
                .from_("max_scores")
                .select("role,category,max_value")
                .eq("scenario_code", scenario_code)
                .execute()
            )
            ms_data = ms.data or []
        except Exception as e:
            st.error(f"❌ Couldn’t load team max_scores: {e}")
            ms_data = []

        # 3) sum per category across all roles
        df_ms = pd.DataFrame(ms_data)

        # 1) Normalize the category names to lowercase so they match med_cats/proc_cats
        if not df_ms.empty:
            df_ms["category"] = df_ms["category"].str.lower()
            team_maxes = df_ms.groupby("category")["max_value"].sum().to_dict()
        else:
            team_maxes = {}
        
        if not df_ind.empty:
            med_totals  = df_ind[med_cats].sum(axis=0).to_dict()
            proc_totals = df_ind[proc_cats].sum(axis=0).to_dict()
            team_actual_scores = {**med_totals, **proc_totals}
        else:
            team_actual_scores = {c: 0 for c in med_cats + proc_cats}

        cats = med_cats + proc_cats

        # 2) Build 3 aligned lists: Category, Your Score, Max Score
        team_actuals = {**med_totals, **proc_totals}

        rows = []
        for cat in med_cats + proc_cats:
            your = team_actuals.get(cat, 0)                   # ← use the merged dict
            mx   = team_maxes.get(f"{cat}_total", 0)          # if your max_keys ended up including "_total"
            pct  = f"{100*your/mx:0.1f}%" if mx else "—"
            rows.append([cat.replace("_"," ").title(), your, mx, pct])

        # 3) Compute subtotals and grand total
        med_actual_sum  = sum(med_totals[c] for c in med_cats)
        proc_actual_sum = sum(proc_totals[c] for c in proc_cats)
        med_max_sum     = sum(team_maxes.get(f"{c}_total", 0) for c in med_cats)
        proc_max_sum    = sum(team_maxes.get(f"{c}_total", 0) for c in proc_cats)
        grand_actual    = med_actual_sum + proc_actual_sum
        grand_max       = med_max_sum    + proc_max_sum

        rows += [
            ["Medical Knowledge",    med_actual_sum,  med_max_sum,  f"{100*med_actual_sum/med_max_sum:.1f}%" if med_max_sum else "—"],
            ["Procedural Knowledge", proc_actual_sum, proc_max_sum, f"{100*proc_actual_sum/proc_max_sum:.1f}%" if proc_max_sum else "—"],
            ["Total",                grand_actual,    grand_max,     f"{100*grand_actual/grand_max:.1f}%"    if grand_max    else "—"],
        ]

        # 4) Turn it into a DataFrame
        df_team_vs_max = pd.DataFrame(
            rows,
            columns=["Category", "Team Score", "Max Score", "% of Maximum"]
        )
        
        st.dataframe(df_team_vs_max)
    else:
        st.info("No decision-maker aggregate found for this simulation.")
        return  # nothing more to plot
    
    # 2) Load the supervisor’s TEAM assessment from the `teamwork` table
    try:
        tw_res = (
            supabase
            .from_("teamwork")
            .select(
                "id, id_simulation, leadership, teamwork, task_management, "
                "overall_performance, total, comments, created_at"
            )
            .eq("id_simulation", sim_id)
            .execute()
        )
        tw_data = tw_res.data or []
    except Exception as e:
        st.error(f"❌ Couldn’t load teamwork assessment: {e}")
        tw_data = []

    if tw_data:
        df_tw = pd.DataFrame(tw_data)
        st.subheader("🔹 Supervisor’s TEAM Assessment")

        # 1) Pull out the four domain scores + total
        tw_cols = ["leadership", "teamwork", "task_management", "overall_performance", "total"]
        labels  = ["Leadership", "Teamwork", "Task Mgmt", "Overall", "Total"]
        actuals = df_tw.loc[0, tw_cols].tolist()

        # 2) Define the max‐possible for each domain + grand total
        maxes = [8, 28, 8, 10, 54]

        # 3) Draw a more compact grouped bar chart
        x     = np.arange(len(labels))
        width = 0.30

        fig, ax = plt.subplots(figsize=(5, 2))  # smaller figure
        ax.bar(x - width/2, actuals, width, label="Your Score")
        ax.bar(x + width/2, maxes,   width, label="Max Possible", color="#cccccc")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylim(0, max(maxes) * 1.05)
        ax.set_ylabel("Points", fontsize=8)
        ax.set_title("TEAM Scores vs Max", fontsize=10)
        ax.legend(fontsize=8, loc="upper right")
        fig.tight_layout()

        st.pyplot(fig, use_container_width=True)
    else:
        st.info("No teamwork assessment found for this simulation.")


    # Finally, download a team report PDF if desired
    def build_team_pdf():
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        elems = [Paragraph("Team Performance Report", styles["Title"]), Spacer(1,12)]

        # 1) Table of Team vs Maximum Scores
        data = [df_team_vs_max.columns.to_list()] + df_team_vs_max.values.tolist()
        tbl = RLTable(data, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), HexColor("#4F81BD")),
            ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
            ("GRID",        (0,0), (-1,-1), 0.25, colors.grey),
            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
            ("ALIGN",      (1,1), (-1,-1), "CENTER"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1,24))

        # 2) TEAM vs Max bar chart
        # reproduce that same matplotlib figure
        tw_cols = ["leadership", "teamwork", "task_management", "overall_performance", "total"]
        labels  = ["Leadership", "Teamwork", "Task Mgmt", "Overall", "Total"]
        actuals = df_tw.loc[0, tw_cols].tolist()
        maxes   = [8, 28, 8, 10, 54]

        x     = np.arange(len(labels))
        width = 0.30
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.bar(x - width/2, actuals, width, label="Your Score")
        ax.bar(x + width/2, maxes,   width, label="Max Possible", color="#cccccc")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylim(0, max(maxes) * 1.05)
        ax.set_ylabel("Points", fontsize=8)
        ax.set_title("TEAM Scores vs Max", fontsize=10)
        ax.legend(fontsize=8, loc="upper right")
        fig.tight_layout()

        # save to buffer
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="PNG", dpi=150, bbox_inches="tight")
        img_buf.seek(0)
        elems.append(RLImage(img_buf, width=400, height=200))
        elems.append(Spacer(1,24))

        # 3) (optional) other charts…
        # for fig in (fig_med, fig_proc, fig_radar):
        #     buf_img = io.BytesIO()
        #     fig.savefig(buf_img, format="PNG", bbox_inches="tight")
        #     buf_img.seek(0)
        #     elems.append(RLImage(buf_img, width=400, height=300))
        #     elems.append(Spacer(1,12))

        doc.build(elems)
        buf.seek(0)
        return buf

    def upload_report_to_storage(bucket_name: str, path: str, pdf_buffer: io.BytesIO) -> str | None:
        """
        Uploads pdf_buffer to `bucket_name` under `path`.
        Returns the public URL (as a str), or None on failure (after st.error).
        """
        file_bytes = pdf_buffer.getvalue()
        # 1) Try the upload; StorageApiError will be raised on RLS / permissions / etc.
        try:
            supabase.storage.from_(bucket_name).upload(
                path,
                file_bytes,
                {"contentType": "application/pdf"},
            )
        except Exception as e:
            return None

        # 2) Fetch a public URL for that object
        try:
            public = supabase.storage.from_(bucket_name).get_public_url(path)
            if isinstance(public, dict):
                return public.get("publicURL") or public.get("publicUrl")
            elif isinstance(public, str):
                return public
            else:
                st.error(f"❌ Unexpected get_public_url response type: {type(public).__name__}")
                return None
        except Exception as e:
            st.error(f"❌ Uploaded, but could not fetch public URL: {e}")
            return None

    pdf_buffer = build_team_pdf()
    if pdf_buffer:
        # let users download in-browser
        st.download_button(
            "📄 Download Team Report PDF",
            data=pdf_buffer,
            file_name=f"{sim_name}_team_report.pdf",
            mime="application/pdf",
        )

        # also push it to your Supabase bucket
        report_path = f"{sim_name}/team_report.pdf"
        public_url = upload_report_to_storage("reports", report_path, pdf_buffer)

    if st.button("Go back to Main Menu"):
        nav_to("welcome")



def page_simulation_menu():
    st.header("Supervisor Dashboard")

    sim_id = st.session_state.get("simulation_id")
    if not sim_id:
        st.error("❗ No simulation selected. Please ask your supervisor to create one first.")
        return

    # 1) Show the simulation name
    st.subheader(f"Simulation: **{st.session_state.simulation_name}**")


    if st.button("▶️ Go to Vital-Signs Dashboard"):
            nav_to("dashboard")

    if st.button("▶️ Go to Supervisor Dashboard"):
        nav_to("live_dashboard")
    
    if st.button("▶️ Go to Teamwork Assessment"):
        nav_to("teamwork_survey")


def page_individual_results():

    sim_name = st.session_state.simulation_name
    dm_role  = st.session_state.dm_role
    sim_id  = st.session_state.simulation_id   # BIGINT PK of simulation
    part_id = st.session_state.participant_id 

    if not sim_name or not dm_role:
        st.error("No simulation or role selected.")
        return

    # 1) Fetch raw answers from Supabase
    try:
        # 0a) find the Flight Director’s participant.id
        fd_part = (
            supabase
            .from_("participant")
            .select("id")
            .eq("id_simulation", sim_id)
            .eq("participant_role", "FD")
            .maybe_single()
            .execute()
        )
        fd_id = fd_part.data and fd_part.data.get("id")
    except Exception as e:
        st.error(f"❌ Could not load Flight Director’s ID: {e}")
        return

    if not fd_id:
        st.error("❌ Flight Director not found in this simulation.")
        return

    def fetch_fd_answer(prefix: str) -> str | None:
        """Grab the one FD answer whose inject starts with prefix."""
        try:
            ans = (
                supabase
                .from_("answers")
                .select("answer_text")
                .eq("id_simulation", sim_id)
                .eq("id_participant", fd_id)
                .like("inject", f"{prefix}%")
                .maybe_single()
                .execute()
            )
            return ans.data and ans.data.get("answer_text")
        except Exception:
            return None

    a7  = fetch_fd_answer("Decision 7")
    a13 = fetch_fd_answer("Decision 13")
    a23 = fetch_fd_answer("Decision 23")
    a34 = fetch_fd_answer("Decision 34")

    if None in (a7, a13, a23, a34):
        st.error("❌ Could not determine scenario code: missing one of FD’s key decisions.")
        return

    scenario_code = f"7({a7})&13({a13})&23({a23})&34({a34})"
    try:
        ans_res = (
            supabase
            .from_("answers")
            .select("inject,answer_text")
            .eq("id_simulation", sim_id)
            .eq("id_participant", part_id)
            .execute()
        )
    except Exception as e:
        st.error(f"❌ Couldn’t load your answers: {e}")
        return

    # instead of `if ans_res.error:` do:
    if not getattr(ans_res, "data", None):
        st.error("❌ No answers found for you in this simulation.")
        return
    
    # 2) Fetch per-role aggregates from your view
    # Individual results
    try:
        ind_res = (
            supabase
            .from_("individual_results")
            .select("*")
            .eq("simulation_id",  sim_id)
            .eq("participant_id", part_id)
            .maybe_single()
            .execute()
        )
    except Exception as e:
        st.error(f"❌ Couldn’t load individual_results: {e}")
        return
    if not ind_res.data:
        st.error("❌ No individual_results row found.")
        return

    ind = ind_res.data
    # categories in your view
    med_cats  = ["basic_life_support", "primary_survey", "secondary_survey", "definitive_care"]
    proc_cats = ["crew_roles_communication", "systems_procedural_knowledge"]
    med_cats_total = ["basic_life_support_total", "primary_survey_total", "secondary_survey_total", "definitive_care_total"]
    proc_cats_total = ["crew_roles_communication_total", "systems_procedural_knowledge_total"]


    med_actuals  = [ float(ind[c]) for c in med_cats ]
    med_subtot   = float(ind["medical_knowledge_total"])
    proc_actuals = [ float(ind[c]) for c in proc_cats ]
    proc_subtot  = float(ind["procedural_knowledge_total"])
    actual_total = float(ind["score"])

    # Max scores
    try:
        max_res = (
            supabase
            .from_("max_scores")
            .select("category,max_value")
            .eq("role", dm_role)
            .eq("scenario_code", scenario_code)
            .execute()
        )
    except Exception as e:
        st.error(f"❌ Couldn’t load max_scores: {e}")
        return

    if not max_res.data:
        st.error(f"❌ No max_scores for role={dm_role} scenario={scenario_code}")
        return

    # lowercase the category so it matches your `med_cats` / `proc_cats`
    max_for_me = {
        r["category"].lower(): float(r["max_value"])
        for r in max_res.data
    }
    
    med_maxs     = [ max_for_me[c] for c in med_cats_total ]
    med_max_sub  = sum(med_maxs)
    proc_maxs    = [ max_for_me[c] for c in proc_cats_total ]
    proc_max_sub = sum(proc_maxs)
    max_total    = med_max_sub + proc_max_sub

    # ——— Load TLX responses for this participant ———
    try:
        tlx_res = (
            supabase
            .from_("taskload_responses")
            .select("mental,physical,temporal,performance,effort,frustration")
            .eq("id_simulation", sim_id)
            .eq("id_participant", part_id)
            .maybe_single()
            .execute()
        )
    except Exception as e:
        st.error(f"❌ Couldn’t load your TLX responses: {e}")
        return

    # If there was no row, tlx_res.data will be None
    if not getattr(tlx_res, "data", None):
        st.error("❌ No TLX responses found for you in this simulation.")
        return
    df_tlx = pd.DataFrame([tlx_res.data])

    st.header("Your Individual Results")
    st.write(f"Your scenario: {scenario_code}")


    if not sim_name:
        st.error("❗️ No simulation name found. Please go back and re-save your results.")
        return

    # … your data loading / totals / values code here …
    col_med, col_proc = st.columns(2)

    with col_med:
        st.subheader("🩺 Medical Knowledge")
        labels = med_cats + ["Subtotal"]
        your   = med_actuals + [med_subtot]
        mx     = med_maxs     + [med_max_sub]
        x = np.arange(len(labels))
        fig1, ax1 = plt.subplots(figsize=(6,4))
        w = 0.35
        ax1.bar(x - w/2, your, width=w, label="You")
        ax1.bar(x + w/2, mx,   width=w, label="Max")
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, rotation=30, ha="right")
        ax1.set_ylabel("Points")
        ax1.legend()
        st.pyplot(fig1, use_container_width=True)

    with col_proc:
        st.subheader("⚙️ Procedural Knowledge")
        labels = proc_cats + ["Subtotal"]
        your   = proc_actuals + [proc_subtot]
        mx     = proc_maxs    + [proc_max_sub]
        x = np.arange(len(labels))
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.bar(x - w/2, your, width=w, label="You",   color="#73cf73")
        ax2.bar(x + w/2, mx,   width=w, label="Max", color="#eeeeee")
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels, rotation=30, ha="right")
        ax2.set_ylabel("Points")
        ax2.legend()
        st.pyplot(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
        # [2] second row: two radar charts side by side
    with col1:
        radar_cats = med_cats + proc_cats
        vals       = med_actuals + proc_actuals
        maxs       = med_maxs    + proc_maxs
        angles     = np.linspace(0,2*np.pi,len(radar_cats),endpoint=False)
        angles     = np.concatenate([angles, angles[:1]])
        vals_wrap  = vals + [vals[0]]
        maxs_wrap  = maxs + [maxs[0]]
        st.subheader("📋 Total Skills Breakdown")

        # build the rows exactly as you did for the PDF
        table_rows = []
        # per‐category rows
        for cat, your, mx in zip(
            med_cats + proc_cats,
            med_actuals + proc_actuals,
            med_maxs    + proc_maxs
        ):
            pct = f"{100 * your / mx:0.1f}%" if mx > 0 else "—"
            table_rows.append([cat, your, mx, pct])

        # subtotals and grand‐total
        table_rows += [
            ["Medical Knowledge",     med_subtot,   med_max_sub,   f"{100*med_subtot/med_max_sub:0.1f}%"],
            ["Procedural Knowledge", proc_subtot,  proc_max_sub,  f"{100*proc_subtot/proc_max_sub:0.1f}%"],
            ["Total",         actual_total, max_total,     f"{100*actual_total/max_total:0.1f}%"],
        ]

        # turn it into a DataFrame and render
        df_tot = pd.DataFrame(
            table_rows,
            columns=["Category", "Your Score", "Max. Score", "% of the Maximum"]
        )

        # you can use st.table for a static, nicely‐formatted view:
        st.table(df_tot)

    with col2:
        tlx_cols = ["mental","physical","temporal","performance","effort","frustration"]
        tlx_vals = df_tlx.loc[0, tlx_cols].tolist()
        angles2  = np.linspace(0,2*np.pi,len(tlx_cols),endpoint=False)
        angles2  = np.concatenate([angles2, angles2[:1]])
        vals2    = tlx_vals + [tlx_vals[0]]
        st.subheader("💼 Taskload Radar")
        fig4, ax4 = plt.subplots(subplot_kw={"polar":True}, figsize=(6,6))
        ax4.plot(angles2, vals2, linewidth=2)
        ax4.fill(angles2, vals2, alpha=0.25)
        ax4.set_xticks(angles2[:-1])
        ax4.set_xticklabels(
            ["Mental","Physical","Temporal","Performance","Effort","Frustration"],
            fontsize=10
        )
        ax4.set_ylim(0, max(vals2)*1.1)
        st.pyplot(fig4, use_container_width=True)

    st.subheader("🔹 Your Answers")

    try:
        raw = (
            supabase
            .from_("answers")
            .select(
                "inject, answer_text, "
                "basic_life_support, primary_survey, secondary_survey, definitive_care, "
                "crew_roles_communication, systems_procedural_knowledge, response_time"
            )
            .eq("id_simulation", sim_id)
            .eq("id_participant", part_id)
            .execute()
            .data
        ) or []
    except Exception as e:
        st.error(f"❌ Couldn’t load raw answers: {e}")
        raw = []

    df_raw = pd.DataFrame(raw)

    if df_raw.empty:
        st.info("No answers to display yet.")
    else:
        order = list(st.session_state.question_text_map.keys())
        df_raw["_order"] = df_raw["inject"].map(
            lambda inj: order.index(inj) if inj in order else 999
        )

        # filter out initial situation and all inject steps
        df_raw = df_raw[
            ~df_raw["inject"].str.startswith("Inject")
            & (df_raw["inject"] != "Initial Situation")
        ]

        df_raw = df_raw.sort_values("_order").drop(columns=["_order"])
        st.dataframe(df_raw)

    def build_pdf():
        buffer = io.BytesIO()
        doc    = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elems  = []

        elems.append(Paragraph(f"Individual Report — {dm_role, sim_name}", styles["Title"]))
        elems.append(Spacer(1,12))

        # build table data
        data = [["Category","Your Score","Max Score","% of the maximum"]]
        for cat in med_cats + proc_cats:
            your = float(ind[cat])
            mx   = max_for_me.get(cat + "_total", 0.0)
            pct  = f"{100*your/mx:.1f}%" if mx>0 else "—"
            data.append([cat, f"{your:.1f}", f"{mx:.1f}", pct])

        # then your subtotals:
        data.append([
            "Medical Knowledge",
            f"{med_subtot:.1f}",
            f"{med_max_sub:.1f}",
            f"{100 * med_subtot/med_max_sub:.1f}%"
        ])
        data.append([
            "Procedural Knowledge",
            f"{proc_subtot:.1f}",
            f"{proc_max_sub:.1f}",
            f"{100 * proc_subtot/proc_max_sub:.1f}%"
        ])
        data.append([
            "Total",
            f"{actual_total:.1f}",
            f"{max_total:.1f}",
            f"{100 * actual_total/max_total:.1f}%"
        ])

        tbl = Table(data, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),HexColor("#4F81BD")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),0.25,colors.grey),
            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),
            ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1,24))

        # now embed the four figs
        for fig in (fig1, fig2, fig4):
            img_buf = io.BytesIO()
            fig.savefig(img_buf, format="PNG", dpi=150, bbox_inches="tight")
            img_buf.seek(0)
            elems.append(Image(img_buf, width=400, height=300))
            elems.append(Spacer(1,12))

        doc.build(elems)
        buffer.seek(0)
        return buffer
    
    def upload_report_to_storage(bucket_name: str, path: str, pdf_buffer: io.BytesIO) -> str | None:
        """
        Uploads pdf_buffer to `bucket_name` under `path`.
        Returns the public URL (as a str), or None on failure (after st.error).
        """
        file_bytes = pdf_buffer.getvalue()
        # 1) Try the upload; StorageApiError will be raised on RLS / permissions / etc.
        try:
            supabase.storage.from_(bucket_name).upload(
                path,
                file_bytes,
                {"contentType": "application/pdf"},
            )
        except Exception as e:
            return None

        # 2) Fetch a public URL for that object
        try:
            public = supabase.storage.from_(bucket_name).get_public_url(path)
            # some versions return a dict, some a bare str
            if isinstance(public, dict):
                # try both common keys
                return public.get("publicURL") or public.get("publicUrl")
            elif isinstance(public, str):
                return public
            else:
                st.error(f"❌ Unexpected get_public_url response type: {type(public).__name__}")
                return None

        except Exception as e:
            st.error(f"❌ Uploaded, but could not fetch public URL: {e}")
            return None




    pdf_buffer = build_pdf()
    if pdf_buffer:
        st.download_button(
            "📄 Download report PDF",
            data=pdf_buffer,
            file_name=f"{dm_role.replace(' ','_')}_report.pdf",
            mime="application/pdf",
        )
        report_path = f"{st.session_state.simulation_name}/{dm_role.replace(' ','_')}_report.pdf"
        public_url = upload_report_to_storage("reports", report_path, pdf_buffer)

    if st.button("Go back to Main Menu"):
        nav_to("welcome")


def page_running_simulations():
    st.header("🏃 Ongoing Simulations")
    if st.button("Go back to the Main Menu"):
        nav_to("welcome")
        return

    # 1) Fetch running sims
    try:
        resp = (
            supabase
            .from_("simulation")
            .select("id, name, started_at, roles_logged")
            .eq("status", "running")
            .order("started_at", desc=True)
            .execute()
        )
        sims = resp.data or []
    except Exception as e:
        st.error(f"❌ Could not load ongoing simulations: {e}")
        return

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
        started = pd.to_datetime(sim["started_at"]).strftime("%Y-%m-%d %H:%M:%S")
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

                # 3) Rebuild each block based on those conds
                b1 = decisions1to13
                b2 = decisions14to23.get(cond1, [])
                b3 = decisions24to28.get(cond1, [])
                b4 = decisions29to32.get(cond1, [])
                b5 = decisions33to34.get(cond2, [])
                b6 = decisions35to43.get(cond3, [])

                if not all(cond1):
                    # still in the first 13 decisions
                    flat_questions = b1
                    inject_marker  = "Initial Situation" if not any(cond1) else "Inject 1"

                elif cond1 and not cond2[2]:
                    # answered 7+13, but not 23
                    flat_questions = b2
                    inject_marker  = "Inject 2"

                elif cond2 and not cond3[3]:
                    # answered 7,13,23 but not 34
                    flat_questions = b3 + b4 + b5
                    inject_marker  = "Inject 3"

                else:
                    # all four FD decisions done
                    flat_questions = b6
                    inject_marker  = "Inject 4"

                all_steps = []
                if inject_marker:
                    all_steps.append(inject_marker)
                all_steps += [q["inject"] for q in flat_questions]


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
                answered_raw = [r["inject"] for r in ans_resp.data or []]
                answered = { normalize(a) for a in answered_raw }

                # also mark off FD-only decisions that FD has already made
                fd_keys = ("Decision 7", "Decision 13", "Decision 23", "Decision 34")
                for fd_pref in fd_keys:
                    if get_role_decision_answer(fd_pref, "FD") is not None:
                        answered.add(fd_pref)

                # 4) now walk the _normalized_ all_steps and land on the first prefix they haven’t done
                norms = [ normalize(s) for s in all_steps ]
                # st.write("DEBUG norms(all_steps):", norms)
                
                # after flat_questions…
                scenario_prefixes = {
                    normalize(d["inject"])
                    for d in flat_questions
                }

                inspect = []
                for step in all_steps:
                    pref = normalize(step)
                    inspect.append({
                        "step": step,
                        "pref": pref,
                        "answered?": pref in answered,
                        "in scenario?": (not pref.startswith("Decision")) or (pref in scenario_prefixes)
                    })
                st.write("DEBUG step inspection:", inspect)
                
                next_step = None
                for step in all_steps:
                    if normalize(step) not in answered:
                        next_step = step
                        break

                if next_step is None:
                    dm_stage, current_decision_index = 12, None

                elif next_step.startswith("Inject"):
                    # e.g. "Inject 2" → stage 3
                    dm_stage = int(next_step.split()[1]) + 1
                    current_decision_index = None

                else:
                    # find the question *within* flat_questions
                    for rel_idx, q in enumerate(flat_questions):
                        if normalize(q["inject"]) == normalize(next_step):
                            break
                    else:
                        st.error(f"⚠️ Couldn't locate {next_step!r} in flat_questions")
                        return

                    # now pick your stage by which flat_questions you built
                    if flat_questions is b1:
                        dm_stage, current_decision_index = 2, rel_idx +1
                    elif flat_questions is b2:
                        dm_stage, current_decision_index = 4, rel_idx + 1

                    elif flat_questions is (b3 + b4 + b5):
                        # if you want a finer split you can check rel_idx here
                        dm_stage, current_decision_index = 6, rel_idx +1
                    else:  # flat_questions is b6
                        dm_stage, current_decision_index = 12, rel_idx +1

                # 6) stash and navigate
                # sanity check:
                # sanity check
                if not flat_questions or not isinstance(flat_questions[0], dict):
                    st.error("⚠️ `all_questions` must be a list of dicts but isn’t – please check your decision blocks.")
                    return
                
                # st.write("DEBUG block lengths:", {
                # "b1": len(b1), "b2": len(b2), "b3": len(b3),
                # "b4": len(b4), "b5": len(b5), "b6": len(b6),
                # })
                # st.write("DEBUG decisions33to34 keys:", list(decisions33to34.keys()))
                # st.write("DEBUG decisions35to43 keys:", list(decisions35to43.keys()))
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
                # st.write("DEBUG flat_questions", flat_questions)
                # st.write ("DEBUG b2",b2)


                st.session_state.all_questions          = flat_questions
                st.session_state.current_decision_index = current_decision_index
                st.session_state.dm_stage               = dm_stage
                # st.write("🔍 debugging all_questions:", st.session_state.all_questions[:5])
                # idx = st.session_state.current_decision_index
                # st.write("🔍 debug current_decision_index:", idx)
                # if idx is not None:
                #     q = st.session_state.all_questions[idx]
                #     st.write("🔍 debug question:", q["inject"])
                # else:
                #     st.write("🔍 currently at an inject, no question index to show")

                nav_to("dm_questionnaire")
                return

            st.error("Only supervisors or participants can join a running simulation.")
            return




def page_past_simulations():
    st.header("📜 Past Simulations")
    # Fetch all simulations whose status is “finished”
    
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




