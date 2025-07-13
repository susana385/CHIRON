# participant_app.py
import streamlit as st

pid = st.experimental_get_query_params().get("participant_id", [None])[0]
sim = st.experimental_get_query_params().get("sim", [None])[0]
if not pid or not sim:
    st.error("Missing participant_id or sim in URL")
    st.stop()

# load that participant’s state from Supabase, then render exactly what they should see
# e.g. look up their current inject, question, etc.
# … all your existing code …
