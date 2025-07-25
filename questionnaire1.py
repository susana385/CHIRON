import streamlit as st
import time
from supabase_client import supabase

GRACE_SECONDS = 60


# ─────────────────────────────────────────────

roles = {
    "FE-3 (EVA2)": "Flight Engineer - Outside performing EVA.",
    "Commander (CMO,IV2)": "Crew Medical Officer (CMO) - Inside the station monitoring EVA",
    "FE-1 (EVA1)": "Flight Engineer - Outside performing EVA.",
    "FE-2 (IV1)": "Flight Engineer - Inside the station monotoring EVA",
    "FD":"Flight Director: Director of Mission Control Operations",
    "FS":"Flight Surgeon: Responsible for the health of the astronauts",
    "BME":"Biomedical Engineer: Support to the flight surgeon and responsible for medical equipment on the station",
    "CAPCOM":"Astronaut on the Mission Control Center responsible for the direct comunications with the astronauts in the station",
}

# Base decision template for repetitions
base_decision = {
    'inject': '',
    'text': '',
    'options': [],
    'scores': [],
    'max_time': 300,
}

# ----------------------------------------------------- 1 to 12 --------------------------------------

decisions1to15 = [
    {"inject": "Decision 1 (9:50:00): ",
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2 (IV1)": {"text": " Keep the normal activities going."},
            "FE-1 (EVA1)": {"text": " Keep the normal activities going."},
            "FE-3 (EVA2)": {"text": " Keep the normal activities going."},
            "FD": {"text": "During an EVA and after a blackout period, what should you do?", "options":["A. Through CAPCOM, check how things are going with the EVs during the fixation of the new component for the new radiation study.","B. Wait for the astronauts to report any issues.", "C. Check if the communications are back on.", "D. Check with the rest of the MCC about the scheduled work."],
    "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FS": {"text": " Keep the normal activities going."},
            "BME": {"text": " Keep the normal activities going." },
            "CAPCOM": {"text": "During an EVA and after a blackout period, what to you do?", "options":["A. Check how things are going with the EVs during the fixation of the new component for the new radiation study.","B. Wait for the astronauts to report any issues.", "C. Check if the communications are back on.", "D. Check with the rest of the MCC about the scheduled work."],
    "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
        } },

    {"inject": "Decision 2 (9:55:00): ",
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Report your positive status only when CAPCOM asks."},
            "FE-2 (IV1)": {"text": "Report your positive status only when CAPCOM asks "},
            "FE-1 (EVA1)": {"text": "You are now starting the fixation of the new component of data collection to the station. Communicate what you’re doing only when asked by the CAPCOM."},
            "FE-3 (EVA2)": {"text": "You are now on a different location than FE-1(EV1), checking on the status of other colection device. Report the positive status of this device only when asked by the CAPCOM."},
            "FD": {"text": "With the information provided by CAPCOM, what’s the next step?", "options": ["A. Stop the activities in the EVA to understand the current situation.","B. Continue with normal activities.", "C. Check if the communications are back on.", "D. Check with the rest of the MCC about the scheduled work."],
    "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300 },
            "FS": {"text": "With the information provided by CAPCOM to the you, what’s the next step?", "options": ["A. Ask, through CAPCOM, for the flight director to order a to stop the activities in the EVA to perform a medical assessment","B. Continue with normal activities.","C. Check if the communications are back on.", "D. Check with the rest of the MCC about the scheduled work."],
    "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300 },
            "BME": {"text": "With the information provided by CAPCOM to the Flight Surgeon, what’s the next step?", "options": ["A. Ask, through CAPCOM, for the flight director to order a to stop the activities in the EVA to perform a medical assessment","B. Continue with normal activities.","C. Check if the communications are back on.", "D. Check with the rest of the MCC about the scheduled work."],
    "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 30},
            "CAPCOM": {"text": "Check how are the things are going with the all astronauts during the fixation of the new component for the new radiation study. Report the status back to the flight director and flight surgeon."},
        } },

     {"inject": "Decision 3 (10:00:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "Keep the normal activities going."},
            "FE-2 (IV1)": {"text": "Keep the normal activities going."},
            "FE-1 (EVA1)": {"text": "2 hour into EVA, sundendly you feel numbness on your right arm while performing a vigurous task with that arm. What should you do?", "options": ["A. Communicate with CAPCOM to report what you fell.","B. Initiate return to the crew lock while continuing to communicate with MCC.","C. Check for suit malfunctions before making any further decisions.","D. Communicate with Commander in the station to report what you fell."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300 },
            "FE-3 (EVA2)": {"text": " Keep the normal activities going."},
            "FD": {"text": " Keep the normal activities going."},
            "FS": {"text": " Keep the normal activities going." },
            "BME": {"text": " Keep the normal activities going."},
            "CAPCOM": {"text": " Keep the normal activities going."},
        }
    },

    {"inject": "Decision 4 (10:00:30): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2 (IV1)": {"text": " Keep the normal activities going."},
            "FE-1 (EVA1)": {"text": "Report to CAPCOM the numbness in your right arm."},
            "FE-3 (EVA2)": {"text": " Keep the normal activities going."},
            "FD": {"text": "Keep the normal activities going."},
            "FS": {"text": " Keep the normal activities going."},
            "BME": {"text": " Keep the normal activities going."},
            "CAPCOM": {"text": "You are in communication with FE-1(EV1). With the information he provided, what should you do?", "options": ["A. Communicate the situation to the flight director and transfer communication to the Flight Surgeon. A private consultation with EVA-1 is recommended.","B. Instruct FE-1(EV1) to initiate the return to the crew lock.","C. FE-1(EV1) should check for suit malfunctions before making any further decisions.","D. Communicate with the Commander at the station to report what FE-1(EV1) feels."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
        }
    },

    {"inject": "Decision 5 (10:01:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2 (IV1)": {"text": " Keep the normal activities going."},
            "FE-1 (EVA1)": {"text": "You’re now in a private consultation with the flight surgeon. Meanwhile, you report that the numbness could be from the strenuous work you were performing with that arm."},
            "FE-3 (EVA2)": {"text": "Keep the normal activities going."},
            "FD": {"text": "Keep the normal activities going."},
            "FS": {"text": "You’re now in a private consult with FE-1(EV1). After gathering more information about the situation. What do you think should be suggested?", "options": ["A. Instruct FE-1(EV1) to stop his work for 15 minutes. Rest in the anatomical reference position to see if the symptoms disappear.","B. Instruct FE-1(EV1) to initiate the return to the crew lock.","C. Instruct FE-1(EV1) to stop his work and check for suit malfunctions.","D. Instruct FE-2(IV1) to suit up and go pick up FE-1(EV1)."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": " Keep the normal activities going."},
            "CAPCOM": {"text": " Establish a private consultation between FE-1(EV1) and the flight surgeon. Report the situation to the flight director and the IV astronauts."},
        }
    },

    {"inject": "Decision 6 (10:16:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2 (IV1)": {"text": " Keep the normal activities going."},
            "FE-1 (EVA1)": {"text": "After 15 min, the symptoms worsen, now you notice weakness in your right arm. You’re still in the private consultation with the fligh surgeon please report it."},
            "FE-3 (EVA2)": {"text": " Keep the normal activities going."},
            "FD": {"text": " Keep the normal activities going."},
            "FS": {"text": "With the information reported by FE-1(EV1). What is the best option?", "options": ["A. You should report the situation to CAPCOM as a possible medical emergency.","B. Wait to see if the symptoms go away.","C. You should report the situation to CAPCOM and proceed with normal activities.","D. You should report the situation to BME."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": " Keep the normal activities going."},
        }
    },

    {"inject": "Decision 7 (10:17:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2 (IV1)": {"text": " Keep the normal activities going."},
            "FE-1 (EVA1)": {"text": "Wait for more instructions."},
            "FE-3 (EVA2)": {"text": " Keep the normal activities going."},
            "FD": {"text": "Receiving the information from  the flight surgeon and knowing that the two EVAS aren’t next to each other. What should be done?", "options": ["A. Instruct EVA2 to meet EVA1 to provide him with any assistance, even though this deslocation could take up to 20 minutes.","B. Instruct FE-3(EV2) to initiate the return to the crew lock.","C. Instruct FE-1(EV1) to initiate the return to the crew lock.","D. Ask another astronaut (still inside) to start preparing to come as EVA3 and pick EVA1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FS": {"text": "Report the situation to the CAPCOM as a possible medical emergency. In discussion with BME, what should be reported?", "options": ["A. Confirm that this is a possible medical emergency and call for a trauma medical specialist. Meanwhile, BME monitors FE-1(EV1) vital signs.","B. Ask EVA1 to continue with the mission tasks and monitor the symptoms for the next 30 minutes.","C. Instruct EVA2 to take over EVA1’s tasks while EVA1 rests inside the airlock. No need to report yet unless the condition worsens.","D. Attribute the symptoms to suit fatigue and recommend hydration and deep breathing exercises before continuing. Meanwhile, BME monitors FE-1(EV1) vital signs."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "Report the situation to the CAPCOM as a possible medical emergency. In discussion with FS, what should be reported?", "options": ["A. Confirm that this is a possible medical emergency and call for a trauma medical specialist. Meanwhile, BME monitors FE-1(EV1) vital signs.","B. Ask EVA1 to continue with the mission tasks and monitor the symptoms for the next 30 minutes.","C. Instruct EVA2 to take over EVA1’s tasks while EVA1 rests inside the airlock. No need to report yet unless the condition worsens.","D. Attribute the symptoms to suit fatigue and recommend hydration and deep breathing exercises before continuing. Meanwhile, BME monitors FE-1(EV1) vital signs."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "CAPCOM": {"text": "Report the situation to the flight director."},
        }
    },

    {"inject": "Decision 8 (10:18:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-2 (IV1)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-1 (EVA1)": {"text": "Wait for more instructions."},
            "FE-3 (EVA2)": {"text": "Wait for instructions."},
            "FD": {"text": " Monitor the situation and assist with anything that the rest of the team might need."},
            "FS": {"text": "What can be done at this stage to help narrow down or confirm a diagnosis for EVA1’s condition?", "options": ["A. Instruct FE-3(EV2) to perform the FAST method; Assess the 6 P’s (pain, pallor, pulselessness, perishingly cold, paraesthesia and paralysis); Monitor for headache severity and photophobia on FE-1(EV1).","B. Instruct FE-3(EV2) to assess orthostatic vital signs; Perform a neurological exam focused on awareness and responsiveness; Monitor for emotional triggers or psychological stressors; Rule out dehydration or hypoxia; on FE-1(EV1).","C. Instruct FE-3(EV2) to perform a basic cognitive and coordination test; Assess for confusion, gait disturbances, or eye movement issues; Check for nutritional deficiencies; Conduct vestibular function tests (if feasible in-mission) on FE-1(EV1).","D.Instruct FE-3(EV2) to repeat FAST over time to evaluate symptom progression; Observe for recurrence or resolution of symptoms; Inspect for isolated facial nerve involvement; Conduct environmental checks; Screen for history of migraines or visual disturbances on FE-1(EV1)."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Instruct FE-3(EV2) to meet FE-1(EV1) to provide him with any assistance."},
        }
    },

    {"inject": "Decision 9 (10:38:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-2 (IV1)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-1 (EVA1)": {"text": "You notice that you can’t feel the right part of you’re face, which makes it difficult to speak."},
            "FE-3 (EVA2)": {"text": "After 20 minutes, you get close to FE-1(EV1) and notice that he is presenting some facial asymmetry, specifically drooping on the right side of the face. You perform the FAST method with positive results; Report this information to CAPCOM. "},
            "FD": {"text": " Receiving information from CAPCOM. In this situation, what’s the best option?", "options": ["A. Abort EVA, instructing the EVs to return to the crew lock and the IVs to prepare the crew lock for repressurization. The return will take at least 15min.","B. Don't abort the EVA yet. Wait to get a better understanding of the situation.","C. Instruct FE-3(EV2) to enter the airlock first to begin repressurization preparation while FE-1(EV1) follows at their own pace.","D. Initiate full depressurisation of the airlock while FE-1(EV1) is still en route to save time."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FS": {"text": "Meanwhile, during communication, you notice that EVA1 is having difficulty speaking clearly. What should be done?", "options": ["A. Communicate with FE-3(EV2) to understand what is happening. With this information it’s possible to understand the result of the FAST method.","B. Wait until EVA1’s speech improves to avoid unnecessary panic or false alarms.","C. Tell EVA1 to hydrate and rest briefly, then retry communication.","D. Ask CAPCOM to re-establish comms in case the distortion is due to a technical glitch."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "You receive some more informationaboutf the situation from FE-3(EV2). What should you do?", "options": ["A. Establish communication between the Flight Surgeon and FE-3(EV2) and report the situation to the flight director.","B. Ask EVA1 to perform basic speech and motor tests to confirm if it’s truly a neurological issue.","C. Instruct  FE-3(EV2) to keep monitoring EVA1 for further symptoms and wait to see if the condition progresses.","D. Report the situation directly to the Flight Director and include the Flight Surgeon in the loop."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
    ],"max_time": 300},
        }
    },

    {"inject": "Decision 10 (10:39:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "Upon receiving the orders from CAPCOM and in discussion with FE-2(IV1), what technical procedures must be prioritised to ensure a safe and efficient re-entry to the airlock during this contingency?", "options": ["A. Ensure suit telemetry is stable, initiate translation path clearance, verify airlock integrity, and coordinate repress sequence timing with MCC.","B. Switch EVA1’s suit to full manual mode to reduce data traffic and speed up the airlock cycle.","C. Instruct EVA2 to enter the airlock first to begin repressurization prep while EVA1 follows at their own pace.","D. Initiate full depressurisation of the airlock while EVA1 is still en route to save time."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2 (IV1)": {"text": "Upon receiving the orders from CAPCOM and in discussion with the Commander, what technical procedures must be prioritised to ensure a safe and efficient re-entry to the airlock during this contingency?", "options": ["A. Ensure suit telemetry is stable, initiate translation path clearance, verify airlock integrity, and coordinate repress sequence timing with MCC.","B. Switch EVA1’s suit to full manual mode to reduce data traffic and speed up the airlock cycle.","C. Instruct EVA2 to enter the airlock first to begin repressurization prep while EVA1 follows at their own pace.","D. Initiate full depressurisation of the airlock while EVA1 is still en route to save time."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "Receiving information from the CAPCOM, You are now escorting EVA1 back to the airlock. What is the most effective way to support EVA1 during this phase?", "options": ["A. Maintain physical proximity, monitor EVA1’s mobility and responsiveness, and provide verbal reassurance while relaying updates to CAPCOM.","B. Minimize communication to reduce stress and interference with MCC telemetry.","C. Leave EVA1 briefly to speed up airlock prep steps from outside.","D. Focus on finishing any remaining mission objectives while EVA1 proceeds slowly toward the airlock."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FD": {"text": "Communicate with CAPCOM to abort EVA, instructing the EVs to return to the crew lock and the IVs to prepare the crew lock for repressurization."},
            "FS": {"text": "The medical team of the MCC discuss the possible diagnosis. What can be happening with EVA 1?", "options": ["A. Stroke; Acute upper limb ischemia; subarachnoid hemorrhage; hypoglycemia; Meningitis/encephalitis.","B. Syncope; Conversion disorder.","C. Wernicke’s encephalopathy; Ménièrés disease","D. Transient ischemic attack (TIA); Bell’s palsy; Migraine with aura; Carbon monoxide exposure."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "The medical team of the MCC discuss the possible diagnosis. What can be happening with EVA 1?", "options": ["A. Stroke; Acute upper limb ischemia; subarachnoid hemorrhage; hypoglycemia; Meningitis/encephalitis.","B. Syncope; Conversion disorder.","C. Wernicke’s encephalopathy; Ménièrés disease","D. Transient ischemic attack (TIA); Bell’s palsy; Migraine with aura; Carbon monoxide exposure."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "CAPCOM": {"text": "Communicate with COMMANDER (IV2) and FE-2(IV1) to abort EVA, instructing the EVs to return to the crew lock and the IVs to prepare the crew lock for repressurization."},
        }
    },

    {"inject": "Decision 11 (10:40:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Keep preparing for the reentry of the EVs."},
            "FE-2 (IV1)": {"text": " Keep preparing for the reentry of the EVs."},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "How should you transport FE-1(EV1) to the crew lock?", "options": ["A. Tow EVA1 using a tether."," B. Carry EVA1 using the SAFER unit."," C. EVA1 should self-rescue using their propulsion system."," D. Assist EVA1 into the MMSEV (Miniature Modular Space Exploration Vehicle)."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #D
    ],"max_time": 300},
            "FD": {"text": " Keep preparing for the reentry of the EVs."},
            "FS": {"text": "In these possible diagnosis, where should the medical assistance be performed?", "options": ["A. Near the Airlock, where the Crew Medical Restraint System is possible to fixate;","B. Near where all the medical equipment is;","C. Outside the station","D. One needs to wait to leave the airlock."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Keep preparing for the reentry of the EVs."},
        }
    },

    {"inject": "Decision 12 (10:41:00): ", 
    "text": "The repressurization of the crew lock can take up to 15 min. Given the circumstances, how should the pressurisation of the crew lock be conducted?", "options": ["A.Partial pressurisation finishing at 12 psi (~10 min.)","B.Normal repressurization (~15 min.)","C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)"],
    "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
    ],"max_time": 300  
    },
    
    {"inject": "Decision 13 (10:42:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "While the EVs are returning, what should you and FE-2(IV1) do to prepare for their arrival?", "options": ["A. The Commander can confirm the medical emergency protocols with the Flight Surgeon; Flight Engineer 2 can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed","B. The commander  and Flight Engineer 2 can initiate a full cabin depressurisation to speed up EVA2’s reentry.","C. The Flight Engineer 2 can leave the airlock hatch open and wait to pull the patient in manually; the Commander gathers information about the medical emergency","D. The crew can begin unrelated maintenance tasks to stay on schedule."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2 (IV1)": {"text": "While the EVs are returning, what should you and the Commander do to prepare for their arrival?", "options": ["A. The Commander can confirm the medical emergency protocols with the Flight Surgeon; Flight Engineer 2 can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed","B. The commander  and Flight Engineer 2 can initiate a full cabin depressurisation to speed up EVA2’s reentry.","C. The Flight Engineer 2 can leave the airlock hatch open and wait to pull the patient in manually; the Commander gathers information about the medical emergency","D. The crew can begin unrelated maintenance tasks to stay on schedule."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "If asked the last known normal of the FE-1(EV1) state was 10:16:00"},
            "FD": {"text": "Communicate with CAPCOM the type of repressurization that will be performed."},
            "FS": {"text": "To understand the situation, it’s important to establish the last known normal (the last time when EVA1 was well, not presenting symptoms) . What do you think it is?", "options": ["A. 10:16:00 from then, they have 60 minutes to administer the medication to have the best possible outcome.","B. 10:50:00  from then, they have 20 minutes to administer the medication to have the best possible outcome.","C. 11:16:00  from then, they have 30 minutes to administer the medication to have the best possible outcome.","D. 11:02:00  from then, they have 50 minutes to administer the medication to have the best possible outcome."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Report the information given by the FD to the astronauts."},
        }
    },


    {"inject": "Decision 14 (10:45:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text":"Start preparing for the crew lock for repressurization."},
            "FE-2 (IV1)": {"text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "You’re almost arriving to the Airlock."},
            "FD": {"text": "Start preparing for the crew lock for repressurization."},
            "FS": {"text": "Give assistance to the IVs inside the station."},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Start preparing for the crew lock for repressurization"},
        }
    },

    {"inject": "Decision 15 (10:46:00): ", 
    "text": "TEVs arrive at the crew lock. Due to the high-stress environment, it’s crucial that CAPCOM reminds EVAs of an important step in their training.", "options": ["A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration.","B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock..","C. Instruct CAPCOM to remind the EVs to make sure the door is well closed.","D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals."],
    "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
    ],"max_time": 300  
    }, 
    
]

decision16_12A=[

    {"inject": "Decision 16 (10:58:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "At 10:58 AM, you find that the hatch between the crew lock and the station cannot be opened because the pressure readings differ between the two locks. Communicate the situation with the MCC."},
            "FE-2 (IV1)": {"text": "At 10:58 AM, you find that the hatch between the crew lock and the station cannot be opened because the pressure readings differ between the two locks. Communicate the situation with the MCC."},
            "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3 (EVA2)": {"text": "Wait for the repressurization to be completed. Keep monitoring EV1"},
            "FD": {"text": " Given the information from the CAPCOM. What should be the Flight Director’s primary focus to resolve the issue?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #D
    ],"max_time": 300},
            "FS": {"text": "Monitor FE-1(EV1) vital signs."},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Report the information given by the IVs"},
        }
    }
]

decisions17to18_12B=[

    {"inject": "Decision 17 (11:01:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2 (IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
            "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
            "FS": {"text": "Monitor FE-1(EV1) vital signs."},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Report the information given by the IVs."},
        }
    },

    {"inject": "Decision 18 (11:02:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2 (IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
            "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
            "FS": {"text": "What coordinated assessment could you do with the BME perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "What coordinated assessment could you do with the Flight Surgeon perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "CAPCOM": {"text": "Report the status of the station to the rest of the MCC."},
        }
    }
]

decisions17to19_12C=[

    {"inject": "Decision 17 (10:51:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2 (IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
            "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
            "FS": {"text": "Monitor FE-1(EV1) vital signs."},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Report the information given by the IVs."},
        }
    },

    {"inject": "Decision 18 (10:52:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2 (IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
            "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
            "FS": {"text": "What coordinated assessment could you do with the BME perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "BME": {"text": "What coordinated assessment could you do with the Flight Surgeon perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "CAPCOM": {"text": "Report the status of the station to the rest of the MCC."},
        }
    },

    {"inject": "Decision 19 (11:01:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text": " Wait for more information"},
            "FE-2 (IV1)": {"text": " Wait for more information"},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
            "FD": {"text": " Wait for more information."},
            "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "BME": {"text": "In discussion with the flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
        }
    }
]



# ---------------------------------------------- 17 to 26 ------------------------------------
#"A.Partial pressurisation finishing at 12 psi (~10 min.)","B.Normal repressurization (~15 min.)","C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min) pressurisation at a rate of 1.0 psi/second (~5 min) "
decisions17to26={
    # Condition key: (answer from Decision 12, answer from Decision 15)
    ("A.Partial pressurisation finishing at 12 psi (~10 min.)", "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration."):[ # without pneumothorax
        
            {"inject": "Decision 17 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "What coordinated assessment could you do with the BME perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "What coordinated assessment could you do with the Flight Surgeon perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the status of the station to the rest of the MCC."},
            }
        },

        {"inject": "Decision 19 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System and measure vital signs, perform neurological evaluation, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System and measure vital signs, perform neurological evaluation, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:20:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:21:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 23 (11:30:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:40:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2 (IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FD": {"text": "Receive information from CAPCOM."},
            "FS": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with BME what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "BME": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with the Flight Surgeon what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "CAPCOM": {"text": "Communicate FS orders to Commander and FD "},
        }
    },


        {"inject": "Decision 25 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },



    ],      
    ("A.Partial pressurisation finishing at 12 psi (~10 min.)", "B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock."): [ # with pneumothorax
        
        {"inject": "Decision 17 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "What coordinated assessment could you do with the BME perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "What coordinated assessment could you do with the Flight Surgeon perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the status of the station to the rest of the MCC."},
            }
        },

        {"inject": "Decision 19 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:20:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:21:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:22:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:32:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    ("A.Partial pressurisation finishing at 12 psi (~10 min.)", "C. Instruct CAPCOM to remind the EVs to make sure the door is well closed."): [ # with pneumothorax
        {"inject": "Decision 17 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "What coordinated assessment could you do with the BME perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "What coordinated assessment could you do with the Flight Surgeon perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the status of the station to the rest of the MCC."},
            }
        },

        {"inject": "Decision 19 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:20:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:21:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:22:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:32:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    
    ("A.Partial pressurisation finishing at 12 psi (~10 min.)", "D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals."): [ # with pneumothorax
        {"inject": "Decision 17 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2 (IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "What coordinated assessment could you do with the BME perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "What coordinated assessment could you do with the Flight Surgeon perform during hatch opening and suit doffing?", "options": ["A. Wait to see the vital signs data.","B. Rely solely on the telemetry data provided by the suit sensors, assuming that clinical symptoms will resolve once environmental pressures are equalised.","C. Conduct a evaluation of the telemetry data displayed.","D. Instruct EVA1 to self-monitor his condition while the BME temporarily disables any conflicting sensor readings to avoid false alarms."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the status of the station to the rest of the MCC."},
            }
        },

        {"inject": "Decision 19 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:20:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:21:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:22:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:32:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],

# B ----------
    ("B.Normal repressurization (~15 min.)", "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration."): [ #without pneumothorax
        

        {"inject": "Decision 19 (11:10:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System and measure vital signs, perform neurological evaluation, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System and measure vital signs, perform neurological evaluation, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:16:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 23 (11:25:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:35:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2 (IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FD": {"text": "Receive information from CAPCOM."},
            "FS": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with BME what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "BME": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with the Flight Surgeon what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "CAPCOM": {"text": "Communicate FS orders to Commander and FD "},
        }
    },


        {"inject": "Decision 25 (11:40:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2 (IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FD": {"text": "Receive information from the CAPCOM and assist in the decisions"},
                "FS": {"text": "Instruct, through CAPCOM, that the astronauts need to take the following medical kits inside CRV: B. Emergency Medical Treatment Pack - Medications (Red) & Other components; F. Oral Medication Pack (Purple); G. Physician Equipment Pack (Yellow);K. Advanced Life Support Pack (ALSP)"},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate the orders to the astronauts and FD."},
            }
        },

        {"inject": "Decision 26 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Establish CRV communications with MCC, close the hatches, verify opportunity windows for undocking, check propulsion systems, perform delta‑V calculations for orbital manoeuvring, assess propellant requirements (if necessary), and don the IV spacesuits.","B. Establish CRV communications with MCC, check propulsion systems, close the hatches, perform delta‑V calculations for orbital manoeuvring, verify opportunity windows for undocking, assess propellant requirements (if necessary), and don the IV spacesuits.","C. Verify opportunity windows for undocking, close the hatches, check propulsion systems, establish CRV communications with MCC, perform delta‑V calculations for orbital manoeuvring, don the IV spacesuits, and assess propellant requirements (if necessary).","D.Don the IV spacesuits, assess propellant requirements (if necessary), perform delta‑V calculations for orbital manoeuvring, check propulsion systems, establish CRV communications with MCC, verify opportunity windows for undocking, and finally close the hatches."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    ("B.Normal repressurization (~15 min.)", "B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock."): [ #with pneumothorax
        
        {"inject": "Decision 19 (11:10:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:16:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:17:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:26:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    ("B.Normal repressurization (~15 min.)", "C. Instruct CAPCOM to remind the EVs to make sure the door is well closed."): [ # with pneumothorax
        {"inject": "Decision 19 (11:10:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:16:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:17:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:26:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    ("B.Normal repressurization (~15 min.)", "D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals."): [ # with pneumothorax
        {"inject": "Decision 19 (11:10:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " Wait for more information"},
                "FE-2 (IV1)": {"text": " Wait for more information"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": " Wait for more information."},
                "FS": {"text": "In discussion with BME and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and without any telemetry data, which immediate action should be prioritised right after the doffing of FE-1(EV1)? Communicate your decision to the MCC", "options": ["A. Instruct IVs to perform a basic vital signs check (heart rate, blood pressure, and oxygen saturation), then resume concurrent tasks.","B. Instruct IVs to restrain FE-1(EV1) to the Crew Medical Restraint System, measure vital signs, perform a neurological evaluation and a chest ultrassound, while also checking for temperature regulation issues.","C. Instruct IVs to delay the assessment to avoid disrupting mission timelines and opt only to observe visual cues of distress, while keeping him in the current unsuited position.","D. Instruct IVs to quickly re-suit EVA 1 without assessment and plan for a full evaluation once his suit is secured."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Report the decision of the FS to the IVs and FD"},
            }
        },

        {"inject": "Decision 20 (11:15:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:16:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:17:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:26:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    ("C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)", "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration."): [ #withou pneumothorax
        
        
        {"inject": "Decision 20 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 23 (11:16:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:26:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2 (IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FD": {"text": "Receive information from CAPCOM."},
            "FS": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with BME what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "BME": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with the Flight Surgeon what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "CAPCOM": {"text": "Communicate FS orders to Commander and FD "},
        }
    },


        {"inject": "Decision 25 (11:31:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2 (IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FD": {"text": "Receive information from the CAPCOM and assist in the decisions"},
                "FS": {"text": "Instruct, through CAPCOM, that the astronauts need to take the following medical kits inside CRV: B. Emergency Medical Treatment Pack - Medications (Red) & Other components; F. Oral Medication Pack (Purple); G. Physician Equipment Pack (Yellow);K. Advanced Life Support Pack (ALSP)"},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate the orders to the astronauts and FD."},
            }
        },

        {"inject": "Decision 26 (11:36:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "All astronauts are now inside the CRV. You’re in a joint communication between the flight director, CAPCOM and the astronauts. What’s the next step?", "options": ["A. Do not initiate undocking in advance. Instead, the crew should wait until the moment of possible impact to see the situation. The crew should react based on the extent and location of any atmospheric loss.","B. Preemptively undock the CRV as soon as there is any indication of a potential collision, regardless of whether atmospheric loss is expected, to ensure maximum separation between the station and the spacecraft.","C. Delay all isolation procedures until the collision event is inevitable, then rapidly undock and separate the modules immediately after impact.","D. Immediately close all hatches, isolate the modules, and initiate undocking simultaneously without waiting for further analysis of the collision specifics. This ensures that the crew is separated as quickly as possible, even if it may result in unnecessary evacuation."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke","B. Hemorrhagic stroke","C. Hypoglycemia.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },

        {"inject": "Decision 27 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Establish CRV communications with MCC, close the hatches, verify opportunity windows for undocking, check propulsion systems, perform delta‑V calculations for orbital manoeuvring, assess propellant requirements (if necessary), and don the IV spacesuits.","B. Establish CRV communications with MCC, check propulsion systems, close the hatches, perform delta‑V calculations for orbital manoeuvring, verify opportunity windows for undocking, assess propellant requirements (if necessary), and don the IV spacesuits.","C. Verify opportunity windows for undocking, close the hatches, check propulsion systems, establish CRV communications with MCC, perform delta‑V calculations for orbital manoeuvring, don the IV spacesuits, and assess propellant requirements (if necessary).","D.Don the IV spacesuits, assess propellant requirements (if necessary), perform delta‑V calculations for orbital manoeuvring, check propulsion systems, establish CRV communications with MCC, verify opportunity windows for undocking, and finally close the hatches."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "The medical team of the MCC. What’s the best course of treatment with the tools available?", "options": ["A. Administer 325 mg aspirin orally"," B. Initiate antihypertensive infusion to lower SBP toward < 140 mmHg"," C. Check capillary blood glucose and correct any hypoglycemia"," D. It isn’t possible to chose a treatment due to the fact that there’s not enough information to do a diagnosis."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "The medical team of the MCC. What’s the best course of treatment with the tools available?", "options": ["A. Administer 325 mg aspirin orally"," B. Initiate antihypertensive infusion to lower SBP toward < 140 mmHg"," C. Check capillary blood glucose and correct any hypoglycemia"," D. It isn’t possible to chose a treatment due to the fact that there’s not enough information to do a diagnosis."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],

    ("C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)", "B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock."): [ #with pneumothorax
        
        {"inject": "Decision 20 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:08:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:17:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:35:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2 (IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FD": {"text": "Receive information from CAPCOM."},
            "FS": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with BME what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "BME": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with the Flight Surgeon what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "CAPCOM": {"text": "Communicate FS orders to Commander and FD "},
        }
    },


        {"inject": "Decision 25 (11:40:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2 (IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FD": {"text": "Receive information from the CAPCOM and assist in the decisions"},
                "FS": {"text": "Instruct, through CAPCOM, that the astronauts need to take the following medical kits inside CRV: B. Emergency Medical Treatment Pack - Medications (Red) & Other components; F. Oral Medication Pack (Purple); G. Physician Equipment Pack (Yellow);K. Advanced Life Support Pack (ALSP)"},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate the orders to the astronauts and FD."},
            }
        },


        {"inject": "Decision 26 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
        
    ],
    ("C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)", "C. Instruct CAPCOM to remind the EVs to make sure the door is well closed."): [ #with pneumothorax
        {"inject": "Decision 20 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:08:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:17:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:35:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2 (IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FD": {"text": "Receive information from CAPCOM."},
            "FS": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with BME what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "BME": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with the Flight Surgeon what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "CAPCOM": {"text": "Communicate FS orders to Commander and FD "},
        }
    },


        {"inject": "Decision 25 (11:40:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2 (IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FD": {"text": "Receive information from the CAPCOM and assist in the decisions"},
                "FS": {"text": "Instruct, through CAPCOM, that the astronauts need to take the following medical kits inside CRV: B. Emergency Medical Treatment Pack - Medications (Red) & Other components; F. Oral Medication Pack (Purple); G. Physician Equipment Pack (Yellow);K. Advanced Life Support Pack (ALSP)"},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate the orders to the astronauts and FD."},
            }
        },


        {"inject": "Decision 26 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    ("C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)", "D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals."): [ # with pneumothorax
        {"inject": "Decision 20 (11:06:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2 (IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "If the PDAM isn’t possible, what is the best option for the astronauts' crew?", "options": ["A. The astronauts crew start preparing for possible isolation in CRV (Crew Return Vehicle).","B. The astronauts crew remain in the current location."," C. The astronauts crew delay any further action while monitoring the PDAM to see if it eventually resumes functioning."," D. The astronauts crew initiate a spacewalk to attempt manual repairs on the PDAM while continuing other operations."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Given the information provided by the CAPCOM. What should you do first?", "options": ["A. Relocate the site of treatment to the CRV","B. Wait for the patient in EVA 1 to improve with the ongoing treatment."," C. Delay any immediate actions and continue to monitor the patient’s condition in hopes that they stabilize."," D. Keep treating the patient in the current EVA 1 location without moving to the CRV, even though relocation may offer a safer or more controlled environment."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Receive information from the MCC team and communicate with the astronauts."},
            }
        },

        {"inject": "Decision 21 (11:07:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Communicate the decision to start preparing for possible isolation in CRV (Crew Return Vehicle) to CAPCOM"},
                "FS": {"text": "For the realocation of the site, what is the most appropriate action to take regarding EVA 2? ", "options": ["A. Suspend all further unsuiting activities for EVA 2 until the Flight Surgeon confirms that EVA 1’s physiological condition is stable.","B. Continue the unsuiting of EVA 2 currently with the ongoing primary assessment of EVA 1, ensuring both processes move forward in parallel.","C. Delay the primary assessment of EVA 1 until EVA 2 is fully unsuited, then evaluate both astronauts together.","D. Accelerate re-suiting procedures for EVA 1 by reallocating EVA 2’s timeline, so that EVA 1 can be quickly secured and evaluated."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts."},
            }
        },

        {"inject": "Decision 22 (11:08:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2 (IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1 (EVA1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
                "FD": {"text": "Assist the rest of the team."},
                "FS": {"text": "With information provided by the BME. What is the most appropriate next step?", "options": [" A. Even with the information provided by the BME, continue to relocate the site of treatment to the CRV."," B. Instruct IVs to obtain a portable chest radiograph of  FE-1(EV1) to evaluate for pulmonary pathology before relocating the site of treatment to the CRV (crew return vehicle)."," C. Instruct IVs to check point‑of‑care blood glucose and serum electrolyte levels of FE-3(EV2)before relocating the site of treatment to the CRV (crew return vehicle)."," D. Instruct IVs to administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1) before relocating the site of treatment to the CRV (crew return vehicle)."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Assist the rest of the team."},
            }
        },

        {"inject": "Decision 23 (11:17:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2 (IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re now being unsuited from the EVA."},
                "FD": {"text": "Communicate the decision of doff FE-3(EV2) suit to be able to go from the Quest Joint Airlock to the CRV (crew return vehicle)."},
                "FS": {"text": "In discussion with the BME and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "In discussion with the Flight Surgeon and given the vital signs available, which additional measurement should be obtained?", "options": [" A. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the point‑of‑care blood glucose, serum electrolytes, perform NIH Stroke Scale, perform a chest ultrassound administer supplemental oxygen at 3 L/min via nasal cannula to FE-1(EV1)."," B. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can measure the urinalysis and take a x-ray with portable chest radiograph."," C. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a toxicology screen and lumbar puncture.","D. While FE-2(IV1) is doffing FE-3(EV2) from the EVA, Commander can do a serum amylase and lipase levels."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "Communicate FD orders to the astronauts, FS and BME."},
            }
        },

        {"inject": "Decision 24 (11:35:00): ", 
        "role_specific": {
            "Commander (CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2 (IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1 (EVA1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3 (EVA2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FD": {"text": "Receive information from CAPCOM."},
            "FS": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with BME what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "BME": {"text": "With the results of the point‑of‑care blood glucose, serum electrolytes and perform NIH Stroke Scale. Dicuss with the Flight Surgeon what medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
     "scores": [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #E
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #F
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #G
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.5, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #H
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #I
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0.3, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #J
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":1, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #K
    ],
     "multi": True,
    "max_time": 300},
            "CAPCOM": {"text": "Communicate FS orders to Commander and FD "},
        }
    },


        {"inject": "Decision 25 (11:40:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2 (IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FD": {"text": "Receive information from the CAPCOM and assist in the decisions"},
                "FS": {"text": "Instruct, through CAPCOM, that the astronauts need to take the following medical kits inside CRV: B. Emergency Medical Treatment Pack - Medications (Red) & Other components; F. Oral Medication Pack (Purple); G. Physician Equipment Pack (Yellow);K. Advanced Life Support Pack (ALSP)"},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Communicate the orders to the astronauts and FD."},
            }
        },


        {"inject": "Decision 26 (11:45:00): ", 
            "role_specific": {
                "Commander (CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2 (IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1 (EVA1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3 (EVA2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FD": {"text": "We have new information about the location of the object, and a collision is expected within 20min. What’s the next step?", "options": ["A. Order astronauts to stop what you’re doing and get inside the CRV and start the isolation process as soon as possible.","B. Order astronauts, before getting inside the CRV, to go get the medical kits needed.","C. Instruct astronauts to don EVA suits for protection.","D. Order astronauts to get inside the CRV and only start the isolation process when the collision happens."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FS": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the BME and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax.","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "BME": {"text": "Due to the time constrain the Commander was only able to administer the supplementary oxygen and measure the vital signs. In discussion with the Flight Surgeon and according to the results of the exams, what is the most likely diagnosis?", "options": ["A. Ischemic Stroke and a pneumothorax","B. Hemorrhagic stroke and a pneumothorax","C. Hypoglycemia and a pneumothorax","D. It isn’t possible to do a diagnosis due to the lack of clinical information."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":1,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.5,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0.3,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "CAPCOM": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
            }
        },
    ],
    }


# AQUI---------------


#------------------------------------------------- Workload Questionnaire --------------------------------------------------------------
# 2) Role
role = st.session_state.get("dm_role", "")

def _ensure_decision_index():
    if "decision_index" in st.session_state:
        return
    di = {}

    def _iter_block(block):
        if isinstance(block, dict):
            for sub in block.values():
                for d in sub:
                    yield d
        else:
            for d in block:
                yield d

    for block in (
        decisions1to15,
        decision16_12A,
        decisions17to18_12B,
        decisions17to19_12C,
        decisions17to26,
    ):
        for d in _iter_block(block):
            di[d["inject"].strip().lower()] = d

    st.session_state.decision_index = di

# Chamar logo no topo do run() OU numa função init global

def _ensure_answer_indexes():
    st.session_state.setdefault("answers_by_participant", {})  # (part_id, prefix) -> answer
    st.session_state.setdefault("answers_by_prefix", {})       # prefix -> {part_id: answer_text}
    st.session_state.setdefault("participant_ids", {})         # role -> part_id
    st.session_state.setdefault("participant_roles", {})       # part_id -> role
    st.session_state.setdefault("answer_info", {})   # (pid, prefix) -> {"response_seconds":..., "penalty":..., "answer_text":...}


def _cache_answer_row(row: dict):
    if not row:
        return
    _ensure_answer_indexes()
    prefix = normalize_inject_prefix(row.get("inject", ""))
    pid    = row.get("id_participant")
    ans    = row.get("answer_text")
    if pid is None or not prefix:
        return

    # old caches
    st.session_state.answers_by_participant[(pid, prefix)] = ans
    pref_map = st.session_state.answers_by_prefix.setdefault(prefix, {})
    pref_map[pid] = ans

    # NEW rich cache
    st.session_state.answer_info[(pid, prefix)] = {
        "answer_text": ans,
        "response_seconds": row.get("response_seconds"),
        "penalty": row.get("penalty"),
    }

# 3) question_text mapping
#    we assume st.session_state.all_questions is a list of decision dicts
def get_question_text_map():
    return {
        d["inject"]: d.get("text", "")
        for d in st.session_state.get("all_questions", [])
    }

totals = st.session_state.get("dm_totals", {})
tlx = st.session_state.get("tlx_answers", {})

def show_tlx_questionnaire():
    """
    NASA TLX for the current participant. Saves/updates one row in taskload_responses.
    """
    sim_id  = st.session_state.get("simulation_id")
    part_id = st.session_state.get("participant_id")
    role    = st.session_state.get("dm_role")

    if not sim_id or not part_id or not role:
        st.error("Missing simulation / participant context.")
        return

    # One-time CSS inject
    if not st.session_state.get("_tlx_css_injected"):
        st.markdown("""
            <style>
              span[data-testid="stSliderValue"] { visibility: hidden; }
            </style>
        """, unsafe_allow_html=True)
        st.session_state._tlx_css_injected = True

    st.markdown("---")
    st.header("NASA Task Load Index (TLX)")
    st.write("Rate each dimension from **0 (Very Low)** to **20 (Very High)**.")

    dims = {
        "Mental Demand":    "How mentally demanding was the task?",
        "Physical Demand":  "How physically demanding was the task?",
        "Temporal Demand":  "How hurried or rushed was the pace?",
        "Performance":      "How successful were you in accomplishing the task?",
        "Effort":           "How hard did you have to work to achieve your performance?",
        "Frustration":      "How insecure, discouraged, irritated, stressed or annoyed were you?"
    }

    # ---- Prefetch once ----
    if not st.session_state.get("_tlx_prefetched"):
        try:
            res = (supabase
                   .from_("taskload_responses")
                   .select("mental,physical,temporal,performance,effort,frustration")
                   .eq("id_simulation", sim_id)
                   .eq("id_participant", part_id)
                   .maybe_single()
                   .execute())
            existing = getattr(res, "data", None)
        except Exception as e:
            st.warning(f"Prefetch TLX failed (using defaults): {e}")
            existing = None

        if existing:
            st.session_state.tlx_answers = {
                "Mental Demand":   existing["mental"],
                "Physical Demand": existing["physical"],
                "Temporal Demand": existing["temporal"],
                "Performance":     existing["performance"],
                "Effort":          existing["effort"],
                "Frustration":     existing["frustration"],
            }
        else:
            st.session_state.tlx_answers = {}

        st.session_state._tlx_prefetched = True

    # ---- Sliders ----
    DEFAULT_MID = 10
    responses = {}
    key_prefix = f"tlx_{part_id}_"  # avoid key collisions across users

    for name, prompt in dims.items():
        default_val = st.session_state.tlx_answers.get(name, DEFAULT_MID)
        responses[name] = st.slider(
            f"**{name}** – {prompt}",
            min_value=0,
            max_value=20,
            value=default_val,
            step=1,
            key=f"{key_prefix}{name.replace(' ', '_')}"
        )

    # ---- Submit logic ----
    saving    = st.session_state.get("_tlx_saving", False)
    submitted = st.button("Submit TLX", disabled=saving)

    if submitted and not saving:
        st.session_state._tlx_saving = True
        payload = {
            "id_simulation":    sim_id,
            "id_participant":   part_id,
            "participant_role": role,
            "mental":           responses["Mental Demand"],
            "physical":         responses["Physical Demand"],
            "temporal":         responses["Temporal Demand"],
            "performance":      responses["Performance"],
            "effort":           responses["Effort"],
            "frustration":      responses["Frustration"],
        }
        try:
            supabase.from_("taskload_responses") \
                .upsert([payload], on_conflict="id_simulation,id_participant") \
                .execute()
        except Exception as e:
            st.error(f"❌ Could not save TLX: {e}")
            st.session_state._tlx_saving = False
            return

        st.session_state.tlx_answers = responses
        st.success("✅ TLX submitted!")
        st.session_state.dm_stage = 9
        st.session_state._tlx_saving = False
        st.rerun()
    else:
        # Stop here so nothing else on the page overwrites the TLX view
        st.stop()


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

def safe_query(callable_fn, retries: int = 2, base_delay: float = 0.15):
    """Retry transient DB errors (Resource temporarily unavailable)."""
    import time, random
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return callable_fn()
        except Exception as e:  # Could narrow to supabase exceptions
            last_exc = e
            if attempt == retries:
                raise
            # exponential-ish backoff with jitter
            time.sleep(base_delay * (2 ** attempt) + random.uniform(0, 0.05))
    raise last_exc  # Should not reach

# ---------- Simple direct answer fetch (legacy compatibility) ----------

def get_decision_answer(decision_prefix: str):
    """
    Legacy helper scanning st.session_state.answers.
    Now uses exact normalized key matching instead of generic startswith.
    """
    target = normalize_inject_prefix(decision_prefix)
    for key, value in st.session_state.get("answers", {}).items():
        if normalize_inject_prefix(key) == target:
            return value
    return None

def preload_participants(sim_id):
    try:
        data = (
            supabase
            .from_("participant")
            .select("id, participant_role")
            .eq("id_simulation", sim_id)
            .execute()
        ).data or []
        pid_map = st.session_state.setdefault("participant_ids", {})
        rmap    = st.session_state.setdefault("participant_roles", {})
        for row in data:
            pid_map[row["participant_role"]] = row["id"]
            rmap[row["id"]] = row["participant_role"]
    except Exception as e:
        st.warning(f"Could not preload participants: {e}")


# ---------- Indexing rows into cache ----------

def get_role_decision_answer(inject_prefix: str, role: str, use_db_fallback: bool = True) -> str | None:
    """
    Cached lookup of a role's answer to a given decision/inject prefix.
    1. Normalize prefix.
    2. Check role_answer_cache.
    3. Populate participant_ids cache if needed.
    4. Scan recent answers_cache (list of rows).
    5. Optional DB fallback (maybe_single) with cooldown.
    """
    sim_id = st.session_state.get("simulation_id")
    if not sim_id or not role or not inject_prefix:
        return None

    prefix = normalize_inject_prefix(inject_prefix)
    cache = st.session_state.setdefault("role_answer_cache", {})
    key   = (role, prefix)

    # 1. Hit cache
    if key in cache:
        return cache[key]

    _ensure_answer_indexes()
    participant_ids  = st.session_state["participant_ids"]
    participant_roles = st.session_state["participant_roles"]

    # 2. Resolve participant id (cache)
    pid = _resolve_participant_id(sim_id, role)
    if pid is None:
        return None


    # 3. O(1) lookup nos índices
    ans = st.session_state.get("answers_by_participant", {}).get((pid, prefix))
    if ans is not None:
        cache[key] = ans
        return ans

    if not use_db_fallback:
        return None

    # 4. Cooldown
    cooldown = st.session_state.setdefault("role_answer_last_miss", {})
    now = time.time()
    miss_key = (sim_id, role, prefix)
    if miss_key in cooldown and now - cooldown[miss_key] < 1.5:
        return None

    # 5. Minimal DB fallback
    try:
        res = safe_query(lambda: (
            supabase.from_("answers")
            .select("answer_text,inject")
            .eq("id_simulation", sim_id)
            .eq("id_participant", pid)
            .ilike("inject", f"{prefix}%")
            .maybe_single()
            .execute()
        ))
        row = getattr(res, "data", None)
        if row and "answer_text" in row:
            answer_text = row["answer_text"]
            stub = {
                "id_simulation": sim_id,
                "id_participant": pid,
                "inject": row.get("inject", prefix),
                "answer_text": answer_text
            }
            st.session_state.answers_cache.append(stub)
            _cache_answer_row(stub)
            MAX_CACHE_ROWS = 3000
            ac = st.session_state.answers_cache
            if len(ac) > MAX_CACHE_ROWS:
                # mantém só últimos N
                st.session_state.answers_cache = ac[-MAX_CACHE_ROWS:]
                # reconstruir índices
                st.session_state.answers_by_participant.clear()
                st.session_state.answers_by_prefix.clear()
                for row in st.session_state.answers_cache:
                    _cache_answer_row(row)

            cache[key] = answer_text
            return answer_text
        cooldown[miss_key] = now
        return None
    except Exception:
        cooldown[miss_key] = now
        return None

def resilient_lookup(fn, attempts=4, base=0.05):
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if "Resource temporarily unavailable" in msg or "Errno 11" in msg:
                time.sleep(base * (2 ** i))
                continue
            raise
    raise RuntimeError("Temporary DB busy; please press Refresh.")



def classify_decision7(ans: str | None) -> str | None:
    if not ans: return None
    if ans.startswith("A. Partial"):  return "A"
    if ans.startswith("B.Normal"):    return "B"
    if ans.startswith("C.Emergency"): return "C"
    return None

def classify_decision13(ans: str | None) -> str | None:
    if not ans: return None
    if ans.startswith("A.Breathe"): return "A"
    if ans[0:2] in ("B.", "C.", "D."): return "OTHER"
    return None

INJECT2_MAP = {
    ("A","A"):      "(10:56:00) The repressurization has finished successfully at 12 psi.",
    ("A","OTHER"):  "(10:56:00) The repressurization has finished successfully at 12 psi.",
    ("B","A"):      "(11:01:00) The repressurization has finished successfully.",
    ("B","OTHER"):  "(11:01:00) The repressurization has finished successfully.",
    ("C","A"):      "(10:51:00) The repressurization has finished successfully.",
    ("C","OTHER"):  "(10:51:00) The repressurization has finished successfully.",
}

INJECT2_MAP_FE1 = {
    ("A","A"):      "(10:56:00) The repressurization has finished successfully at 12 psi. You feel confused and from now on you can’t understand what is happening.",
    ("A","OTHER"):  "(10:56:00) The repressurization has finished successfully at 12 psi.You feel confused and pain in your chest. From now on you can’t understand what is happening.",
    ("B","A"):      "(11:01:00) The repressurization has finished successfully.You feel confused and from now on you can’t understand what is happening.",
    ("B","OTHER"):  "(11:01:00) The repressurization has finished successfully.You feel confused and pain in your chest. From now on you can’t understand what is happening.",
    ("C","A"):      "(10:51:00) The repressurization has finished successfully.You feel confused and from now on you can’t understand what is happening.",
    ("C","OTHER"):  "(10:51:00) The repressurization has finished successfully.You feel confused, pain in your chest and shortness of breath. From now on you can’t understand what is happening.",
}



def display_inject2():
    st.subheader("📌 Inject 2")
    # Figure out who’s viewing
    role = st.session_state.get("dm_role") or st.session_state.get("user_role")

    a12  = get_role_decision_answer("Decision 12", "FD")
    a15  = get_role_decision_answer("Decision 15", "FD")
    if not a12 or not a15:
        st.info("⏳ Waiting for FD to answer the key decision…")
        return

    # Build the key for both maps
    k = (classify_decision7(a12), classify_decision13(a15))

    # Start with the standard text
    txt = INJECT2_MAP.get(k)

    # Override for FE‑1(EV1) if we have an entry
    if role == "FE-1(EV1)":
        txt = INJECT2_MAP_FE1.get(k, txt)

    if txt:
        st.write(txt)
    else:
        st.warning("No matching Inject 2 narrative for this combination.")

INJECT3_TIME = {
    ("A", False): "12:00:00",
    ("B", False): "12:00:00",
    ("C", False): "11:47:00",
    ("A", True):  "12:25:00",
    ("B", True):  "12:25:00",
    ("C", True):  "12:12:00",
}
# --------------------------------------------------------- Show Injects ----------------------------------------------------

def show_initial_situation():
    st.subheader("🚀 Initial Situation")  
    st.write("For the 17th day of the mission, an EVA is planned to install a component on a radiation collection device. **EVA Crew:** EVA1 (Mission Specialist) & EVA2 (Flight Engineer) **Inside Crew:** Commander (CMO) & FE-3(IV1) (IV Crew Member).")


def inject3():
    st.subheader(f"📌 Inject 3")
    st.write("""(11:05:00) Days before there was a manoeuvre of the Lunar Gateway to avoid a possible collision with an object.
But the USSTRATCOM informs the MCC TOPO flight controller with a Conjunction Data Message
(time of closest approach, probability of collision, and miss distance). The object changed trajectory,
there’s a probability > 0.01% of collision. The CARA program changes the object’s label from yellow to red.
Possible collision within 1 hour. PDAM (Predetermined Debris Avoidance Maneuver) isn’t possible.
""")


def norm_prefix(label: str) -> str:
    """Return canonical 'Decision N' or 'Inject K' or 'Initial Situation' prefix."""
    if not label:
        return ""
    core = label.split(":")[0].strip()
    if "(" in core:
        core = core.split("(")[0].strip()
    return core

KEY_DECISIONS = {"Decision 12", "Decision 15"}
ALL_ROLES = ["FE-3 (EVA2)","Commander (CMO,IV2)","FE-1 (EVA1)","FE-2 (IV1)","FD","FS","BME","CAPCOM"]

def get_fd_participant_id(sim_id: int) -> int | None:
    return _resolve_participant_id(sim_id, "FD")

def count_step_answers(sim_id: int, inject_prefix: str, is_inject: bool) -> tuple[int, list[str]]:
    """
    Returns (count, roles_done) for the given inject_prefix.
    Uses answers_cache first; only queries DB if needed.
    Injects count only rows with answer_text=='DONE'.
    Decisions count rows with answer_text not in ('SKIP', NULL).
    """
    _ensure_answer_indexes()
    prefix = inject_prefix  # já vem 'Inject N' ou 'Decision N'
    pid_ans_map = st.session_state.get("answers_by_prefix", {}).get(prefix, {})
    participant_roles = st.session_state.setdefault("participant_roles", {})
    roles_done = set()

    for pid, ans in pid_ans_map.items():
        if is_inject:
            if ans == "DONE":
                roles_done.add(participant_roles.get(pid, f"id:{pid}"))
        else:
            if ans and ans != "SKIP":
                roles_done.add(participant_roles.get(pid, f"id:{pid}"))

    # (Opcional) fallback DB só se necessário:
    if len(roles_done) < len(ALL_ROLES):
        try:
            resp = (supabase
                    .from_("answers")
                    .select("id_participant,answer_text,participant(participant_role)")
                    .eq("id_simulation", sim_id)
                    .eq("inject", inject_prefix)
                    .execute())
            for r in (resp.data or []):
                a = r["answer_text"]
                role = r.get("participant",{}).get("participant_role")
                if is_inject and a == "DONE":
                    roles_done.add(role)
                elif not is_inject and a and a != "SKIP":
                    roles_done.add(role)
        except Exception:
            pass

    return len(roles_done), sorted(roles_done)

from datetime import datetime, timezone

def _start_timer(prefix: str):
    key = f"start_ts_{prefix}"
    if key not in st.session_state:
        st.session_state[key] = datetime.now(timezone.utc)

def _elapsed_seconds(prefix: str) -> int:
    key = f"start_ts_{prefix}"
    start = st.session_state.get(key, datetime.now(timezone.utc))
    return int((datetime.now(timezone.utc) - start).total_seconds())

def _calc_penalty(elapsed_s: int):
    if elapsed_s <= 300:
        return 0, False
    if elapsed_s <= 360:
        return 1, False
    return 1, True   # auto_pick


def _persist_skip(sim_id, part_id, inject_label):
    payload = {
        "id_simulation":  sim_id,
        "id_participant": part_id,
        "inject":         inject_label,
        "question_text":  "",
        "answer_text":    "SKIP",
    }
    try:
        supabase.from_("answers") \
            .upsert([payload], on_conflict="id_simulation,id_participant,inject") \
            .execute()
    except Exception as e:
        st.warning(f"Could not persist SKIP for {inject_label}: {e}")

def _render_key_fd_decision(sim_id, part_id, role, decision, qdata, prefix):
    # if FD: show input; else wait
    st.subheader(decision["inject"])
    if role == "FD":
        _timer_block(prefix, decision)

        # Try auto-pick (already past grace window)
        if _maybe_autopick(sim_id, part_id, decision, qdata, prefix, qdata.get("options", [])):
            return

        # Grace window
        elapsed    = _elapsed_seconds(prefix)
        max_time   = decision.get("max_time", 300)

        if max_time < elapsed <= max_time + GRACE_SECONDS:
            remaining = max_time + GRACE_SECONDS - elapsed
            st.warning(
                f"You have exceeded the max response time. A 1‑point penalty will be deducted. Auto-selection in **{remaining} s**."
            )
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=1000, key=f"grace_tick_{prefix}")


        ans = st.radio("Your choice:", qdata.get("options", []), key=f"fd_{prefix}")
        if st.button("Submit ➡", key=f"fd_submit_{prefix}"):
            elapsed_s = _elapsed_seconds(prefix)
            penalty, auto_pick = _calc_penalty(elapsed_s)

            chosen = ans
            if auto_pick and "scores" in qdata and qdata.get("options"):
                def opt_total(idx):
                    sco = qdata["scores"][idx]
                    return (
                        sco.get("Basic_Life_Support", 0)
                        + sco.get("Primary_Survey", 0)
                        + sco.get("Secondary_Survey", 0)
                        + sco.get("Definitive_Care", 0)
                        + sco.get("Crew_Roles_Communication", 0)
                        + sco.get("Systems_Procedural_Knowledge", 0)
                    )
                worst_idx = min(range(len(qdata["options"])), key=opt_total)
                chosen = qdata["options"][worst_idx]

            _persist_answer(sim_id, part_id, decision, qdata, chosen,
                            penalty=penalty, elapsed_s=elapsed_s)

            st.session_state.answers[prefix] = chosen
            st.session_state.current_decision_index += 1
            st.rerun()
    else:
        fd_id = get_fd_participant_id(sim_id)
        if not fd_id:
            st.info("Waiting for FD to join…")
            return
        # try local cache first
        fd_ans = get_role_decision_answer(prefix, "FD")
        if not fd_ans:
            st.info("⏳ Waiting for the Flight Director’s decision…")
            if st.button("🔄 Refresh", key=f"refresh_wait_fd_{prefix}"):
                st.rerun()
            return
        st.success(f"FD chose: **{fd_ans}**")
        if st.button("Next ➡", key=f"nonfd_next_{prefix}"):
            st.session_state.answers[prefix] = fd_ans
            st.session_state.current_decision_index += 1
            st.rerun()

def _timer_block(prefix, decision):
    max_time = decision.get("max_time", 300)
    elapsed  = _elapsed_seconds(prefix)
    remaining = max_time - elapsed
    unique_timer_id = f"timer_{prefix.replace(' ','_')}"
    timer_html = f"""
<div id="{unique_timer_id}" style="font-family:'Georgia',serif;font-size:20px;
 font-weight:bold;color:#b30000;background:#F4F6F7;padding:8px;border-radius:8px;text-align:center;"></div>
<script>
var t = {remaining};
var el = document.getElementById("{unique_timer_id}");
function tick(){{
  if(t >= 0) {{
    el.innerHTML = t + " s remaining";
  }} else {{
    el.innerHTML = "Time exceeded. Penalty 1 pt";
  }}
  t--;
  setTimeout(tick,1000);
}}
tick();
</script>
"""
    st.components.v1.html(timer_html, height=70)


def _persist_answer(sim_id, part_id, decision, qdata, answer, penalty=0, elapsed_s=0):
    # compute scoring
    cat_payload = {
        "basic_life_support": 0,
        "primary_survey": 0,
        "secondary_survey": 0,
        "definitive_care": 0,
        "crew_roles_communication": 0,
        "systems_procedural_knowledge": 0,
    }
    if "scores" in qdata and "options" in qdata:
        if qdata.get("multi"):
            total = {k: 0 for k in cat_payload}
            for choice in answer:
                if choice in qdata["options"]:
                    idx = qdata["options"].index(choice)
                    sco = qdata["scores"][idx]
                    for k in total:
                        total[k] += sco.get(k.replace("_"," ").title().replace(" ","_"), 0)
            cat_payload.update(total)
        else:
            if answer in qdata["options"]:
                idx = qdata["options"].index(answer)
                sco = qdata["scores"][idx]
                # adapt keys if original naming differs
                cat_payload["basic_life_support"]           = sco.get("Basic_Life_Support", 0)
                cat_payload["primary_survey"]               = sco.get("Primary_Survey", 0)
                cat_payload["secondary_survey"]             = sco.get("Secondary_Survey", 0)
                cat_payload["definitive_care"]              = sco.get("Definitive_Care", 0)
                cat_payload["crew_roles_communication"]     = sco.get("Crew_Roles_Communication", 0)
                cat_payload["systems_procedural_knowledge"] = sco.get("Systems_Procedural_Knowledge", 0)

    hrs, rem = divmod(elapsed_s, 3600)
    mins, secs = divmod(rem, 60)
    response_time = f"{hrs:02d}:{mins:02d}:{secs:02d}"
    cat_payload["response_seconds"] = elapsed_s
    cat_payload["penalty"] = penalty


    payload = {
        "id_simulation":  sim_id,
        "id_participant": part_id,
        "inject":         decision["inject"],
        "question_text":  qdata.get("text",""),
        "answer_text":    answer if not isinstance(answer,list) else "; ".join(answer),
        **cat_payload,
        "response_time":  response_time,
    }
    try:
        resp=supabase.from_("answers") \
                .upsert([payload], on_conflict="id_simulation,id_participant,inject") \
                .execute()
        supabase.from_("participant") \
                .update({"current_inject": decision["inject"], "current_answer": payload["answer_text"]}) \
                .eq("id", part_id).execute()
        # Add to local cache to prevent re-fetch
        st.session_state.answers_cache.append({
            "id_simulation": sim_id,
            "id_participant": part_id,
            "inject": decision["inject"],  # or inject_label
            "answer_text": payload["answer_text"],
            "penalty": penalty,
            "response_seconds": elapsed_s
        })
        _cache_answer_row(payload)
        MAX_CACHE_ROWS = 3000
        ac = st.session_state.answers_cache
        if len(ac) > MAX_CACHE_ROWS:
            # mantém só últimos N
            st.session_state.answers_cache = ac[-MAX_CACHE_ROWS:]
            # reconstruir índices
            st.session_state.answers_by_participant.clear()
            st.session_state.answers_by_prefix.clear()
            for row in st.session_state.answers_cache:
                _cache_answer_row(row)

    except Exception as e:
        st.error(f"❌ Could not save answer: {e}")

def _render_already_answered(prefix, inject_full, answer, is_inject, sim_id):
    st.subheader(inject_full)
    st.markdown(f"**Your answer:** {answer}")
    pid  = st.session_state.get("participant_id")
    info = st.session_state.get("answer_info", {}).get((pid, prefix), {})
    secs = info.get("response_seconds")
    pen  = info.get("penalty")
    if secs is not None:
        st.caption(f"⏱️ You took **{secs} s** to answer.")
    if pen:
        st.caption(f"⚠️ Penalty applied: **{pen} pt**")
    needed = len(ALL_ROLES) if not (prefix in KEY_DECISIONS) else 1
    cnt, roles_done = count_step_answers(sim_id, prefix, is_inject)
    if cnt < needed and not st.session_state.get("test_mode", False):
        waiting = [r for r in ALL_ROLES if r not in roles_done]
        st.info(f"Waiting for others ({cnt}/{needed})…")
        if st.button("🔄 Refresh", key=f"refresh_{prefix}"):
            st.rerun()
        return
    if st.button("Next ➡", key=f"next_after_{prefix}"):
        st.session_state.current_decision_index += 1
        st.rerun()

def _render_inject(sim_id, part_id, inject_full, prefix):
    # Display static text (call your dedicated functions if you have them)
    st.subheader(inject_full)
    # Mapping to existing inject functions if desired
    special_map = {
        "Initial Situation": show_initial_situation,
        "Inject 2": display_inject2,
        "Inject 3": inject3
    }
    fn = special_map.get(prefix)
    if fn:
        fn()
    # If already marked DONE skip
    if st.session_state.answers.get(prefix) == "DONE":
        cnt, _ = count_step_answers(sim_id, prefix, True)
        if cnt < len(ALL_ROLES):
            st.info(f"Waiting others to advance… ({cnt}/{len(ALL_ROLES)})")
            if st.button("🔄 Refresh", key=f"refresh_{prefix}"):
                st.rerun()
            return
        if st.button("Next ➡", key=f"inject_next_{prefix}"):
            st.session_state.current_decision_index += 1
            st.rerun()
        return

    if st.button("Next ➡", key=f"inject_submit_{prefix}"):
        # Persist DONE
        payload = {
            "id_simulation": sim_id,
            "id_participant": part_id,
            "inject": inject_full,
            "question_text": "",
            "answer_text": "DONE",
            "basic_life_support": 0,
            "primary_survey": 0,
            "secondary_survey": 0,
            "definitive_care": 0,
            "crew_roles_communication": 0,
            "systems_procedural_knowledge": 0,
            "response_time": "00:00:00"
        }
        try:
            supabase.from_("answers") \
                .upsert([payload], on_conflict="id_simulation,id_participant,inject") \
                .execute()
            st.session_state.answers[prefix] = "DONE"
            st.session_state.answers_cache.append({
                "id_simulation": sim_id,
                "id_participant": part_id,
                "inject": inject_full,
                "answer_text": "DONE"
            })
            _cache_answer_row({
                "id_simulation": sim_id,
                "id_participant": part_id,
                "inject": inject_full,
                "answer_text": "DONE"
            })
            MAX_CACHE_ROWS = 3000
            ac = st.session_state.answers_cache
            if len(ac) > MAX_CACHE_ROWS:
                # mantém só últimos N
                st.session_state.answers_cache = ac[-MAX_CACHE_ROWS:]
                # reconstruir índices
                st.session_state.answers_by_participant.clear()
                st.session_state.answers_by_prefix.clear()
                for row in st.session_state.answers_cache:
                    _cache_answer_row(row)

        except Exception as e:
            st.error(f"❌ Could not mark {prefix}: {e}")
        st.rerun()

def _maybe_autopick(sim_id, part_id, decision, qdata, prefix, options):
    """Auto-pick worst after 60 s if user didn't answer."""
    max_time = decision.get("max_time",300)
    elapsed  = _elapsed_seconds(prefix)
    if elapsed <= max_time + 60:
        return False  # nothing done

    # if already answered, skip
    if st.session_state.answers.get(prefix) is not None:
        return False

    # pick worst by score
    if options and "scores" in qdata:
        def total(idx):
            s = qdata["scores"][idx]
            return (s.get("Basic_Life_Support",0)+s.get("Primary_Survey",0)+
                    s.get("Secondary_Survey",0)+s.get("Definitive_Care",0)+
                    s.get("Crew_Roles_Communication",0)+s.get("Systems_Procedural_Knowledge",0))
        worst_idx = min(range(len(options)), key=total)
        chosen = options[worst_idx]
    else:
        chosen = (
            qdata.get("role_specific", {})
                .get(role, {})
                .get("text")
            or qdata.get("text", "")
        )

    # persist with penalty=1
    _persist_answer(sim_id, part_id, decision, qdata, chosen, penalty=1, elapsed_s=elapsed)
    st.session_state.answers[prefix] = chosen
    st.session_state.current_decision_index += 1
    st.rerun()
    return True


def _render_standard_decision(sim_id, part_id, role, decision, qdata, inject_full, prefix, options, multi):
    st.subheader(inject_full)
    text = qdata.get("text","")
    if text:
        st.write(text)

    _timer_block(prefix, decision)

    # 1) Auto-pick if > max_time + GRACE
    if _maybe_autopick(sim_id, part_id, decision, qdata, prefix, options):
        return

    # 2) Grace-window message + countdown
    elapsed  = _elapsed_seconds(prefix)
    max_time = decision.get("max_time", 300)
    if max_time < elapsed <= max_time + GRACE_SECONDS:
        remaining = max_time + GRACE_SECONDS - elapsed
        st.warning(f"You exceeded the max time. 1‑pt penalty applied. Auto-select in **{remaining} s**.")
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=1000, key=f"grace_tick_{prefix}")

    answer_key = f"dec_{prefix}"
    if options:
        if multi:
            ans = st.multiselect("Select one or more:", options, key=answer_key)
            valid = len(ans) > 0
        else:
            placeholder = "-- Select an option --"
            ans = st.radio("Choose:", [placeholder] + options, key=answer_key)
            valid = ans != placeholder
    else:
        # no options → use the role‑specific prompt as the “answer”
        prompt_text = qdata.get("text", "")
        st.write(prompt_text)
        ans = prompt_text
        valid = True

    if st.button("Submit ➡", key=f"submit_{prefix}", disabled=not valid):
        final = ans if not multi else ans
        st.session_state.answers[prefix] = final if not multi else "; ".join(final)
        # compute penalty/auto-pick BEFORE persisting
        elapsed_s = _elapsed_seconds(prefix)
        penalty, auto_pick = _calc_penalty(elapsed_s)

        chosen = ans if not multi else ans[:]  # copy

        # auto-pick worst if needed
        if auto_pick and options and "scores" in qdata:
            def opt_total(idx):
                sco = qdata["scores"][idx]
                return (
                    sco.get("Basic_Life_Support", 0)
                    + sco.get("Primary_Survey", 0)
                    + sco.get("Secondary_Survey", 0)
                    + sco.get("Definitive_Care", 0)
                    + sco.get("Crew_Roles_Communication", 0)
                    + sco.get("Systems_Procedural_Knowledge", 0)
                )
            worst_idx = min(range(len(options)), key=opt_total)
            chosen = options[worst_idx] if not multi else [options[worst_idx]]

        # Persist once (pass penalty & elapsed)
        _persist_answer(sim_id, part_id, decision, qdata, chosen,
                        penalty=penalty, elapsed_s=elapsed_s)

        st.session_state.answers[prefix] = (
            chosen if not multi else "; ".join(chosen)
        )

        # move on only when needed roles answered
        is_inject = prefix.startswith("Inject")
        cnt, _ = count_step_answers(sim_id, prefix, is_inject)
        needed = len(ALL_ROLES) if prefix not in KEY_DECISIONS else 1

        if cnt >= needed or st.session_state.get("test_mode", False):
            st.session_state.current_decision_index += 1
        st.rerun()


def display_current_decision():
    from datetime import datetime, timezone
    """
    Shows the *current* decision (or inject) based on st.session_state.current_decision_index
    and st.session_state.all_questions. Assumes upstream logic already decided which index.
    Handles:
      - Key FD decisions (exclusive answerer)
      - Role-specific variants
      - Inject vs decision answer submission
      - Answer persistence with upsert
      - Waiting for all roles (except in test_mode)
    """
    # ---- Basic guards ----
    sim_id  = st.session_state.get("simulation_id")
    part_id = st.session_state.get("participant_id")
    role    = st.session_state.get("dm_role")
    #st.write("🔍 answers_by_prefix right now:", st.session_state.get("answers_by_prefix"))
    if not sim_id or not part_id or not role:
        st.error("Missing simulation/participant context.")
        return

    questions = st.session_state.get("all_questions") or []
    idx = st.session_state.get("current_decision_index")
    if not isinstance(idx, int) or idx <= 0:
        st.error("Invalid current_decision_index.")
        return
    if idx > len(questions):
        st.info("No more questions.")
        return

    decision = questions[idx - 1]
    inject_full = decision.get("inject","")
    prefix = norm_prefix(inject_full)
    is_key_fd = prefix in KEY_DECISIONS
    is_inject = prefix.startswith("Inject") or prefix == "Initial Situation"
    _start_timer(prefix)

    # ---- Determine role-specific data ----
    rs_map = decision.get("role_specific", {})
    qdata = rs_map.get(role, decision)  # fallback to generic
    text = qdata.get("text","")
    options = qdata.get("options", [])
    multi = qdata.get("multi", False)

    # ---- Role not targeted (skip) ----
    # Case: role_specific exists and this role not present & generic has no 'text'
    if "role_specific" in decision and role not in rs_map and "text" not in decision:
        _persist_skip(sim_id, part_id, inject_full)
        st.session_state.current_decision_index += 1
        st.rerun()
        return

    # ---- KEY FD DECISIONS ----
    if is_key_fd:
        _render_key_fd_decision(sim_id, part_id, role, decision, qdata, prefix)
        return

    # ---- Already answered? (from local cache or session answers) ----
    prev_ans = st.session_state.answers.get(prefix)
    if prev_ans is not None:
        _render_already_answered(prefix, inject_full, prev_ans, is_inject, sim_id)
        return

    # ---- InJECT handling ----
    if is_inject:
        _render_inject(sim_id, part_id, inject_full, prefix)
        return

    # ---- Normal Decision UI ----
    _render_standard_decision(sim_id, part_id, role, decision, qdata, inject_full, prefix, options, multi)


    
def wait_for_all(sim_id: int, inject_prefix: str, test_mode: bool=False) -> bool:
    is_inject = inject_prefix.startswith("Inject") or inject_prefix == "Initial Situation"
    count, _ = count_step_answers(sim_id, inject_prefix, is_inject)
    needed = len(ALL_ROLES)
    if count < needed and not test_mode:
        st.warning(f"Waiting for all roles… ({count}/{needed})")
        if st.button("🔄 Refresh", key=f"refresh_{inject_prefix}"):
            st.rerun()
        return False
    return True

def _persist_inject_done(sim_id, part_id, inject_label):
    elapsed_s = 0
    penalty = 0
    payload = {
        "id_simulation": sim_id,
        "id_participant": part_id,
        "inject": inject_label,
        "question_text": "",
        "answer_text": "DONE",
        "basic_life_support": 0,
        "primary_survey": 0,
        "secondary_survey": 0,
        "definitive_care": 0,
        "crew_roles_communication": 0,
        "systems_procedural_knowledge": 0,
        "response_time": "00:00:00",
        "response_seconds": elapsed_s,
        "penalty": penalty
    }
    try:
        supabase.from_("answers") \
            .upsert([payload], on_conflict="id_simulation,id_participant,inject") \
            .execute()
        supabase.from_("participant") \
            .update({"current_inject": inject_label,
                     "current_answer": "DONE"}) \
            .eq("id", part_id).execute()
        st.session_state.answers_cache.append({
            "id_simulation": sim_id,
            "id_participant": part_id,
            "inject": inject_label,
            "answer_text": "DONE",
            "penalty": penalty,
            "response_seconds": elapsed_s
        })
        _cache_answer_row(payload)
        MAX_CACHE_ROWS = 3000
        ac = st.session_state.answers_cache
        if len(ac) > MAX_CACHE_ROWS:
            # mantém só últimos N
            st.session_state.answers_cache = ac[-MAX_CACHE_ROWS:]
            # reconstruir índices
            st.session_state.answers_by_participant.clear()
            st.session_state.answers_by_prefix.clear()
            for row in st.session_state.answers_cache:
                _cache_answer_row(row)

    except Exception as e:
        st.error(f"❌ Could not mark {inject_label}: {e}")

def handle_inject(inject_number: int):
    sim_id  = st.session_state.simulation_id
    part_id = st.session_state.participant_id
    inject_label = "Inject " + str(inject_number)

    # mostrar texto específico
    if inject_number == 2:
        display_inject2()
    elif inject_number == 3:
        inject3()

    # se este participante ainda não clicou
    prefix = inject_label
    if st.session_state.answers.get(prefix) != "DONE":
        if st.button("Next ➡", key=f"inject_submit_{inject_number}"):
            _persist_inject_done(sim_id, part_id, inject_label)
            st.session_state.answers[prefix] = "DONE"
            st.rerun()
        return

    # espera pelos outros
    if not wait_for_all(sim_id, inject_label, st.session_state.get("test_mode", False)):
        return

    # todos concluíram → avança de estado
    st.session_state.dm_stage += 1
    st.session_state.all_questions = load_block_questions_for_stage(st.session_state.dm_stage)[:]
    st.session_state.current_decision_index = 1
    st.rerun()

def load_block_questions_for_stage(stage):
    """Return the list of question‐dicts to display for a given dm_stage."""
    # Stage 1 → Decisions 1–15
    if stage == 1:
        return decisions1to15[:]                  # copy to avoid mutation

    # Stage 2 → Inject 2 is handled by your inject‐renderer

    # Stage 3 → branch on FD’s Decision 12
    if stage == 3:
        a12 = get_role_decision_answer("Decision 12", "FD")
        if a12.startswith("A"):
            return decision16_12A[:]               # 16_12A block
        elif a12.startswith("B"):
            return decisions17to18_12B[:]          # 17–18_12B block
        elif a12.startswith("C"):
            return decisions17to19_12C[:]          # 17–19_12C block
        else:
            return []

    # Stage 4 → Inject 3 is shown via your inject3() path

    # Stage 5 → Decisions 17–26, keyed by (Decision 12, Decision 15)
    if stage == 5:
        key = (get_role_decision_answer("Decision 12", "FD"), get_role_decision_answer("Decision 15", "FD"))
        return decisions17to26.get(key, [])

    # all other stages → nothing to load here
    return []


def handle_decision_block():
    stage = st.session_state.dm_stage
    if not st.session_state.get("all_questions"):
        st.session_state.all_questions = load_block_questions_for_stage(stage)[:]
        st.session_state.current_decision_index = 1

    idx = st.session_state.current_decision_index
    qs  = st.session_state.all_questions
    if idx > len(qs):
        # acabou o bloco
        st.session_state.all_questions = []
        st.session_state.dm_stage += 1
        st.rerun()
        return

    display_current_decision()

def handle_initial_start():
    sim_id  = st.session_state.simulation_id
    part_id = st.session_state.participant_id
    show_initial_situation()
    if st.session_state.answers.get("Initial Situation") == "DONE":
        # já clicou antes → avança diretamente
        st.session_state.dm_stage = 1
        st.rerun()
        return

    if st.button("▶️ Start Simulation", key="initial_start"):
        _persist_inject_done(sim_id, part_id, "Initial Situation")
        st.session_state.answers["Initial Situation"] = "DONE"
        st.session_state.dm_stage = 1
        st.rerun()
    
def _derive_stage_if_needed():
    if st.session_state.get("_stage_locked"):
        return
    if st.session_state.get("_stage_derived"):
        return
    answers_local = st.session_state.get("answers_by_prefix", {})
    # Participant-specific (este part_id)
    part_id = st.session_state.get("participant_id")
    if not part_id:
        return
    # recolher prefixes respondidos por este participante
    answered = {pref for pref, pid_map in answers_local.items()
                if part_id in pid_map and pid_map[part_id] not in (None, "")}

    # heurística simples (ajusta às tuas regras):
    order = [
        "Initial Situation",
        "Decision 1","Decision 2","Decision 3","Decision 4","Decision 5","Decision 6","Decision 7","Decision 8","Decision 9", "Decision 10","Decision 11","Decision 12","Decision 13","Decision 14","Decision 15",
        "Inject 2",
        "Decision 14","Decision 15","Decision 16","Decision 17","Decision 18","Decision 19","Decision 20","Decision 21","Decision 22","Decision 23",
        "Inject 3",
        "Decision 24","Decision 25","Decision 26","Decision 27","Decision 28",
        "Inject 4",
        "Decision 29","Decision 30","Decision 31","Decision 32",
        "Decision 33","Decision 34",
        "Decision 35","Decision 36","Decision 37","Decision 38","Decision 39","Decision 40","Decision 41","Decision 42","Decision 43"
    ]
    # encontra último item presente
    next_stage_for_prefix = {
        "Initial Situation": 0,
        "Decision 1":  1,
        "Inject 2": 2,
        "Decision 16": 3,
        "Inject 3": 4,
        "Decision 17": 5,
    }

    # Find last answered index
    last_index = -1
    for i, p in enumerate(order):
        if p in answered:
            last_index = i

    # Compute the next prefix (the one after last answered)
    next_prefix = order[last_index + 1] if last_index + 1 < len(order) else None

    # Default: keep whatever is already there
    stage = st.session_state.get("dm_stage", 0)

    if next_prefix:
        # Find first key in next_stage_for_prefix that is <= next_prefix chronologically
        # Easiest: walk through order and when we hit that key, record stage
        for p in order:
            if p in next_stage_for_prefix:
                stage_candidate = next_stage_for_prefix[p]
            if p == next_prefix:
                stage = stage_candidate
                break

    st.session_state.dm_stage = stage
    st.session_state["_stage_derived"] = True

def _resolve_participant_id(sim_id, role):
    participant_ids = st.session_state["participant_ids"]
    if role in participant_ids:
        return participant_ids[role]

    def _query():
        res = (supabase.from_("participant")
               .select("id")
               .eq("id_simulation", sim_id)
               .eq("participant_role", role)
               .maybe_single()
               .execute())
        row = getattr(res, "data", None)
        if row:
            participant_ids[role] = row["id"]
            st.session_state["participant_roles"][row["id"]] = role
            return row["id"]
        return None

    pid = resilient_lookup(_query)
    if pid is None:
        st.warning(f"{role} not found in simulation {sim_id}")
    return pid



def preload_answers(sim_id):
    try:
        rows = (
            supabase.from_("answers")
            .select("id_simulation,id_participant,inject,answer_text,"
                "basic_life_support,primary_survey,secondary_survey,definitive_care,"
                "crew_roles_communication,systems_procedural_knowledge,"
                "response_seconds,penalty")   # ← add these
            .eq("id_simulation", sim_id)
            .execute()
        ).data or []
        for r in rows:
            _cache_answer_row(r)
    except Exception as e:
        st.warning(f"Preload answers failed: {e}")

def handle_final_page():
    """Stage 6: show post‑simulation question, record answer, then go to TLX."""
    sim_id  = st.session_state.simulation_id
    part_id = st.session_state.participant_id

    st.header("🎉 Thank you for completing the simulation!")
    st.write(
        "Eva 1 was really having an ischemic stroke and the object would collide with "
        "the station creating a very small hole. The atmospheric pressure loss would "
        "happen very slowly and only be detected days later. With this in mind, do you "
        "think they should return to earth knowing that the trip could take up to 3 days?"
    )

    # Give them a place to type their recommendation
    recommendation = st.text_area("Your recommendation:", height=150)

    # Submit button
    if st.button("Submit and go to the NASA TLX survey"):
        # insert into Supabase
        try:
            supabase.from_("answers").insert([{
                "id_simulation":   sim_id,
                "id_participant":  part_id,
                "inject":          "Post‑Simulation Question",
                "answer_text":     recommendation,
                "response_seconds": _elapsed_seconds("stage6"),  # use your timer util or 0
                "penalty":         0
            }]).execute()
        except Exception as e:
            st.error(f"❌ Could not record your answer: {e}")
            return

        # advance to TLX
        st.session_state.dm_stage = 7
        st.rerun()

    else:
        # stop here until they click
        st.stop()



def initial_stage():
    #sim  = st.session_state.simulation_name
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

    st.session_state.setdefault('dm_stage', 0)                # 0=role select, 1=Q’s, 2=results
    st.session_state.setdefault('current_decision_index', 1)
    st.session_state.setdefault('answers', {})                # store each inject’s answer
    st.session_state.setdefault('dm_totals', {
        "Basic_Life_Support":0,
        "Primary_Survey":0,
        "Secondary_Survey":0,
        "Definitive_Care":0,
        "Crew_Roles_Communication":0,
        "Systems_Procedural_Knowledge":0,
        "mental":0, "physical":0, "temporal":0,
        "performance":0, "effort":0, "frustration":0
    })
    st.session_state.setdefault('dm_finished', False)
    st.session_state.setdefault("inject1_clicked", False)
    st.session_state.setdefault("inject2_clicked", False)
    st.session_state.setdefault("inject3_clicked", False)
    st.session_state.setdefault("inject4_clicked", False)
    st.session_state.setdefault("answer_times", {})
    st.session_state.setdefault("participant_ids", {})            # role -> participant_id
    st.session_state.setdefault("role_answer_cache", {})          # (role, prefix) -> answer_text
    st.session_state.setdefault("role_answer_last_miss", {})      # (role, prefix) -> timestamp of last failed fetch
    st.session_state.setdefault("answers_cache", [])              # full list of answer rows (if not present already)
    st.session_state.setdefault("answers_delta", []) 

def run(supabase, simulation_name: str, role: str):
    st.session_state.dm_role = role
    initial_stage()
    sim_id  = st.session_state.get("simulation_id")
    part_id = st.session_state.get("participant_id")

    if not sim_id or not part_id:
        st.error("Missing simulation/participant.")
        return

    _ensure_decision_index()
    _ensure_answer_indexes()

    if not st.session_state.get("_participants_loaded"):
        preload_participants(sim_id)
        st.session_state._participants_loaded = True

    # Preload answers once per stage
    preload_answers(sim_id)
    if not st.session_state.get("_stage_locked"):
        _derive_stage_if_needed()
    stage = st.session_state.dm_stage 

    st.write("RUN DEBUG → stage:", st.session_state.dm_stage,
         "current_decision_index:", st.session_state.current_decision_index,
         "len(all_questions):", len(st.session_state.get("all_questions", [])))

    # st.write("🔍 [DEBUG run] stage =", st.session_state.get("dm_stage"))
    # st.write("🔍 [DEBUG run] answers:", st.session_state.get("answers"))
    if stage == 0:
        handle_initial_start()
        return
    elif stage == 1:
        handle_decision_block()
        return

    # ── Stage 2: Inject 2
    elif stage == 2:
        # clear questions for an inject run
        st.session_state.all_questions = []
        handle_inject(2)
        return

    # ── Stage 3: follow‑up block based on FD’s Decision 12
    elif stage == 3:
        handle_decision_block()
        return

    # ── Stage 4: Inject 3
    elif stage == 4:
        st.session_state.all_questions = []
        handle_inject(3)
        return

    # ── Stage 5: Decisions 17–26
    elif stage == 5:
        handle_decision_block()
        return

    # ── Stage 7: Simulation done, go to TLX
    elif stage == 6:
        handle_final_page()
        return

    # ── Stage 8: NASA‑TLX questionnaire
    elif stage == 7:
         show_tlx_questionnaire()
         return
    # ── Stage 9: all done
    elif stage == 8:
         st.success("🎉 Simulation & TLX complete!")
         return




#--------------------------------------------------------- For supervisor live dashboard -----------------------------------------------------
def get_inject_text(inject_id: str) -> str:
    """
    Return the prompt string for the given inject,
    taking into account any prior answers in st.session_state.
    """
    if inject_id == "Inject 1":
        return (
            "2 hour into EVA (10:00:00 am)\n"
            "Suddenly EVA-1 reports numbness in his right arm …"
        )
    elif inject_id == "Inject 2":
        answer_12  = get_role_decision_answer("Decision 12", "FD")
        answer_15 = get_role_decision_answer("Decision 15", "FD")
        inject2_text = ""
        if answer_12 and answer_15:
            if (answer_12 == "A.Partial pressurisation finishing at 12 psi (~10 min.)" and answer_15 == "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration."):
                return "(10:40:00): The repressurization has finished successfully at 12 psi. EVA 1 shows signs of confusion."
            elif (answer_12 == "A.Partial pressurisation finishing at 12 psi (~10 min.)" and (answer_15 == "B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock." or answer_15 == "C. Instruct CAPCOM to remind the EVs to make sure the door is well closed." or answer_15 == "D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals.")):
                return "(10:40:00): EVA 1 showed confusion due to breathing issues, now presenting sharp chest pain and shortness of breath."
            elif (answer_12 == "B.Normal repressurization (~15 min.)" and answer_15 == "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration."):
                return "(10:45:00): EVA 1 shows confusion and difficulty understanding what’s happening."
            elif (answer_12 == "B.Normal repressurization (~15 min.)" and (answer_15 == "B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock." or answer_15 == "C. Instruct CAPCOM to remind the EVs to make sure the door is well closed." or answer_15 == "D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals.")):
                return"(10:45:00): EVA 1 shows confusion and shortness of breath due to lack of pressure adaptation."
            elif (answer_12 == "C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)" and answer_15 == "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration."):
                return "(10:35:00): EVA 1 has discomfort in ears and sinuses."
            elif (answer_12 == "C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)" and (answer_15 == "B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock." or answer_15 == "C. Instruct CAPCOM to remind the EVs to make sure the door is well closed." or answer_15 == "D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals.")):
                return"(10:35:00): EVA 1 shows chest pain and shortness of breath due to confusion."
    elif inject_id == "Inject 3":
            return("""(11:05:00)
        Days before there was a manoeuvre of the Lunar Gateway to avoid a possible collision with an object.
        But the USSTRATCOM informs the MCC TOPO flight controller with a Conjunction Data Message
        (time of closest approach, probability of collision, and miss distance). The object changed trajectory,
        there’s a probability > 0.01% of collision. The CARA program changes the object’s label from yellow to red.
        Possible collision within 1 hour. PDAM (Predetermined Debris Avoidance Maneuver) isn’t possible.
        """)
    else:
        return "_No prompt defined for {inject_id}_"

import re

def get_current_decision():
    """
    Returns the dict for the currently‐active decision/inject 
    based on session_state.current_decision_index.
    """
    qs = st.session_state.all_questions or []
    i  = st.session_state.current_decision_index - 1
    return qs[i]



# -------------------------------------------------------- Saving Answers to DB ---------------------------------------------------
def get_correct_answer(inject: str):
    _ensure_decision_index()
    decision = st.session_state.decision_index.get(inject.strip().lower())
    if not decision:
        return ""
    role = st.session_state.get("dm_role","")
    rs = decision.get("role_specific")
    if rs:
        # 1) tenta correct específico do role
        if role in rs and isinstance(rs[role], dict):
            return rs[role].get("correct", decision.get("correct",""))
        # 2) fallback: se algum bloco tem 'correct'
        for sub in rs.values():
            if isinstance(sub, dict) and "correct" in sub:
                return sub["correct"]
    return decision.get("correct","")


def apply_vital_consequences(answer_text: dict):
    FD_2 = get_role_decision_answer("Decision 2", "FD")
    CAPCOM_5 = get_role_decision_answer("Decision 5", "CAPCOM")
    FS_8 = get_role_decision_answer("Decision 8", "FS")
    CAPCOM_9 = get_role_decision_answer("Decision 9", "CAPCOM")
    FS_10 = get_role_decision_answer("Decision 10", "FS")
    FE2_14 = get_role_decision_answer("Decision 14", "FE-2(IV1)")
    FD_15 = get_role_decision_answer("Decision 15", "FD")
    FD_12 = get_role_decision_answer("Decision 12", "FD")
    FD_16 = get_role_decision_answer("Decision 16", "FD")
    FS_19 = get_role_decision_answer("Decision 21", "FS")
    FS_21 = get_role_decision_answer("Decision 21", "FS")
    FS_23 = get_role_decision_answer("Decision 23", "FS")
    commander_18 = get_role_decision_answer("Decision 18", "Commander (CMO,IV2)")
    commander_17 = get_role_decision_answer("Decision 17", "Commander (CMO,IV2)")

    effects = {}

    # 1. Default vitals at start: EVA1 and EVA2 show vitals, others = offline
    effects["FE-1(EV1)"] = {
        "bp": "120/72 mmHg", "spo2": "98%", "hr": "85 bpm", "rr": "15 rpm",
        "co2": "40 mmHg", "ecg": "Normal", "status": "online"
    }
    effects["FE-3(EV2)"] = {
        "bp": "118/70 mmHg", "spo2": "97%", "hr": "82 bpm", "rr": "14 rpm",
        "co2": "39 mmHg", "ecg": "Normal", "status": "online"
    }
    effects["Commander (CMO,IV2)"] = {"status": "offline"}
    effects["FE-2(IV1)"] = {"status": "offline"}


    # 3. After Inject 2 if Decision 15 ≠ A → drop SpO2
    if FD_2 is not None:
        effects["FE-1(EV1)"]["hr"] = "92 bpm"
        effects["FE-1(EV1)"]["rr"] = "20 rpm"
    
    if CAPCOM_5 is not None:
        effects["FE-1(EV1)"]["hr"] = "95 bpm"
        effects["FE-1(EV1)"]["rr"] = "22 rpm"
        effects["FE-1(EV1)"]["bp"] = "127/77 mmHg"
        effects["FE-1(EV1)"]["spo2"] = "98%"
    
    if FS_8 is not None:
        effects["FE-1(EV1)"]["hr"] = "97 bpm"
        effects["FE-1(EV1)"]["rr"] = "20 rpm"
        effects["FE-1(EV1)"]["bp"] = "130/80 mmHg"
        effects["FE-1(EV1)"]["spo2"] = "99%"
    
    if CAPCOM_9 is not None:
        effects["FE-1(EV1)"]["hr"] = "95 bpm"
        effects["FE-1(EV1)"]["rr"] = "19 rpm"
        effects["FE-1(EV1)"]["bp"] = "131/82 mmHg"
        effects["FE-1(EV1)"]["spo2"] = "97%"
    
    if FS_10 is not None:
        effects["FE-1(EV1)"]["hr"] = "93 bpm"
        effects["FE-1(EV1)"]["rr"] = "23 rpm"
        effects["FE-1(EV1)"]["bp"] = "135/87 mmHg"
        effects["FE-1(EV1)"]["spo2"] = "99%"
    
    if FE2_14 is not None:
        effects["FE-1(EV1)"]["hr"] = "91 bpm"
        effects["FE-1(EV1)"]["rr"] = "22 rpm"
        effects["FE-1(EV1)"]["bp"] = "137/90 mmHg"
        effects["FE-1(EV1)"]["spo2"] = "99%"
    

    if FD_15 is not None and FD_15 != "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration.":
        effects["FE-1(EV1)"]["spo2"] = "88%"
        effects["FE-1(EV1)"]["hr"] = "92 bpm"
        if FD_12 is not None and FD_12 == "A. Partial pressurisation finishing at 12 psi (~10 min.)":
            if FD_16 is not None:
                effects["FE-1(EV1)"]["hr"] = "100 bpm"
                effects["FE-1(EV1)"]["rr"] = "28 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "88%"
            if commander_18 is not None:
                effects["FE-1(EV1)"]["status"] = "offline"
            if FS_19 is not None:
                effects["FE-1(EV1)"] = {
                    "status": "online", "bp": "134/82 mmHg", "spo2": "87%", "hr": "101 bpm",
                    "rr": "30 rpm", "ecg": "Normal"
                }
                effects["FE-1(EV1)"]["temp"] = "98.3 °F or 36.8ºC"
            if FS_21 is not None:
                effects["FE-1(EV1)"]["hr"] = "95 bpm"
                effects["FE-1(EV1)"]["rr"] = "35 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "86%"
            if FS_23 is not None:
                effects["FE-1(EV1)"]["spo2"] = "96%"
                effects["FE-1(EV1)"]["hr"] = "91 bpm"
                effects["FE-1(EV1)"]["rr"] = "22 rpm"
                effects["FE-1(EV1)"]["bp"] = "130/80 mmHg"

        if FD_12 is not None and FD_12 == "B.Normal repressurization (~15 min.)":
            if commander_17 is not None:
                effects["FE-1(EV1)"]["hr"] = "100 bpm"
                effects["FE-1(EV1)"]["rr"] = "28 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "88%"
            if commander_18 is not None:
                effects["FE-1(EV1)"]["status"] = "offline"
            if FS_19 is not None:
                effects["FE-1(EV1)"] = {
                    "status": "online", "bp": "134/82 mmHg", "spo2": "87%", "hr": "101 bpm",
                    "rr": "30 rpm", "ecg": "Normal"
                }
                effects["FE-1(EV1)"]["temp"] = "98.3 °F or 36.8ºC"
            if FS_21 is not None:
                effects["FE-1(EV1)"]["hr"] = "95 bpm"
                effects["FE-1(EV1)"]["rr"] = "35 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "86%"
            if FS_23 is not None:
                effects["FE-1(EV1)"]["spo2"] = "96%"
                effects["FE-1(EV1)"]["hr"] = "91 bpm"
                effects["FE-1(EV1)"]["rr"] = "22 rpm"
                effects["FE-1(EV1)"]["bp"] = "130/80 mmHg"
                effects["FE-1(EV1)"]["glucose"] = "135 mg/dL"
                effects["FE-1(EV1)"]["electrolytes"] = "Na 132 mmol/L; K 4.2 mmol/L; Ca 8.5 mg/dL"

        if FD_12 is not None and FD_12 == "C.Emergency pressurisation at a rate of 1.0 psi/second (~5 min)":
            if commander_17 is not None:
                effects["FE-1(EV1)"]["hr"] = "100 bpm"
                effects["FE-1(EV1)"]["rr"] = "28 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "88%"
            if commander_18 is not None:
                effects["FE-1(EV1)"]["status"] = "offline"
            if FS_19 is not None:
                effects["FE-1(EV1)"] = {
                    "status": "online", "bp": "134/82 mmHg", "spo2": "87%", "hr": "101 bpm",
                    "rr": "30 rpm", "ecg": "Normal"
                }
                effects["FE-1(EV1)"]["temp"] = "98.3 °F or 36.8ºC"
            if FS_21 is not None:
                effects["FE-1(EV1)"]["hr"] = "95 bpm"
                effects["FE-1(EV1)"]["rr"] = "35 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "86%"
            if FS_23 is not None:
                effects["FE-1(EV1)"]["spo2"] = "96%"
                effects["FE-1(EV1)"]["hr"] = "91 bpm"
                effects["FE-1(EV1)"]["rr"] = "22 rpm"
                effects["FE-1(EV1)"]["bp"] = "130/80 mmHg"
                effects["FE-1(EV1)"]["glucose"] = "135 mg/dL"
                effects["FE-1(EV1)"]["electrolytes"] = "Na 132 mmol/L; K 4.2 mmol/L; Ca 8.5 mg/dL"
                effects["FE-1(EV1)"]["nihss"] = "NIHSS = 11"
                effects["FE-1(EV1)"]["diagnostic"] = "Ultrasound shows pneumothorax of <20% lung volume"
    

    if FD_15 is not None and FD_15 == "A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration.":
        effects["FE-1(EV1)"]["spo2"] = "98%"
        effects["FE-1(EV1)"]["hr"] = "92 bpm"
        if commander_17 is not None:
                effects["FE-1(EV1)"]["hr"] = "90 bpm"
                effects["FE-1(EV1)"]["rr"] = "20 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "99%"
        if commander_18 is not None:
                effects["FE-1(EV1)"]["status"] = "offline"
        if FS_19 is not None:
                effects["FE-1(EV1)"] = {
                    "status": "online", "bp": "134/82 mmHg", "spo2": "100%", "hr": "93 bpm",
                    "rr": "21 rpm", "ecg": "Normal"
                }
                effects["FE-1(EV1)"]["temp"] = "98.3 °F or 36.8ºC"
        if FS_21 is not None:
                effects["FE-1(EV1)"]["hr"] = "91 bpm"
                effects["FE-1(EV1)"]["rr"] = "22 rpm"
                effects["FE-1(EV1)"]["bp"] = "135/86 mmHg"
                effects["FE-1(EV1)"]["spo2"] = "99%"
        if FS_23 is not None:
                effects["FE-1(EV1)"]["spo2"] = "98%"
                effects["FE-1(EV1)"]["hr"] = "91 bpm"
                effects["FE-1(EV1)"]["rr"] = "22 rpm"
                effects["FE-1(EV1)"]["bp"] = "130/80 mmHg"
                effects["FE-1(EV1)"]["glucose"] = "135 mg/dL"
                effects["FE-1(EV1)"]["electrolytes"] = "Na 132 mmol/L; K 4.2 mmol/L; Ca 8.5 mg/dL"
                effects["FE-1(EV1)"]["nihss"] = "NIHSS = 11"


    # Salvar efeitos no estado
    st.session_state["vital_effects"] = effects
