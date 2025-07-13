import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import neurokit2 as nk  # ✅ Using neurokit2 for real ECG signals

# Set page title and layout
st.set_page_config(page_title="Astronaut Vital Signs Monitoring", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main .block-container { padding-top: 0rem; padding-bottom: 0rem; }
    .astronaut-box {
        background-color: #1E3A5F; /* Dark Blue */
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
    {"name": "Jack Marshall", "role": "EVA 1", "age": 45, "gender": "Male", "status": "Normal"},
    {"name": "Clara Jensen", "role": "EVA 2", "age": 45, "gender": "Female", "status": "Warning"},
    {"name": "Hiroshi Tanaka", "role": "Commander", "age": 45, "gender": "Male", "status": "Critical"},
    {"name": "Miguel Costa", "role": "Pilot", "age": 45, "gender": "Male", "status": "Normal"},
]

# Function to determine clinical status color
def get_status_class(status):
    return "normal" if status == "Normal" else "warning" if status == "Warning" else "critical"

# ✅ Generate a realistic ECG waveform using `neurokit2`
def generate_ecg(signal_type):
    duration = 5  # 5 seconds of ECG
    sampling_rate = 300  # 300Hz (standard for ECG)
    
    ecg_signal = nk.ecg_simulate(duration=duration, sampling_rate=sampling_rate)

    # Modify ECG based on condition
    if signal_type == "Arrhythmia":
        ecg_signal += np.random.normal(0, 0.2, len(ecg_signal))  # Introduce noise
    elif signal_type == "Bradycardia":
        ecg_signal = np.interp(np.linspace(0, 1, 200), np.linspace(0, 1, len(ecg_signal)), ecg_signal)  # Slower HR
    elif signal_type == "Tachycardia":
        ecg_signal = np.interp(np.linspace(0, 1, 400), np.linspace(0, 1, len(ecg_signal)), ecg_signal)  # Faster HR

    return np.linspace(0, duration, len(ecg_signal)), ecg_signal, sampling_rate

# Function to calculate heart rate from ECG peaks
def calculate_heart_rate(ecg_signal, sampling_rate):
    try:
        processed_ecg, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_rate)
        heart_rate = int(np.mean(info["ECG_Rate"]))  # Average HR over the segment
    except:
        heart_rate = np.random.randint(60, 100)  # Fallback HR if detection fails
    return heart_rate

# ✅ Use `st.session_state` to store previous values and avoid flickering
if "heart_rates" not in st.session_state:
    st.session_state.heart_rates = {astro["role"]: 70 for astro in astronauts}

# Display the dashboard title
st.markdown("<h1 class='title-space'>🚀 CHIRON Dashboard</h1>", unsafe_allow_html=True)

# Create four **equal-sized** columns to fit all astronauts
columns = st.columns(4)

# Create placeholders for each astronaut's ECG and HR
ecg_placeholders = {}
heart_rate_placeholders = {}

# Loop through astronauts and display their **entire info inside the blue box**
for col, astronaut in zip(columns, astronauts):
    with col:
        # Start blue box
        st.markdown(f"""
        <div class="astronaut-box">
            <h3>{astronaut['role']} ({astronaut['name']})</h3>
            <p>Age: {astronaut['age']} | Gender: {astronaut['gender']}</p>
        """, unsafe_allow_html=True)
        
        # Clinical Presentation Status (Outside the Blue Box)
        st.markdown(f"**Clinical Presentation:** {get_status_class(astronaut['status'])}")

        # ECG Type Selection inside blue box
        ecg_type = st.selectbox(f"ECG ({astronaut['role']})", ["Normal", "Arrhythmia", "Bradycardia", "Tachycardia"], key=astronaut["role"])

        # ✅ Create placeholders for ECG & HR **inside** the astronaut’s column
        ecg_placeholders[astronaut["role"]] = st.empty()
        heart_rate_placeholders[astronaut["role"]] = st.empty()  # Placeholder for dynamic HR

        # ✅ **Align all vitals perfectly using `st.columns()`**
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                heart_rate_placeholders[astronaut["role"]].metric(label="❤️ Heart Rate", value=f"{st.session_state.heart_rates[astronaut['role']]} bpm")
                st.metric(label="💨 Resp Rate", value="15 rpm")
                st.metric(label="🩸 Blood Pressure", value="120/72 mmHg")
                st.metric(label="🫁 SpO₂ (Oxygen Saturation)", value="98%")
            with col2:
                st.metric(label="🧪 Glucose", value="80 mg/dL")
                st.metric(label="🧂 Electrolytes", value="132 k 4.2 mmol/L")
                st.metric(label="🌡️ Temp", value="36.0°C")
                st.metric(label="🫧 CO₂ (Carbon Dioxide)", value="40 mmHg")

        # Close blue box
        st.markdown("</div>", unsafe_allow_html=True)

# --- Real-time ECG & Heart Rate Update for ALL Astronauts ---
while True:
    for astronaut in astronauts:
        role = astronaut["role"]
        ecg_type = st.session_state[role]  # Get selected ECG type

        t, ecg_signal, sampling_rate = generate_ecg(ecg_type)  # Get ECG signal
        heart_rate = calculate_heart_rate(ecg_signal, sampling_rate)  # Calculate HR from ECG

        # ✅ Store HR in session state to avoid flickering
        st.session_state.heart_rates[role] = heart_rate

        # ✅ Update Heart Rate dynamically inside astronaut's column
        heart_rate_placeholders[role].metric(label="❤️ Heart Rate", value=f"{heart_rate} bpm")

        # ✅ Plot the ECG signal **inside each astronaut's column** without flickering
        with ecg_placeholders[role].container():
            fig, ax = plt.subplots(figsize=(3, 1.5))  # Adjusted size to fit in the column
            ax.plot(t, ecg_signal, label=ecg_type, color="red", linewidth=0.8)
            ax.set_xticks([])  
            ax.set_yticks([])
            ax.legend(fontsize=8)

            # ✅ Ensure ECG is plotted **inside** the astronaut's column
            ecg_placeholders[role].pyplot(fig)

    time.sleep(1)  # Refresh every second
