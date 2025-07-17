import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
from typing import Dict
from supabase_client import supabase

# ———————————————————————————
# Constants & helper
# ———————————————————————————


likert_options = [
    "Please select an option",
    "0 – Never/Hardly ever",
    "1 – Seldom",
    "2 – About as often as not",
    "3 – Often",
    "4 – Always/Nearly always"
]

def get_score(choice: str) -> int:
    return int(choice.split('–')[0].strip())

# ———————————————————————————
# Pages
# ———————————————————————————

def page_one():
    st.title("Team Emergency Assessment Measure (TEAM)")
    st.write("""
    This tool lets you, the supervisor, evaluate your team's 
    performance during a simulation on three domains:  
    Leadership, Teamwork, and Task Management.
    """)
    
    if st.button("Start the Questionnaire"):
        st.session_state.teamwork_page = 2

metrics: dict[str, float] = {}
feedback_text: str = ""

def page_two():
    sim_id   = st.session_state.get("simulation_id")
    sim_name = st.session_state.get("simulation_name")
    if not sim_id or not sim_name:
        st.error("❌ Simulation context missing — please join a simulation first.")
        return
    st.subheader(f"TEAM Questionnaire")

    st.markdown("### 🧭 Leadership")
    st.markdown("_It is assumed that the leader is either designated, has emerged, or is the most senior — if no leader emerges allocate a ‘0’ to questions 1 & 2._")

    resp: Dict[str, str] = st.session_state.teamwork_responses

    resp['Q1'] = st.selectbox("1. The team leader let the team know what was expected of them through direction and command", likert_options, key='q1')
    resp['Q2'] = st.selectbox("2. The team leader maintained a global perspective (e.g. monitoring clinical procedures and the environment, delegation)", likert_options, key='q2')

    st.markdown("### 🤝 Teamwork")
    st.markdown("_Ratings should include the team as a whole, i.e. the leader and the team as a collective._")

    teamwork_questions = {
        3: "3. The team communicated effectively",
        4: "4. The team worked together to complete tasks in a timely manner",
        5: "5. The team acted with composure and control",
        6: "6. The team morale was positive (e.g. support, confidence, spirit)",
        7: "7. The team adapted to changing situations (e.g. deterioration, role change)",
        8: "8. The team monitored and reassessed the situation",
        9: "9. The team anticipated potential actions (e.g. drugs, defibrillator prep)"
    }
    for i in range(3, 10):
        resp[f'Q{i}'] = st.selectbox(teamwork_questions[i], likert_options, key=f'q{i}')

    st.markdown("### 🛠️ Task Management")
    resp['Q10'] = st.selectbox("10. The team prioritised tasks", likert_options, key='q10')
    resp['Q11'] = st.selectbox("11. The team followed approved standards/guidelines", likert_options, key='q11')

    st.markdown("### 🌟 Overall Performance")
    resp['Q12'] = st.slider("12. On a scale of 1–10, give your global rating of the team's performance", 1, 10, 5, key='q12_slider')

    st.text_area("📝 Comments:", key='comments', height=100)

    if st.button("✅ Submit and Continue"):
        if any(resp.get(f'Q{i}', "") == likert_options[0] for i in range(1, 12)):
            st.error("⚠️ Please answer all Likert questions (Q1–Q11) before submitting.")
            return

        # Compute domain scores
        leadership = get_score(resp['Q1']) + get_score(resp['Q2'])
        teamwork   = sum(get_score(resp[f'Q{i}']) for i in range(3, 10))
        task       = get_score(resp['Q10']) + get_score(resp['Q11'])
        overall    = resp['Q12']  # already an int from slider
        total      = leadership + teamwork + task + overall
        comments = resp.get('coments','')

        payload = {
            "id_simulation":       sim_id,
            "simulation_name":     sim_name,   
            "leadership":          leadership,
            "teamwork":            teamwork,
            "task_management":     task,
            "overall_performance": overall,
            "total":               total,
            "comments":            comments,
        }
        try:
            supabase.from_("teamwork").insert(payload).execute()
            st.success("✅ Teamwork assessment saved!")
        except Exception as e:
            st.error(f"❌ Failed to save teamwork assessment: {e}")

        
# ———————————————————————————
# Public entrypoint
# ———————————————————————————

def run(simulation_name: str):
    """Render the TEAM flow only when called from your main app."""
    # initialize our private keys
    st.session_state.setdefault('teamwork_page', 1)
    st.session_state.setdefault('teamwork_submitted', False)
    st.session_state.setdefault('teamwork_responses', {})
    st.session_state.setdefault('teamwork_scores', {})

    # dispatch internally
    p = st.session_state.teamwork_page
    if p == 1:
        page_one()
    elif p == 2:
        page_two()





