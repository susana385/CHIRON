# chiron_control_center.py
import streamlit as st
import data_simulation          # your wrapper now exposes run(simulation_name)
import teamwork                 # sets st.session_state['teamwork_submitted']=True
import questionnaire1           # sets st.session_state['dm_finished']=True
import os, json
import sqlite3
import generate_sql
import pandas as pd 
from questionnaire1 import compute_team_breakdown


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

st.set_page_config(
    page_title="CHIRON Control Center",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def nav_to(page_name: str):
    """Helper: set the app’s current page in session_state and rerun."""
    st.session_state.page = page_name
    st.rerun()

def init_state():
    """Initialize persistent bits once per session."""
    st.session_state.setdefault('simulation_certified', False)
    st.session_state.setdefault('role', None)
    st.session_state.setdefault('simulation_name', '')
    st.session_state.setdefault('teamwork_submitted', False)
    st.session_state.setdefault('dm_finished', False)
    # our replacement for query-params
    st.session_state.setdefault('page', 'welcome')
    # make sure our questionnaire has somewhere to stash answers
    st.session_state.setdefault('answers', {})
    st.session_state.setdefault('roles', [])
    st.session_state.setdefault('tlx_answers', {})

#
# ——— Page implementations ——————————————————————————————————————————————————————————
#

def page_welcome():
    
    if FRESH_FLAG not in st.session_state:
        for f in (SIM_FILE, ROLES_FILE):
            if os.path.exists(f):
                os.remove(f)
        st.session_state[FRESH_FLAG] = True

    for key in ['simulation_name', 'teamwork_submitted', 'dm_finished', 'role']:
        st.session_state[key] = None if key == 'role' else False if key != 'simulation_name' else ''
    st.session_state['page'] = 'welcome'

    st.title("Welcome to CHIRON Training System")
    st.write("""
This system lets you **participate in** or **supervise** a CHIRON astronaut simulation.
Please select your role to continue.
    """)

    role = st.radio("I am a:", ["Decision Maker", "Supervisor"])
    clicked = st.button("Next")
    if clicked:
        if role == "Supervisor":
            st.session_state.role = role
            nav_to('supervisor_menu')

        else:  # Decision Maker
            # only let them through if the supervisor has already submitted
            if not os.path.exists(SIM_FILE):
                st.error("🚫 Supervisor must submit a simulation name first.")
            else:
                nav_to('dm_role_claim') 
                

def page_supervisor_menu():
    st.header("Supervisor Setup")

    sim  = st.session_state.simulation_name

    if st.button("Start Simulation") and sim:
        conn = sqlite3.connect("astronaut_quiz.db")
        conn.execute("DROP TABLE IF EXISTS quiz_results;")
        conn.commit()
        conn.close()
        st.session_state.simulation_name = sim
        st.rerun()


    if st.session_state.simulation_name:
         st.markdown(f"**Simulation Name:** {st.session_state.simulation_name}")
    else:
        sim_input = st.text_input("Enter simulation name", value="")
        if st.button("Submit Name"):
            save_current(sim_input.strip())
            st.session_state.simulation_name = sim_input.strip()
            st.success(f"Simulation '{sim_input.strip()}' registered.")
    
    st.subheader("Roles Claimed")
    claimed = load_selected_roles()
    if not claimed:
        st.write("_None yet_")
    else:
        for r in claimed:
            st.write(f"- **{r}** — {questionnaire1.roles[r]}")
    
    if st.button("Refresh Roles"):
        st.rerun() 

    # 3) Only once name + exactly 8 roles claimed do we unlock next steps:
    can_go = bool(st.session_state.simulation_name) and len(claimed) == 8

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Show Dashboard", disabled=not can_go):
            nav_to('live_dashboard')
    with c2:
        if st.button("Team Assessment Form", disabled=not can_go):
            nav_to('teamwork_survey')

    if st.button("← Back to Welcome"):
        # clear both files
        if os.path.exists(SIM_FILE):   os.remove(SIM_FILE)
        if os.path.exists(ROLES_FILE): os.remove(ROLES_FILE)
        st.session_state.clear()
        nav_to('welcome')

def page_live_dashboard():
    data_simulation.run(simulation_name=st.session_state.simulation_name)

    if st.button("← Back to Menu"):
        nav_to('supervisor_menu')

def page_teamwork_survey():
    teamwork.run(simulation_name=st.session_state.simulation_name)

    if st.session_state.teamwork_submitted:
        sim = st.session_state.simulation_name
        generate_sql.init_db(sim)
        comments = st.session_state.get("teamwork_feedback_text", "")
        scores = st.session_state.get("teamwork_scores", {})
        generate_sql.write_supervisor_scoring(
            sim,
            st.session_state.supervisor,
            comments,
            scores
        )
        st.success("✅ Supervisor scores saved.")
        nav_to('certify_and_results')

TEAMWORK_SQL = """
  SELECT supervisor, leadership_score, teamwork_score, task_score, overall_score, total_score, comments, submitted_at "
    "FROM supervisor_scoring WHERE simulation_name = ?"
"""

TEAMSCORES_SQL = """
  SELECT criterion, total_score,
            Basic_Life_Support_team, Primary_Survey_team, Secondary_Survey_team,
            Definitive_Care_team, medical_knowledge_team,
            Crew_Roles_Communication_team, Systems_Procedural_Knowledge_team,
            procedural_knowledge_team,
            mental_team, physical_team, temporal_team,
            performance_team, effort_team, frustration_team,
            taskload,
            submitted_at
        FROM team_scoring
    WHERE simulation_name = ?
"""

def page_certify_and_results():
    st.header("Certification & Combined Results")
    st.write("Make sure the simulation ran and the teamwork form is complete.")

    if not st.session_state.teamwork_submitted:
        st.warning("Teamwork form not submitted yet.")
        return

    if st.button("✅ Certify Simulation Completed and View Team Results"):
        st.session_state.simulation_certified = True
        sim_name  = st.session_state.simulation_name
        generate_sql.init_db(sim_name)
        comments = st.session_state.get("teamwork_feedback_text", "")
        scores = st.session_state.get("teamwork_scores", {})
        generate_sql.write_supervisor_scoring(
            sim_name,
            st.session_state.supervisor,
            comments,
            scores
        )
        generate_sql.write_team_scoring(sim_name)
        generate_sql.write_csv_exports(sim_name)
        st.success("✅ Supervisor scores saved.")
        nav_to('team_results')

def page_team_results():
    print("🚨 ENTER page_team_results(), simulation_certified=", st.session_state.simulation_certified)
    if not st.session_state.simulation_certified:
        st.error("❗️ You must certify the simulation as completed before viewing team results.")
        return
    st.header("🏆 Team Performance Results")
    print("🚨 page_team_results: teamwork.metrics =", getattr(teamwork, "metrics", None))
    sim_name = st.session_state.simulation_name
    print("🚨 page_team_results: sim_name =", sim_name)
    metrics = getattr(teamwork, "metrics", None)
    print("🚨 raw teamwork.metrics keys:", list(metrics.keys()))

    if not sim_name:
        st.error("❗️ No simulation name found. Go back and re-save your results first.")
        return

    sim = st.session_state.simulation_name

    # 1) Supervisor’s own scores
    df_sup = pd.read_sql_query(
    "SELECT supervisor, leadership_score, teamwork_score, task_score, overall_score, total_score, comments, submitted_at "
    "FROM supervisor_scoring WHERE simulation_name = ?",
    sqlite3.connect(f"{sim}.db"),
    params=(sim,)
    )
    st.subheader("🔹 Supervisor’s TEAM Questionnaire")
    st.dataframe(df_sup)

    # 2) Decision-Maker aggregate
    df_dm = pd.read_sql_query(
    """
    SELECT criterion, total_score,
            Basic_Life_Support_team, Primary_Survey_team, Secondary_Survey_team,
            Definitive_Care_team, medical_knowledge_team,
            Crew_Roles_Communication_team, Systems_Procedural_Knowledge_team,
            procedural_knowledge_team,
            mental_team, physical_team, temporal_team,
            performance_team, effort_team, frustration_team,
            taskload,
            submitted_at
        FROM team_scoring
    WHERE simulation_name = ?
    """,
    sqlite3.connect(f"{sim}.db"),
    params=(sim,)
    )
    st.subheader("🔸 Decision-Maker Aggregate Performance")
    st.dataframe(df_dm)



def page_review_roles():
    st.header("Who’s in this Simulation?")
    for r in load_selected_roles():
         st.write(f"- **{r}** — {questionnaire1.roles[r]}")
    can_start = len(load_selected_roles()) == 8
    if st.button("Begin Simulation", disabled=not can_start):
        nav_to('dm_questionnaire')
    if not can_start:
        st.warning("All 8 roles must be claimed before starting the simulation.")
    if st.button("Refresh Roles"):
        st.rerun() 

def page_dm_role_claim():
    st.header("Claim Your Role")
    claimed = load_selected_roles()
    all_roles = list(questionnaire1.roles.keys())
    available = [r for r in all_roles if r not in claimed]

    st.write("Roles already taken:")
    if not claimed:
        st.write("_None yet_")
    else:
        st.write(", ".join(claimed))

    if st.button("Refresh Roles"):
        st.rerun()

    # Let me pick from the *remaining* ones
    choice = st.selectbox("Choose your role", options=available)
    if st.button("Submit Role"):
        save_selected_role(choice)
        st.session_state.roles = load_selected_roles()
        st.session_state.dm_role = choice
        nav_to('review_roles')   # jump straight to review

def page_dm_questionnaire():
    # Show the DM’s own role and the simulation name
    name = load_current()
    if name:
        st.session_state.simulation_name = name
        
    st.markdown(f"### Role: **{st.session_state.dm_role}**")
    st.markdown(f"### Simulation: **{st.session_state.simulation_name}**")
    st.session_state.simulation_name = load_current()

    # Run the questionnaire, passing in both simulation name and role
    questionnaire1.run(
        simulation_name=st.session_state.simulation_name,
        role=st.session_state.dm_role
    )

    # Once they finish, let them view results
    if st.session_state.dm_finished:
        st.write("")
        if st.button("View Your Individual Results", key="view_results_cc"):
            sim_name = st.session_state.simulation_name
            role = st.session_state.dm_role
            answers    = st.session_state.answers
            times      = st.session_state.answer_times
            all_qs     = st.session_state.all_questions
            totals     = st.session_state.dm_totals
            tlx        = st.session_state.tlx_answers
            generate_sql.init_db(sim_name)
            generate_sql.write_answers(
                sim_name, answers, times, all_qs, role,
                questionnaire1.get_score_breakdown
            )
            generate_sql.write_individual_scores(sim_name, role, totals, tlx)

            st.success("✅ All data saved!")
            nav_to("individual_results")


ANSWERS_SQL = """
  SELECT inject, question_text, answer_text, score,
         Basic_Life_Support, Primary_Survey, Secondary_Survey, Definitive_Care,                  
         Crew_Roles_Communication, Systems_Procedural_Knowledge 
    FROM answers
   WHERE simulation_name = ?
     AND role = ?
ORDER BY id
"""

IND_SQL = """
  SELECT Basic_Life_Support, Primary_Survey, Secondary_Survey, Definitive_Care,
         medical_knowledge,                   
         Crew_Roles_Communication, Systems_Procedural_Knowledge, 
         procedural_knowledge, mental, physical, temporal,
         performance, effort, frustration, taskload
    FROM individual_scores
   WHERE simulation_name = ?
     AND role = ?
"""


def page_individual_results():
    st.header("Your Individual Results")
    sim_name = st.session_state.simulation_name
    dm_role  = st.session_state.dm_role
    roles = [
        "SO (EVA2)", "Commander (CMO, IV1)", "FE-1 (EVA1)",
        "FE-2 (IV1)", "FD", "FS", "BME", "CAPCOM"
    ]
    # Open the DB once
    conn = sqlite3.connect(f"{sim_name}.db")


    # 2) Then per-role answers & scores
    for role in roles:
        safe     = dm_role.replace(" ", "_")
        df_ans = pd.read_sql_query(
            ANSWERS_SQL, conn, params=(sim_name, dm_role)
        )
        df_ans.to_csv(f"{sim_name}_answers_{safe}.csv", index=False)

        df_ind = pd.read_sql_query(
            IND_SQL, conn, params=(sim_name, dm_role)
        )
        df_ind.to_csv(f"{sim_name}_individual_scores_{safe}.csv", index=False)

    conn.close()

    st.success("All CSVs generated!")


    if not sim_name:
        st.error("❗️ No simulation name found. Please go back and re-save your results.")
        return
    conn = sqlite3.connect(f"{sim_name}.db")
    df   = pd.read_sql("SELECT * FROM individual_scores WHERE role = ?", conn, params=(st.session_state.dm_role,))
    conn.close()
    
    try:
        safe_dm = dm_role.replace(" ", "_")
        df_ans = pd.read_csv(f"{sim_name}_answers_{safe_dm}.csv")
        df_ind = pd.read_csv(f"{sim_name}_individual_scores_{safe_dm}.csv")
    except FileNotFoundError as e:
        st.error(f"❗️ Missing CSV: {e.filename}")
        return

    st.header("Your Individual Results")

    st.subheader("🔹 Your Answers")
    st.dataframe(df_ans)

    st.subheader("🔸 Your Total Scores")
    st.dataframe(df_ind)

#
# ——— Main routing ——————————————————————————————————————————————————————————————
#

def main():
    init_state()
    # read our in-memory page
    page = st.session_state.page
    pages = {
        'welcome': page_welcome,
        'supervisor_menu': page_supervisor_menu,
        'review_roles': page_review_roles,
        'dm_role_claim': page_dm_role_claim,      
        'live_dashboard': page_live_dashboard,
        'teamwork_survey': page_teamwork_survey,
        'certify_and_results': page_certify_and_results,
        'team_results': page_team_results,
        'dm_questionnaire': page_dm_questionnaire,
        'individual_results': page_individual_results,
    }

    if page not in pages:
        # clear out whatever bogus page param was there
        # st.set_query_params()
        # and default back to welcome
        pages['welcome']()
        return

    # otherwise go to the requested page
    pages[page]()

if __name__ == '__main__':
    main()




