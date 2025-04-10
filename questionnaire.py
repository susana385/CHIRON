import streamlit as st
import sqlite3
import time

st.markdown("""
    <style>
        .main .block-container { max-width: 900px; padding-top: 2rem; }
        h1, h2, h3, h4 { font-size: 24px !important; }
        p { font-size: 18px !important; line-height: 1.6; }
        div.stButton > button {
            width: 100%; height: 50px; font-size: 18px; font-weight: bold; border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

conn = sqlite3.connect("astronaut_quiz.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT, inject TEXT, question TEXT, answer TEXT, correct_answer TEXT, score INTEGER
)
""")
conn.commit()

roles = {
    "EVA2": "Flight Engineer (Science Officer) - Outside performing EVA.",
    "Commander": "Chief Medical Officer (CMO) - Inside the station.",
    "Pilot": "IV Crew Member - Inside the station.",
    "MCC": "Mission Control Crew - Monitoring from Earth."
}

if "role_selected" not in st.session_state:
    st.session_state.role_selected = False
    st.session_state.role = None
    st.session_state.stage = 0  
    st.session_state.current_decision_index = 0 
    st.session_state.answers = {}


if not st.session_state.role_selected:
    st.title("🚀 CHIRON Decision-Making Questionnaire")
    role = st.selectbox("Select Your Role", list(roles.keys()))
    st.markdown(f"<p><strong>Role Description:</strong> {roles[role]}</p>", unsafe_allow_html=True)
    if st.button("Next ➡ Begin Simulation"):
        st.session_state.role_selected = True
        st.session_state.role = role
        st.session_state.stage = 0  
        st.session_state.answers = {}
        st.session_state.current_decision_index = 0
        st.rerun()
    st.stop()

role = st.session_state.role

# ----------------------------------------------------- 1 to 12 --------------------------------------

decisions1to12 = [
    {"inject": "Decision 1 (10:00:30): ", "text": "What should be suggested?", 
        "options": ["A. Rest", "B. Return", "C. Check suit", "D. Prepare EVA3"], "correct": "B. Return",
 "max_time": 30 },

    {"inject": "Decision 2 (10:16:00): ", "text": "What should EVA2 do?", 
        "options": ["A. Assist", "B. Call help", "C. Return", "D. Prepare EVA3"], "correct": "B. Call help",
 "max_time": 30 },
    
    {"inject": "Decision 3 (10:16:30): ", 
        "role_specific": {
            "Commander": {"text": "What should the Commander do?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC",
 "max_time": 30 },
            "Pilot": {"text": "What should the Pilot do?", "options": ["A. Contact EVA2"], "correct": "A. Contact EVA2",
 "max_time": 30 },
            "EVA2": {"text": "What should EVA2 do?", "options": ["A. Confirm symptoms"], "correct": "A. Confirm symptoms",
 "max_time": 30 },
            "MCC": {"text": "What should MCC do?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist",
 "max_time": 30 },
        }
    },

    {"inject": "Decision 4 (10:18:30): ", "text": "Best course of action?", 
        "options": ["A. ALS", "B. Return & FAST"], "correct": "B. Return & FAST",
 "max_time": 30 },

    {"inject": "Decision 5 (10:19:00): ", "text": "Possible diagnosis?", 
        "options": ["A. Stroke", "B. Syncope", "C. Wernicke’s"], "correct": "A. Stroke",
 "max_time": 30 },

    {"inject": "Decision 6 (10:19:30): ", "text": "Time to treatment?", 
        "options": ["A. 60 min", "B. ASAP", "C. 40 min", "D. Different"], "correct": "B. ASAP",
 "max_time": 30 },
    
    {"inject": "Decision 7 (10:20:00): ", "text": "Pressurization method?", 
        "options": ["A. Partial", "B. Normal", "C. Emergency"], "correct": "C. Emergency",
 "max_time": 30 },

    {"inject": "Decision 8 (10:23:00):", 
        "role_specific": {
            "Commander": {"text": "While the EVA 2 is transporting the patient, what the crew inside can do to prepare for their arrival?", "options": ["A.The commander can confirm the medical emergency protocols with the Flight Surgeon; Pilot can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed"], "correct": "A. The commander can confirm the medical emergency protocols with the Flight Surgeon; Pilot can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed",
 "max_time": 30 },
            "Pilot": {"text": "While the EVA 2 is transporting the patient, what the crew inside can do to prepare for their arrival?", "options": ["A. The commander can confirm the medical emergency protocols with the Flight Surgeon; Pilot can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed"], "correct": "A. The commander can confirm the medical emergency protocols with the Flight Surgeon; Pilot can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed",
 "max_time": 30 },
            "EVA2": {"text": "How should the EVA 2 transport the patient?", "options": ["A. figures"], "correct": "A. figures",
 "max_time": 30 },
            "MCC": {"text": "While the EVA 2 is transporting the patient, what the crew inside can do to prepare for their arrival?", "options": ["A. The commander can confirm the medical emergency protocols with the Flight Surgeon; Pilot can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed"], "correct": "A. The commander can confirm the medical emergency protocols with the Flight Surgeon; Pilot can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed",
 "max_time": 30 },
        }
    },

    {"inject": "Decision 9 (10:24:00):", "text": "What protocol should be followed?", 
        "options": ["A. 1.102 AED ASSISTED CPR", "B. 1.101 SEVERE ALLERGIC REACTION", "C. 1.103 ALS ALGORITHM", "D. 1.206 STROKE ALGORITHM"], "correct": "D. 1.206 STROKE ALGORITHM",
 "max_time": 30 }, 

    {"inject": "Decision 10 (10:24:30):", "text": "Where should the medical assistance be performed?", 
        "options": ["A. Near the Joint Airlock Quest where the Crew Medical Restraint System is possible to fixate", "B. Near where all the medical equipment is", "C. Outside the station", "D. One needs to wait to leave airlock"], "correct": "A. Near the Joint Airlock Quest where the Crew Medical Restraint System is possible to fixate",
 "max_time": 30 }, 

    {"inject": "Decision 11 (10:25:00):", 
     "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
     "options": [
         "A. Crew Medical Restraint System (CMR)", 
         "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
         "C. Medical Diagnostic Pack (Blue)", 
         "D. Medical Supply Pack (Green)",
         "E. Minor Treatment Pack (Pink)", 
         "F. Oral Medication Pack (Purple)",
         "G. Physician Equipment Pack (Yellow)", 
         "H. Topical & Injectable Medication Pack - Medications (Brown)",
         "I. Convenience Medication Pack (White)", 
         "J. IV Supply Pack (Gray)", 
         "K. Advanced Life Support Pack (ALSP) & Other Componentes"
     ], 
     "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
     "multi": True,
    "max_time": 30 
    },
    {"inject": "Decision 12 (10:30:00): ", "text": "What should Ground IV remind the EVAs?", 
        "options": [
            "A. Breathe frequently, do not sustain respiration", 
            "B. Pay attention to the temperature", 
            "C. Ensure the door is well closed", 
            "D. Keep monitoring EVA1 vital signals"
        ], "correct": "A. Breathe frequently, do not sustain respiration",
        "max_time": 30 }
]

# ---------------------------------------------- 13 to 20 ------------------------------------

decisions13to20 = {
    # Condition key: (answer from Decision 7, answer from Decision 12)
    ("A. Partial", "A. Breathe frequently, do not sustain respiration"):[ # without pneumothorax
        {
            "inject": "Decision 13 (10:50:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:15:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:25:00): ",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:25:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {
            "inject": "Decision 18 (11:25:00):",
            "text": "To understand the situation it’s important to establish the last known normal ???. What do you think it is?",
            "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"],
            "correct": "A. 10:16:00"
        },
        {
            "inject": "Decision 19 (11:55:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (11:55:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin","B. Control blood pressure and oxygen therapy for the stroke","C. Glucose"],
            "correct": "A. Aspirin"
        }
    ],      
    ("A. Partial", "B. Pay attention to the temperature"): [ # with pneumothorax
        {
            "inject": "Decision 13 (10:50:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:15:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:25:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:35:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options":["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:35:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:35:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:20:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:20:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("A. Partial", "C. Ensure the door is well closed"): [ # with pneumothorax
        {
            "inject": "Decision 13 (10:50:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:15:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:25:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:35:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:35:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:35:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:20:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:20:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals"): [ # with pneumothorax
        {
            "inject": "Decision 13 (10:50:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:15:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:25:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:35:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:35:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:35:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:20:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:20:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration"): [ #without pneumothorax
        {
            "inject": "Decision 13 (10:47:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:12:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:22:00): ",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:22:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {
            "inject": "Decision 18 (11:22:00):",
            "text": "To understand the situation it’s important to establish the last known normal ???. What do you think it is?",
            "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"],
            "correct": "A. 10:16:00"
        },
        {
            "inject": "Decision 19 (11:55:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (11:55:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin","B. Control blood pressure and oxygen therapy for the stroke","C. Glucose"],
            "correct": "A. Aspirin"
        }
    ],
    ("B. Normal", "B. Pay attention to the temperature"): [ #with pneumothorax
        {
            "inject": "Decision 13 (10:47:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:12:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:22:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:32:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:32:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:32:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:20:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:20:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("B. Normal", "C. Ensure the door is well closed"): [ # with pneumothorax
        {
            "inject": "Decision 13 (10:47:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:12:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:22:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:32:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:32:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:32:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:20:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:20:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals"): [ # with pneumothorax
        {
            "inject": "Decision 13 (10:47:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:12:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:22:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:32:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:32:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:32:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:20:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:20:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration"): [ #withou pneumothorax
        {
            "inject": "Decision 13 (10:37:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:02:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:12:00): ",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:12:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {
            "inject": "Decision 18 (11:12:00):",
            "text": "To understand the situation it’s important to establish the last known normal ???. What do you think it is?",
            "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"],
            "correct": "A. 10:16:00"
        },
        {
            "inject": "Decision 19 (11:42:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (11:42:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin","B. Control blood pressure and oxygen therapy for the stroke","C. Glucose"],
            "correct": "A. Aspirin"
        }
    ],
    ("C. Emergency", "B. Pay attention to the temperature"): [ #with pneumothorax
        {
            "inject": "Decision 13 (10:37:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:02:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:12:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:22:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:22:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:22:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:07:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:07:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("C. Emergency", "C. Ensure the door is well closed"): [ #with pneumothorax
        {
            "inject": "Decision 13 (10:37:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:02:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:12:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:22:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:22:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:22:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:07:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:07:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals"): [ # with pneumothorax
        {
            "inject": "Decision 13 (10:37:00):",
            "text": "What should the team do first?",
            "options": ["A. Take EVA 1 from the EMU suit","B. Take EVA 1 vitals","C. Take EVA 2 from the EMU suit","D. Give proper medication to EVA 1"],
            "correct": "B. Take EVA 1 vitals"
        },
        {
            "inject": "Decision 14 (11:02:00):",
            "text": "After EVA 1 is unsuited, How should they proceed?",
            "options": ["A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals","B. Commander take EVA 1 vitals while the Pilot unsuits EVA 2","C. Equip EVA 2 with monitoring medical equipment and take his vitals"],
            "correct": "A. Commander and Pilot restrain EVA 1 to the Crew Medical Restraint System (CMR) and take his vitals"
        },
        {
            "inject": "Decision 15 (11:12:00): ",
            "text": " EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 90%. What should be the next step?",
            "options": ["A. Provide oxygen (>28%) to EVA 1","B. Do other tests to understand what is going on","C. Glucose levels; Electrolyte levels"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {
            "inject": "Decision 16 (11:22:00):",
            "text": "EVA 1 Vital signs: BP 160/90; Temp 98.3; HR 118; RR 22; O2 Sat 95%. What should also be measured?",
            "options": ["A. Glucose levels; Electrolyte levels","B. Urinalysis; Chest radiograph","C. Toxicology; Lumbar Puncture"],
            "correct": "A. Glucose levels; Electrolyte levels"
        },
        {"inject": "Decision 17 (11:22:00):", 
            "role_specific": {
                "Commander": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "A.Perform NIH Stroke Scale"},
                "Pilot": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "B. Unsuit EVA 2"},
                "EVA2": {"text": "what should be done?", "options": ["A. figures"], "correct": "A. figures"},
                "MCC": {"text": "Meanwhile what should be also accessed?", "options": ["A.Perform NIH Stroke Scale","B. Unsuit EVA 2", "C.Review patient history"], "correct": "C.Review patient history"},
            }
        },
        {"inject": "Decision 18 (11:22:00):", 
            "role_specific": {
                "Commander": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct": "A. 10:16:00"},
                "Pilot": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
                "EVA2": {"text": "The persistent right chest pain and oxygen requirement of EVA 1 suggest necessary action. What should be done?", "options": ["A. EVA 2 goes grab the ultrasound equipment"], "correct": "A. EVA 2 goes grab the ultrasound equipment"},
                "MCC": {"text": "To understand the situation it’s important to establish the last known normal. What do you think it is?", "options": ["A. 10:16:00","B. 11:00:00","C. 12:00:00"], "correct":"A. 10:16:00"},
            }
        },
        {
            "inject": "Decision 19 (12:07:00):",
            "text": "EVA 1 Vital signs: BP 172/90; Temp 98.3°F/36.8°C; HR 118; RR 22; O2 Sat 95%; Glucose 145 mg/dL; Electrolytes: Na 132 mmol/L;K 4.2 mmol/L; Ca 8.5 mg/dL. NIHSS =11. According to the presentations, what is the most likely diagnosis?",
            "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia"],
            "correct": "A. Ischemic Stroke"
        },
        {
            "inject": "Decision 20 (12:07:00):",
            "text": "What’s the best course of treatment with the tools available?",
            "options": ["A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","C. Glucose for the stroke and observation for the pneumothorax"],
            "correct": "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
        }
    ],
    }

# ---------------------------------------------------- 21 to 24 --------------------------------------------------
decisions21to24 = {
    # Condition key: (answer from Decision 7, answer from Decision 12)
    ("A. Partial", "A. Breathe frequently, do not sustain respiration"):[
        {"inject": "Decision 21 (12:00:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:00:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:00:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:00:30 (Without Pneumothorax)
        {"inject": "Decision 22 (12:00:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:00:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:00:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:01:00 (Same for all roles)
        {"inject": "Decision 23 (12:01:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:01:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:01:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],      
    ("A. Partial", "B. Pay attention to the temperature"): [
        {"inject": "Decision 21 (12:25:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:25:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:25:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:26:00 (Same for all roles)
        {"inject": "Decision 23 (12:26:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:26:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:26:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("A. Partial", "C. Ensure the door is well closed"): [
        {"inject": "Decision 21 (12:25:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:25:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:25:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:26:00 (Same for all roles)
        {"inject": "Decision 23 (12:26:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:26:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:26:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals"): [
        {"inject": "Decision 21 (12:25:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:25:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:25:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:26:00 (Same for all roles)
        {"inject": "Decision 23 (12:26:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:26:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:26:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration"): [
        {"inject": "Decision 21 (12:00:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:00:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:00:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:00:30 (Without Pneumothorax)
        {"inject": "Decision 22 (12:00:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:00:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:00:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:01:00 (Same for all roles)
        {"inject": "Decision 23 (12:01:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:01:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:01:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "B. Pay attention to the temperature"): [
        {"inject": "Decision 21 (12:25:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:25:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:25:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:26:00 (Same for all roles)
        {"inject": "Decision 23 (12:26:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:26:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:26:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "C. Ensure the door is well closed"): [
        {"inject": "Decision 21 (12:25:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:25:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:25:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:26:00 (Same for all roles)
        {"inject": "Decision 23 (12:26:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:26:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:26:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals"): [
        {"inject": "Decision 21 (12:25:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 12:25:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:25:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:25:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 12:26:00 (Same for all roles)
        {"inject": "Decision 23 (12:26:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 12:26:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:26:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration"): [
        {"inject": "Decision 21 (11:47:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(11:47:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(11:47:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 11:47:30 (With Pneumothorax)
        {"inject": "Decision 22 (11:47:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(11:47:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(11:47:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 11:48:00 (Same for all roles)
        {"inject": "Decision 23 (11:48:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 11:48:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (11:48:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "B. Pay attention to the temperature"): [
        {"inject": "Decision 21 (12:12:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:12:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:12:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 11:47:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:12:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:12:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:12:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 11:48:00 (Same for all roles)
        {"inject": "Decision 23 (12:13:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 11:48:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:13:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "C. Ensure the door is well closed"): [
        {"inject": "Decision 21 (12:12:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:12:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:12:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 11:47:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:12:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:12:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:12:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 11:48:00 (Same for all roles)
        {"inject": "Decision 23 (12:13:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 11:48:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:13:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals"): [
        {"inject": "Decision 21 (12:12:00): ", 
        "role_specific": {
            "Commander": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:12:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:12:00) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "If the PDAM isn’t possible what should they do next?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 22 - 11:47:30 (With Pneumothorax)
        {"inject": "Decision 22 (12:12:30): ", 
        "role_specific": {
            "Commander": {"text": "What should you do first?", "options": ["A. Contact MCC"], "correct": "A. Contact MCC"},
            "Pilot": {"text": "(12:12:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "EVA2": {"text": "(12:12:30) Meanwhile, EVA 2 administers the treatment chosen to EVA 1."}, # No question, just text
            "MCC": {"text": "What should you do first?", "options": ["A. Call trauma specialist"], "correct": "A. Call trauma specialist"},
        }},
        
        # Decision 23 - 11:48:00 (Same for all roles)
        {"inject": "Decision 23 (12:13:00):", 
         "text": "What is the best way to transport EVA 1?",
         "options": ["A. Restrained to the CMR", "B. Take EVA 1 vitals", "C. Take EVA 2 from the EMU suit", "D. Give proper medication to EVA 1"],
         "correct": "A. Restrained to the CMR"},

        # Decision 24 - 11:48:00 (Same for all roles, multi-select)
        {"inject": "Decision 24 (12:13:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    }

# ----------------------------------------------- 25 to 27 -------------------------------------------------------------------------
#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)

decisions25to27 = {
    # Condition key: (answer from Decision 7, answer from Decision 12)
    ("A. Partial", "A. Breathe frequently, do not sustain respiration"):[

        {"inject": "Decision 25 (12:05:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:10:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:20:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:25:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],      
    ("A. Partial", "B. Pay attention to the temperature"): [
        {"inject": "Decision 25 (12:30:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:35:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:45:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:50:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("A. Partial", "C. Ensure the door is well closed"): [
        {"inject": "Decision 25 (12:30:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:35:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:45:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:50:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals"): [
        {"inject": "Decision 25 (12:30:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:35:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:45:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:50:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration"): [
        {"inject": "Decision 25 (12:05:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:10:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:20:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:25:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "B. Pay attention to the temperature"): [
        {"inject": "Decision 25 (12:30:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:35:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:45:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:50:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "C. Ensure the door is well closed"): [
        {"inject": "Decision 25 (12:30:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:35:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:45:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:50:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals"): [
        {"inject": "Decision 25 (12:30:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:35:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:45:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:50:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration"): [
        
        {"inject": "Decision 25 (11:52:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (11:57:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:07:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:12:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "B. Pay attention to the temperature"): [
        {"inject": "Decision 25 (12:17:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:22:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:32:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:37:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "C. Ensure the door is well closed"): [
        {"inject": "Decision 25 (12:17:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:22:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:32:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:37:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals"): [
        {"inject": "Decision 25 (12:17:00):", 
         "text": "Commander is bleeding from the injury. What should be done first?", 
         "options": ["A. Rapidly assess the bleeding","B. Get to the CRV", "C. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","D. Give him an injection of ..."], 
        },

        {"inject": "Decision 26 (12:22:00):", 
         "text": "Evaluation of the haemorrhage:"
            "Muscles involved: Rectus femoris muscle; Vastus laterallis and Iliotibial tract"
            "Vessels involved: superficial veins of the lower extremity. Commander is allert, anxious and breathing a bit fast. What should be done first", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },
        
        {"inject": "Decision 27 (12:32:00):", 
         "text": "The use of the tourniquet is enough to control the bleeding. What should you do next?", 
         "options": ["A. Cover the wound with gaze to avoid the spread of blood through the station and continue the journey to the CRV","B. Control the bleeding with the use of a Tourniquete", "C. Get to the CRV"], 
        },

        {"inject": "Decision 28 (12:37:00):", 
         "text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
    ],
    }
# ------------------------------------------------------- 28 to 29 ---------------------------------------------------------------------
# 20(A)
#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)
# 20(BvC)
#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)

# 20 (without pneumothorax)
#      "A. Aspirin"
#      "B. Control blood pressure and oxygen therapy for the stroke"
#      "C. Glucose"
# 20 (with pneumothorax)
#      "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
#      "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"
#      "C. Glucose for the stroke and observation for the pneumothorax"
decisions29to30 = {
# ----- 20 (A) ---------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "A. Aspirin"):[ # without pneumothorax
        {"inject": "Decision 29 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:40:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
        
    ],      
    ("A. Partial", "B. Pay attention to the temperature","A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, 
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },        
    ],
    ("A. Partial", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "A.Aspirin"): [ # without pneumothorax
        {"inject": "Decision 29 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:40:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "B. Pay attention to the temperature", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "A. Aspirin"): [ # without pneumothorax
        {"inject": "Decision 29 (12:17:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:27:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."}, # No question, just text
            "EVA2": {"text": "At this time, the improvement of EVA 1 presenting with less confusion and face paralysis is evident. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
# --- 20 (B)--------------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke"):[ # without pneumothorax
        {"inject": "Decision 29 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:40:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],      
    ("A. Partial", "B. Pay attention to the temperature","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("A. Partial", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke"): [ # without pneumothorax
        {"inject": "Decision 29 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:40:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "B. Pay attention to the temperature", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke"): [ # without pneumothorax
        {"inject": "Decision 29 (12:17:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:27:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
# --- 20 (C)--------------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "C. Glucose"):[ # without pneumothorax
        {"inject": "Decision 29 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:40:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],      
    ("A. Partial", "B. Pay attention to the temperature","C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("A. Partial", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "CCommander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "C. Glucose"): [ # without pneumothorax
        {"inject": "Decision 29 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:40:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "B. Pay attention to the temperature", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (13:05:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "C. Glucose"): [ # without pneumothorax
        {"inject": "Decision 29 (12:17:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets more confused and the face gets more paralysed. Would you change the course of treatment?", "options": ["A. Yes, to aspirin", "B. Yes, to control blood pressure and oxygen therapy for the stroke", "C. Yes, to Glucose","D. No"], "correct": "A. Yes, to aspirin"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:27:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax"): [ # with pneumothorax
        {"inject": "Decision 29 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "Pilot": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
            "EVA2": {"text": "At this time, EVA 1 gets worse losing consciousness. Would you change the course of treatment?", "options": ["A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. Yes, to control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax", "C. Yes, to glucose for the stroke and observation for the pneumothorax","D. No"], "correct": "A. Yes, to aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"},
            "MCC": {"text": "Pilot and MCC crew access the risk of collision and prepare to follow the protocol of collision."},
        }},
        {"inject": "Decision 30 (12:52:00):", 
         "text": " Independent from the possible collision event, should they return to earth due to the medical state of their colleagues?", 
         "options": ["A. Yes","B. No"], 
         "correct": "A. Yes"
        },
    ],
}

# ------------------------------------------------------- 31 to 37 ---------------------------------------------------------------------
# 29(A - yes)
# 20(A)
#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)
# 20(BvC)
#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)

# 29(B - No)
# 20(A)
#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)
# 20(BvC)
#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)

# 20 (without pneumothorax)
#      "A. Aspirin"
#      "B. Control blood pressure and oxygen therapy for the stroke"
#      "C. Glucose"
# 20 (with pneumothorax)
#      "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax"
#      "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax"
#      "C. Glucose for the stroke and observation for the pneumothorax"

decisions31to38 = {
#29(A - Yes)
# ----- 20 (A) ---------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "A. Aspirin","A. Yes"):[ # without pneumothorax
        {"inject": "Decision 31 (12:40:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:54:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (12:56:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],      
    ("A. Partial", "B. Pay attention to the temperature","A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "A. Aspirin", "A. Yes"): [ # without pneumothorax
        {"inject": "Decision 31 (12:40:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:54:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (12:56:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "B. Pay attention to the temperature", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "A. Aspirin", "A. Yes"): [ # without pneumothorax
        {"inject": "Decision 31 (12:27:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:41:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:06:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:06:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00):", 
         "text": "Do they need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 33 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:06:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
# --- 20 (B)--------------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke","A. Yes"):[ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],      
    ("A. Partial", "B. Pay attention to the temperature","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke","A. Yes"): [ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "B. Pay attention to the temperature", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke","A. Yes"): [ # without pneumothorax
        {"inject": "Decision 31 (12:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:37:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (12:47:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (12:57:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (12:59:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
# --- 20 (C)--------------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "C. Glucose","A. Yes"):[ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],      
    ("A. Partial", "B. Pay attention to the temperature","C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "C. Glucose","A. Yes"): [ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "B. Pay attention to the temperature", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "C. Glucose","A. Yes"): [ # without pneumothorax
        {"inject": "Decision 31 (12:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:37:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (12:47:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (12:57:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (12:59:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax","A. Yes"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do you need any more medical equipment for the travel?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],

#29(B - No)
# ----- 20 (A) ---------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "A. Aspirin","B. No"):[ # without pneumothorax
        {"inject": "Decision 31 (12:40:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need to treat the patients should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need to treat the patients should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:54:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (12:56:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],      
    ("A. Partial", "B. Pay attention to the temperature","A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "A. Aspirin", "B. No"): [ # without pneumothorax
        {"inject": "Decision 31 (12:40:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:43:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need to treat the patients should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need to treat the patients should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:54:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (12:56:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "B. Pay attention to the temperature", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (13:08:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:18:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:19:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:20:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "A. Aspirin", "B. No"): [ # without pneumothorax
        {"inject": "Decision 31 (12:27:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:30:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:41:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:06:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax", "B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:06:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "A. Aspirin for the stroke and initial oxygen therapy and observation for the minor pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00):", 
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 32 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 33 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "What much time do you think you have with the tourniquet before you have a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "What should the pilot do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:06:00): ", 
        "role_specific": {
            "Commander": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:07:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
# --- 20 (B)--------------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke","B. No"):[ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],      
    ("A. Partial", "B. Pay attention to the temperature","B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke","B. No"): [ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "B. Pay attention to the temperature", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "B. Control blood pressure and oxygen therapy for the stroke","B. No"): [ # without pneumothorax
        {"inject": "Decision 31 (12:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:37:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
        }},
        {"inject": "Decision 35 (12:47:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
        }},
        {"inject": "Decision 36 (12:57:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (12:59:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "B. Control blood pressure and oxygen therapy for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
# --- 20 (C)--------------
    ("A. Partial", "A. Breathe frequently, do not sustain respiration", "C. Glucose","B. No"):[ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],      
    ("A. Partial", "B. Pay attention to the temperature","C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("A. Partial", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "A. Breathe frequently, do not sustain respiration", "C. Glucose","B. No"): [ # without pneumothorax
        {"inject": "Decision 31 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:50:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:53:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:55:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (12:13:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "B. Pay attention to the temperature", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("B. Normal", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (13:05:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:20:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:23:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:25:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:42:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:43:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "A. Breathe frequently, do not sustain respiration", "C. Glucose","B. No"): [ # without pneumothorax
        {"inject": "Decision 31 (12:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " Although the confusion of the patient (EVA1), he is cooperating and the swallowing reflex is prevered. How would you administer the medication to this patient?", "options": ["A. Give the oral aspirin", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Give the oral aspirin"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (12:37:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (12:40:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (12:42:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
        }},
        {"inject": "Decision 35 (12:47:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision"},
        }},
        {"inject": "Decision 36 (12:57:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (12:59:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:00:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "B. Pay attention to the temperature", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "C. Ensure the door is well closed", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    ("C. Emergency", "D. Keep monitoring EVA1 vital signals", "C. Glucose for the stroke and observation for the pneumothorax","B. No"): [ # with pneumothorax
        {"inject": "Decision 31 (12:52:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
            "EVA2": {"text": " How would you administer the medication to an unconscious patient (EVA1)?", "options": ["A. Crush the aspirin, mix it with water and administer it through a nasogastric tube", "B. Trought a nasal canula", "C.Give the oral glucose"], "correct": "A. Crush the aspirin, mix it with water and administer it through a nasogastric tube"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV for a possible return to earth"},
        }},
        
        {"inject": "Decision 32 (13:07:00):",
         "text": "Do they need any more medical equipment to treat the patients inside the CRV?(maxim. 5)", 
         "options": [
            "A. Crew Medical Restraint System (CMR)", 
            "B. Emergency Medical Treatment Pack - Medications (Red) & Other components", 
            "C. Medical Diagnostic Pack (Blue)", 
            "D. Medical Supply Pack (Green)",
            "E. Minor Treatment Pack (Pink)", 
            "F. Oral Medication Pack (Purple)",
            "G. Physician Equipment Pack (Yellow)", 
            "H. Topical & Injectable Medication Pack - Medications (Brown)",
            "I. Convenience Medication Pack (White)", 
            "J. IV Supply Pack (Gray)", 
            "K. Advanced Life Support Pack (ALSP) & Other Componentes"
        ], 
        "correct": ["K. Advanced Life Support Pack (ALSP) & Other Componentes"],
        "multi": True
        },
        {"inject": "Decision 33 (13:10:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
            "EVA2": {"text": "If there was something that they need for the travel, should they get it?", "options": ["A. Yes", "B. No"], "correct": "A. Yes"},
            "MCC": {"text": "What should the you do?", "options": ["A. Close the hatch that separates the station from the CRV", "B. Help colleagues manage medical emergencies."], "correct": "A. Close the hatch that separates the station from the CRV"},
        }},
        {"inject": "Decision 34 (13:12:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "While the medication given to EVA1 is doing its work. EVA 2 can now assist the Commander, what should be done?", "options": ["A. Initiate fluid resuscitation", "Clean the wound"], "correct": "A. Initiate fluid resuscitation"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 35 (13:17:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
            "EVA2": {"text": "What time do you think the Commander has with the tourniquet before he has a higher risk of an ischemic event?", "options": ["A. < 2 hours", "B. < 1 hours"], "correct": "A. < 2 hours"},
            "MCC": {"text": "Pilot and MCC crew prepare the CRV and protocols needed for the possible collision."},
        }},
        {"inject": "Decision 36 (13:27:00): ", 
        "role_specific": {
            "Commander": {"text": "Although the physical imparement the Commander can participate in discussions"},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "The blood pressure of the Commander improves. What should be done?", "options": ["A. Assess the wound and prepare to close so they can take out the tourniquet", "B. Clean the wound"], "correct": "A. Assess the wound and prepare to close so they can take out the tourniquet"},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 37 (13:29:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "Pilot": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
            "EVA2": {"text": "EVA 1 stroke symptoms stabilized. Does he still need a hospital check-up?", "options": ["A. Yes, performing a CT scan is mandatory.", "B. No"], "correct": "A. Yes, performing a CT scan is mandatory."},
            "MCC": {"text": "Pilot and MCC crew assess the damage that the object may have caused"},
        }},
        {"inject": "Decision 38 (13:30:00): ", 
        "role_specific": {
            "Commander": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "Pilot": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
            "EVA2": {"text": "EVA 2 with the help of commander and flight surgeon proceeds with the suturing of the wound of commander."},
            "MCC": {"text": "The pilot and MCC crew receive a depressurization alert from the airlock. The alert specifies that is a slow depressurization, a small hole. Should the astronauts repair the damage?", "options": ["A. Yes", "B. No"], "correct": "B. No"},
        }},
    ],
    
}

#Without Pneumothorax: 1. 7(A)&12(A) + 7(B)&12(A) 2. 7(C)&12(A)
#With Pneumothorax: 1. 7(A)&12(BvCvD) + 7(B)&12(BvCvD) 2. 7(C)&12(BvCvD)

# ------------------------------------------- Functions to handle injects ------------------------------------------------------------
def get_answers_for_7_and_12():
    answer_7 = st.session_state.answers.get("Decision 7 (10:20:00): ", None)
    answer_12 = st.session_state.answers.get("Decision 12 (10:30:00): ", None)
    return answer_7, answer_12

def display_inject2():
    answer_7, answer_12 = get_answers_for_7_and_12()
    inject2_text = ""
    if answer_7 and answer_12:
        if answer_7 == "A. Partial" and answer_12 == "A. Breathe frequently, do not sustain respiration":
            inject2_text = "(10:40:00): The repressurization has finished successfully at 12 psi. EVA 1 shows signs of confusion."
        elif answer_7 == "A. Partial" and (answer_12 == "B. Pay attention to the temperature" or answer_12 == "C. Ensure the door is well closed" or answer_12 == "D. Keep monitoring EVA1 vital signals"):
            inject2_text = "(10:40:00): EVA 1 showed confusion due to breathing issues, now presenting sharp chest pain and shortness of breath."
        elif answer_7 == "B. Normal" and answer_12 == "A. Breathe frequently, do not sustain respiration":
            inject2_text = "(10:45:00): EVA 1 shows confusion and difficulty understanding what’s happening."
        elif answer_7 == "B. Normal" and (answer_12 == "B. Pay attention to the temperature" or answer_12 == "C. Ensure the door is well closed" or answer_12 == "D. Keep monitoring EVA1 vital signals"):
            inject2_text = "(10:45:00): EVA 1 shows confusion and shortness of breath due to lack of pressure adaptation."
        elif answer_7 == "C. Emergency" and answer_12 == "A. Breathe frequently, do not sustain respiration":
            inject2_text = "(10:35:00): EVA 1 has discomfort in ears and sinuses."
        elif answer_7 == "C. Emergency" and (answer_12 == "B. Pay attention to the temperature" or answer_12 == "C. Ensure the door is well closed" or answer_12 == "D. Keep monitoring EVA1 vital signals"):
            inject2_text = "(10:35:00): EVA 1 shows chest pain and shortness of breath due to confusion."
    return inject2_text
 

def get_inject3_time(answer7, answer12):
    """
    Returns a scenario-specific time string for Inject 3 based on:
      - answer7 => 'A. Partial', 'B. Normal', 'C. Emergency'
      - answer12 => 'A. Breathe frequently...' => no pneumothorax, else => with pneumothorax
    """
    no_pneumo = (answer12 == "A. Breathe frequently, do not sustain respiration")
    if no_pneumo:
        # Without Pneumothorax
        if answer7 in ["A. Partial", "B. Normal"]:
            return "12:00:00"   # 7(A)+12(A)&7(B)+12(A)
        elif answer7 == "C. Emergency":
            return "11:47:00"   # 7(C)+12(A)
        else:
            return "???"        # fallback
    else:
        # With Pneumothorax
        if answer7 in ["A. Partial", "B. Normal"]:
            return "12:25:00"   # 7(A)+12(BvCvD)&7(B)+12(BvCvD)
        elif answer7 == "C. Emergency":
            return "12:12:00"   # 7(C)+12(BvCvD)
        else:
            return "???"

# --------------------------------------------------------- Show Injects ----------------------------------------------------

def show_initial_situation():
    st.subheader("🚀 Initial Situation")  
    st.write("For the 17th day of the mission, an EVA is planned to install a component on a radiation collection device. "
    "  **EVA Crew:** EVA1 (Mission Specialist) & EVA2 (Flight Engineer) "
    " **Inside Crew:** Commander (CMO) & Pilot (IV Crew Member).")

def inject1():
    st.subheader("📌 Inject 1")
    st.write("2 hour into EVA (10:00:00 am)"
             "Sundendly EVA 1 reports numbness on his right arm as performing the task."
             "Note: The EVA’s aren’t close so they can’t see each other")

def inject2():
    st.subheader("📌 Inject 2")
    st.write(display_inject2())

def inject3():
    a7, a12 = get_answers_for_7_and_12()
    scenario_time = get_inject3_time(a7, a12)
    st.subheader(f"📌 Inject 3 - {scenario_time}")
    st.write("""
Days before there was a manoeuvre of the Lunar Gateway to avoid a possible collision with an object.
But the USSTRATCOM informs the MCC TOPO flight controller with a Conjunction Data Message
(time of closest approach, probability of collision, and miss distance). The object changed trajectory,
there’s a probability > 0.01% of collision. The CARA program changes the object’s label from yellow to red.
Possible collision within 1 hour. PDAM (Predetermined Debris Avoidance Maneuver) isn’t possible.
""")

def inject4():
    st.subheader("📌 Inject 4")
    st.write("During the relocation and transport of the patient and medical equipment, the Commander accidentally bumps into a protruding sharp edge on the gateway wall. This results in a deep, longitudinally oriented laceration on the medial side of the anterior portion of the right thigh. The cut extends from the proximal (closer to the hip) to the distal (closer to the knee) part of the thigh.")

def finish_questionnaire():
    st.success("✅ Thank you for completing the questionnaire!")

inject_stages = {0, 1, 3, 5, 7}
def is_inject_stage(stage):
    return stage in inject_stages

if is_inject_stage(st.session_state.stage):
    if st.session_state.stage == 0:
        show_initial_situation()
    elif st.session_state.stage == 1:
        inject1()
    elif st.session_state.stage == 3:
        inject2()
    elif st.session_state.stage == 5:
        inject3()
    elif st.session_state.stage == 7:
        inject4()

    if st.button("Next ➡"):
        st.session_state.stage += 1
        st.session_state.current_decision_index = 1 
        st.rerun()
    st.stop()

# ---------------------------------------------------------- Functions to handle decisions --------------------------------------------
def get_condition_key():
    answer_7 = st.session_state.answers.get("Decision 7 (10:20:00): ", None)
    answer_12 = st.session_state.answers.get("Decision 12 (10:30:00): ", None)
    return (answer_7, answer_12)

condition_key = get_condition_key()
D13to20 = decisions13to20.get(condition_key, [])
D21to24 = decisions21to24.get(condition_key, [])
D25to27 = decisions25to27.get(condition_key, [])

def get_decision_answer(decision_prefix):
    # Iterate over all keys in session_state.answers and return the first one that starts with the given prefix
    for key, value in st.session_state.answers.items():
        if key.startswith(decision_prefix):
            return value
    return None

def get_condition_key_for_decisions29to30():
    answer_7 = st.session_state.answers.get("Decision 7 (10:20:00): ", None)
    answer_12 = st.session_state.answers.get("Decision 12 (10:30:00): ", None)
    answer_20 = get_decision_answer("Decision 20")
    return (answer_7, answer_12, answer_20)

composite_key = get_condition_key_for_decisions29to30()
D29to30= decisions29to30.get(composite_key, [])

def get_condition_key_for_decisions31to38():
    answer_7 = st.session_state.answers.get("Decision 7 (10:20:00): ", None)
    answer_12 = st.session_state.answers.get("Decision 12 (10:30:00): ", None)
    answer_20 = get_decision_answer("Decision 20")
    answer_30 = get_decision_answer("Decision 30")
    return (answer_7, answer_12, answer_20, answer_30)

composite_key1 = get_condition_key_for_decisions31to38()
D31to38= decisions31to38.get(composite_key1, [])


def process_decisions(decision_list):
    """
    Loops over the given list of decision dictionaries,
    displays each decision, captures the answer, and returns a dictionary of answers.
    """
    answers = {}
    for idx, decision in enumerate(decision_list):
        if "role_specific" in decision:
            if role in decision["role_specific"]:
                qdata = decision["role_specific"][role]
            else:
                st.warning("No question for your role in this decision. Skipping...")
                continue
        else:
            qdata = decision

        st.subheader(f"{decision['inject']} {qdata.get('text', '')}")

        if qdata.get("multi", False):
            user_ans = st.multiselect("", qdata["options"], key=f"dec_{decision['inject']}")
            if not user_ans:
                st.error("Please select at least one option.")
                st.stop()
        else:
            placeholder = "-- Select an option --"
            radio_options = [placeholder] + qdata["options"]
            user_ans = st.radio("", radio_options, key=f"dec_{decision['inject']}")
            if user_ans == placeholder:
                st.error("Please select an option before continuing.")
                st.stop()

        answers[decision["inject"]] = user_ans
    return answers


def display_current_decision(decision_list):
    if not decision_list:
        st.info("No decisions available for this stage, skipping...")
        st.session_state.stage += 1
        st.session_state.current_decision_index = 1
        st.rerun()
    
    idx = st.session_state.current_decision_index - 1  
    if idx < 0 or idx >= len(decision_list):
        st.error("No decision available for this index.")
        st.stop()
    decision = decision_list[idx]
    
    # Initialize decision start time if not already set.
    if "decision_start_time" not in st.session_state:
        st.session_state.decision_start_time = time.time()
    
    if "role_specific" in decision:
        if role in decision["role_specific"]:
            qdata = decision["role_specific"][role]
        else:
            st.warning("No question for your role in this decision. Skipping...")
            return None
    else:
        qdata = decision

    # Retrieve the max time for this decision
    max_time = decision.get("max_time", 30)

    # Render the countdown timer on top
    unique_timer_id = f"timer_{idx}"
    timer_html = f"""
<div id="{unique_timer_id}" style="font-family: 'Georgia', serif; font-size: 24px; font-weight: bold; color: red; background-color: #F4F6F7; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 0px;"></div>
<script>
    var timeleft = {max_time};
    var timer = document.getElementById("{unique_timer_id}");
    function countdown() {{
        if(timeleft >= 0) {{
            timer.innerHTML = timeleft + " seconds remaining";
        }} else {{
            var extra_time = -timeleft;
            var penalty = 1 + 2 * Math.floor(extra_time / 10);
            timer.innerHTML = "You have exceeded the time limit. A penalty of " + penalty + " points will be applied.";
        }}
        timeleft -= 1;
        setTimeout(countdown, 1000);
    }}
    countdown();
</script>
"""
    st.components.v1.html(timer_html, height=80)

    # Now display the decision text below the timer.
    st.subheader(f"{decision['inject']} {qdata.get('text', '')}")

    unique_key = f"decision_{decision['inject']}_{idx}"
    
    if "options" in qdata:
        if qdata.get("multi", False):
            user_ans = st.multiselect("", qdata["options"], key=unique_key)
            if len(user_ans) > 5:
                st.error("You can select at most 5 options. Please remove extra selections.")
                st.stop()
            if not user_ans:
                st.error("Please select at least one option before continuing.")
                st.stop()
        else:
            placeholder = "-- Select an option --"
            radio_options = [placeholder] + qdata["options"]
            user_ans = st.radio("", radio_options, key=unique_key)
            if user_ans == placeholder:
                st.error("Please select an option before continuing.")
                st.stop()
    else:
        st.info("No response required for this message.")
        user_ans = qdata.get("text", "")
    
    # Save the answer using the decision inject as the key.
    st.session_state.answers[decision["inject"]] = user_ans

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            if st.session_state.current_decision_index > 1:
                st.session_state.current_decision_index -= 1
                st.rerun()
    with col2:
        if st.button("Next ➡"):
            elapsed = time.time() - st.session_state.decision_start_time
            penalty = 0
            if elapsed > max_time:
                extra_time = elapsed - max_time
                penalty = 2 * (extra_time // 5)
                st.warning(f"You have exceeded the time limit. A penalty of {penalty} points will be applied.")
            
            # Reset the start time for the next decision.
            st.session_state.decision_start_time = time.time()
            
            if st.session_state.current_decision_index == len(decision_list):
                st.session_state.current_decision_index = 1
                st.session_state.stage += 1
            else:
                st.session_state.current_decision_index += 1
            st.rerun()



# --------------------------------------------------- Show decisions-----------------------------------------------------

if st.session_state.stage == 2:
    display_current_decision(decisions1to12)
elif st.session_state.stage == 4:
    display_current_decision(D13to20)
elif st.session_state.stage == 6:
    display_current_decision(D21to24)
elif st.session_state.stage == 8:
    display_current_decision(D25to27)
elif st.session_state.stage == 9:
    display_current_decision(D29to30)
elif st.session_state.stage == 10:
    display_current_decision(D31to38)
elif st.session_state.stage == 11:
    finish_questionnaire()
    st.stop()
else:
    st.error("Unexpected stage!")
    st.stop()

# -------------------------------------------------------- Saving Answers to DB ---------------------------------------------------
def get_correct_answer(decision_inject):
    all_decision_lists = [
        decisions1to12,
        decisions13to20,
        decisions21to24,
        decisions25to27,
        decisions29to30,
        decisions31to38,
    ]
    for decision_list in all_decision_lists:
        # If decision_list is a dict, iterate over its values (which are lists)
        if isinstance(decision_list, dict):
            iter_list = []
            for value in decision_list.values():
                iter_list.extend(value)
        else:
            iter_list = decision_list

        for decision in iter_list:
            if decision.get("inject", "").strip() == decision_inject.strip():
                if "role_specific" in decision:
                    if role in decision["role_specific"]:
                        return decision["role_specific"][role].get("correct", "")
                    else:
                        return decision.get("correct", "")
                else:
                    return decision.get("correct", "")
    return ""


if st.session_state.stage ==11:
    for decision_inject, answer in st.session_state.answers.items():
        correct_answer = get_correct_answer(decision_inject)
        score = 1 if answer == correct_answer else 0
        cursor.execute(
            "INSERT INTO quiz_results (role, inject, question, answer, correct_answer, score) VALUES (?, ?, ?, ?, ?, ?)",
            (role, decision_inject, "", str(answer), str(correct_answer), score)
        )
conn.commit()
conn.close()
