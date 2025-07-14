import streamlit as st
import matplotlib.pyplot as plt
import random

def vary_vital(base, min_val, max_val, unit=""):
    variation = random.randint(-2, 2)
    value = base + variation
    value = max(min_val, min(value, max_val))
    return f"{value}{unit}"


# note: st.set_page_config should only be called once at the very top of your app
# so omit it here if already set in chiron_control_center

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
    {"name": "Jack Marshall", "role": "EVA 1", "age": 50, "gender": "Male", "status": "Normal"},
    {"name": "Clara Jensen", "role": "EVA 2", "age": 45, "gender": "Female", "status": "Warning"},
    {"name": "Hiroshi Tanaka", "role": "Commander", "age": 47, "gender": "Male", "status": "Critical"},
    {"name": "Miguel Costa", "role": "Pilot", "age": 40, "gender": "Male", "status": "Normal"},
]

# Helper for status label color
status_classes = {"Normal": "✅", "Warning": "⚠️", "Critical": "❌"}

# ECG generation and HR calculation





def run(simulation_name: str, updates:int=10, delay:float=1.0):
    # from streamlit_autorefresh import st_autorefresh
    # st_autorefresh(interval=2000, limit=None, key="vitals_autorefresh")
    if st.button("🔄 Refresh"):
            st.rerun()

    inject_css()
    st.session_state.setdefault("vital_effects", {})
    st.header(f"🚀 Decision Suport Dashboard: {simulation_name}")


    # initial heart rates in session
    if 'heart_rates' not in st.session_state:
        st.session_state.heart_rates = {astro['role']: 75 for astro in astronauts}

    # layout columns
    # astronaut_list: uma lista com os astronautas ativos
    cols = st.columns(len(astronauts))

    for col, astro in zip(cols, astronauts):
        with col:
            effects = st.session_state.get("vital_effects", {}).get(astro["role"], {})
            status = effects.get("status", "online" if astro["role"] in ["EVA 1", "EVA 2"] else "offline")

            # Fase inicial: gerar valores variáveis até decisão 7
            answered7 = any(k.startswith("Decision 7") for k in st.session_state.get("answers", {}))
            if not answered7:
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
