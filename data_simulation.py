import streamlit as st
import matplotlib.pyplot as plt
import random
from supabase_client import supabase
from questionnaire1 import (
    _ensure_answer_indexes, preload_answers,
    apply_vital_consequences,  # <-- import it
)

# ---------- tiny helper to know if a step is already answered ----------
def normalize_inject_prefix(raw: str) -> str:
    """Return canonical prefix: 'Initial Situation', 'Inject N', 'Decision N'."""
    if not raw:
        return ""
    raw = str(raw).strip()
    import re
    m = re.match(r'^(Initial Situation|Inject\s+\d+|Decision\s+\d+)', raw, flags=re.IGNORECASE)
    if not m:
        return raw  # unknown pattern, return as-is
    pref = m.group(1)
    # Uniform capitalization: “Decision 7”, “Inject 3”
    parts = pref.split()
    if parts[0].lower() in ("decision", "inject"):
        return f"{parts[0].capitalize()} {parts[1]}"
    if pref.lower().startswith("initial"):
        return "Initial Situation"
    return pref

def is_decision_answered(prefix: str) -> bool:
    """True if someone answered this decision (not SKIP)."""
    prefix_norm = normalize_inject_prefix(prefix)

    # 1) Cached index (built by _cache_answer_row → normalize_inject_prefix)
    pid_map = st.session_state.get("answers_by_prefix", {}).get(prefix_norm, {})
    if any(v and v != "SKIP" for v in pid_map.values()):
        return True

    # 2) DB fallback – match full label with ILIKE
    sim_id = st.session_state.get("simulation_id")
    if not sim_id:
        return False
    try:
        rows = (supabase
                .from_("answers")
                .select("answer_text, inject")
                .eq("id_simulation", sim_id)
                .ilike("inject", f"{prefix_norm}%")   # <- catch "(10:37:00)"
                .execute()).data or []
        return any(r["answer_text"] and r["answer_text"] != "SKIP" for r in rows)
    except Exception:
        return False


def vary_vital(base, min_val, max_val, unit=""):
    variation = random.randint(-2, 2)
    value = base + variation
    value = max(min_val, min(value, max_val))
    return f"{value}{unit}"


# Custom CSS for styling
def inject_css():
    st.markdown(
        """
        <style>
        .main .block-container { padding-top: 0rem; padding-bottom: 0rem; }
        .astronaut-box {
            background-color: #1E3A5F;
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 10px;
        }
        .metric-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            flex-wrap: wrap;
        }
        .metric-container div {
            flex: 1;
            text-align: center;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Define astronaut data
astronauts = [
    {"name": "Mariana Peyroteo", "role": "FE-1(EV1)", "age": 50, "gender": "Female", "status": "Normal"},
    {"name": "Ana Martins", "role": "FE-3(EV2)", "age": 45, "gender": "Female", "status": "Warning"},
    {"name": "Joana Godinho", "role": "Commander (CMO,IV2)", "age": 47, "gender": "Female", "status": "Critical"},
    {"name": "Mariana Figueiras", "role": "FE-2(IV1)", "age": 40, "gender": "Female", "status": "Normal"},
]


def run(simulation_name: str, updates:int=10, delay:float=1.0):
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, limit=None, key="vitals_autorefresh")

    inject_css()
    st.session_state.setdefault("vital_effects", {})
    st.header(f"🚀 Decision Suport Dashboard: {simulation_name}")
    _ensure_answer_indexes()
    preload_answers(st.session_state.get("simulation_id"))
    apply_vital_consequences({})

    effects_all = st.session_state.setdefault("vital_effects", {})

    # initial heart rates in session
    if 'heart_rates' not in st.session_state:
        st.session_state.heart_rates = {astro['role']: 75 for astro in astronauts}

    # layout columns
    # astronaut_list: uma lista com os astronautas ativos
    cols = st.columns(len(astronauts))

    for col, astro in zip(cols, astronauts):
        with col:
            effects_all = st.session_state.get("vital_effects", {})
            effects      = effects_all.get(astro["role"], {})
            status = effects.get("status", "online" if astro["role"] in ["FE-1(EV1)", "FE-3(EV2)"] else "offline")

            # Fase inicial: gerar valores variáveis até decisão 7
            _ensure_answer_indexes()
            preload_answers(st.session_state.get("simulation_id"))

            answered1 = is_decision_answered("Decision 1")
            if not answered1:
                if "dynamic_vitals" not in st.session_state:
                    st.session_state.dynamic_vitals = {}

                if astro["role"] not in st.session_state.dynamic_vitals:
                    st.session_state.dynamic_vitals[astro["role"]] = {}

                # Atualiza os valores aleatórios em cada ciclo
                st.session_state.dynamic_vitals[astro["role"]].update({
                    "hr": vary_vital(85, 78, 92, " bpm"),
                    "rr": vary_vital(15, 12, 18, " rpm"),
                    "spo2": vary_vital(98, 95, 99, "%"),
                    "bp": f"{random.randint(115, 125)}/{random.randint(70, 78)} mmHg",
                    "co2": vary_vital(40, 37, 43, " mmHg"),
                })

                hr   = st.session_state.dynamic_vitals[astro["role"]]["hr"]
                rr   = st.session_state.dynamic_vitals[astro["role"]]["rr"]
                spo2 = st.session_state.dynamic_vitals[astro["role"]]["spo2"]
                bp   = st.session_state.dynamic_vitals[astro["role"]]["bp"]
                co2  = st.session_state.dynamic_vitals[astro["role"]]["co2"]

            else:
                # Fase após Decision 7 — usar valores fixos definidos nos efeitos
                hr   = effects.get("hr", "85 bpm")
                rr   = effects.get("rr", "15 rpm")
                spo2 = effects.get("spo2", "98%")
                bp   = effects.get("bp", "120/72 mmHg")
                co2  = effects.get("co2", "40 mmHg")

            temp  = effects.get("temp")
            gluc  = effects.get("glucose")
            elec  = effects.get("electrolytes")
            nihss = effects.get("nihss")
            diag  = effects.get("diagnostic")

            # Card style
            st.markdown(f"""
            <div style='background-color:#002b50;padding:16px;border-radius:12px;color:white;text-align:center;'>
                <h5 style='margin-bottom:4px'>{astro['role']} ({astro['name']})</h5>
                <small>Age: {astro['age']} | Gender: {astro['gender']}</small>
            </div>
            """, unsafe_allow_html=True)

            if status == "offline":
                st.markdown("<div style='background:#fffbe6;color:#b30000;border-radius:10px;padding:16px;text-align:center;margin-top:8px;'>❌ No data available.</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background:white;padding:12px;border-radius:10px;margin-top:8px;font-size:0.95em;'>
                """, unsafe_allow_html=True)

                st.markdown(f"❤️ **Heart Rate:** {hr}", unsafe_allow_html=True)
                st.markdown(f"🫁 **Resp Rate:** {rr}", unsafe_allow_html=True)
                st.markdown(f"🩸 **Blood Pressure:** {bp}", unsafe_allow_html=True)
                st.markdown(f"🫀 **SpO₂:** {spo2}", unsafe_allow_html=True)
                if co2: st.markdown(f"🫧 **CO₂:** {co2}", unsafe_allow_html=True)
                if temp: st.markdown(f"🌡 **Temp:** {temp}", unsafe_allow_html=True)
                if gluc: st.markdown(f"🧃 **Glucose:** {gluc}", unsafe_allow_html=True)
                if elec: st.markdown(f"🧪 **Electrolytes:** {elec}", unsafe_allow_html=True)
                if nihss: st.markdown(f"🧠 **NIHSS:** {nihss}", unsafe_allow_html=True)
                if diag: st.markdown(f"📋 *{diag}*", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
