from dotenv import load_dotenv
load_dotenv("supabase.env")

try:
    import streamlit as st
    class _DummySecrets:
        def get(self, key, default=None):
            # always fall back to the real env var
            return os.getenv(key, default)
    st.secrets = _DummySecrets()
except ImportError:
    # if streamlit isn't even installed, no problem
    pass
import os
from itertools import product
import os
from itertools import product
from supabase import create_client

# 1) Load from env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY as environment variables")

# 2) Initialize the client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


decisions1to15 = [
    {"inject": "Decision 1 (9:50:00): ",
        "role_specific": {
            "Commander(CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2(IV1)": {"text": " Keep the normal activities going."},
            "FE-1(EV1)": {"text": " Keep the normal activities going."},
            "FE-3(EV2)": {"text": " Keep the normal activities going."},
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
            "Commander(CMO,IV2)": {"text": " Report your positive status only when CAPCOM asks."},
            "FE-2(IV1)": {"text": "Report your positive status only when CAPCOM asks "},
            "FE-1(EV1)": {"text": "You are now starting the fixation of the new component of data collection to the station. Communicate what you’re doing only when asked by the CAPCOM."},
            "FE-3(EV2)": {"text": "You are now on a different location than FE-1(EV1), checking on the status of other colection device. Report the positive status of this device only when asked by the CAPCOM."},
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
            "Commander(CMO,IV2)": {"text": "Keep the normal activities going."},
            "FE-2(IV1)": {"text": "Keep the normal activities going."},
            "FE-1(EV1)": {"text": "2 hour into EVA, sundendly you feel numbness on your right arm while performing a vigurous task with that arm. What should you do?", "options": ["A. Communicate with CAPCOM to report what you fell.","B. Initiate return to the crew lock while continuing to communicate with MCC.","C. Check for suit malfunctions before making any further decisions.","D. Communicate with Commander in the station to report what you fell."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300 },
            "FE-3(EV2)": {"text": " Keep the normal activities going."},
            "FD": {"text": " Keep the normal activities going."},
            "FS": {"text": " Keep the normal activities going." },
            "BME": {"text": " Keep the normal activities going."},
            "CAPCOM": {"text": " Keep the normal activities going."},
        }
    },

    {"inject": "Decision 4 (10:00:30): ", 
        "role_specific": {
            "Commander(CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2(IV1)": {"text": " Keep the normal activities going."},
            "FE-1(EV1)": {"text": "Report to CAPCOM the numbness in your right arm."},
            "FE-3(EV2)": {"text": " Keep the normal activities going."},
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
            "Commander(CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2(IV1)": {"text": " Keep the normal activities going."},
            "FE-1(EV1)": {"text": "You’re now in a private consultation with the flight surgeon. Meanwhile, you report that the numbness could be from the strenuous work you were performing with that arm."},
            "FE-3(EV2)": {"text": "Keep the normal activities going."},
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
            "Commander(CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2(IV1)": {"text": " Keep the normal activities going."},
            "FE-1(EV1)": {"text": "After 15 min, the symptoms worsen, now you notice weakness in your right arm. You’re still in the private consultation with the fligh surgeon please report it."},
            "FE-3(EV2)": {"text": " Keep the normal activities going."},
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
            "Commander(CMO,IV2)": {"text": " Keep the normal activities going."},
            "FE-2(IV1)": {"text": " Keep the normal activities going."},
            "FE-1(EV1)": {"text": "Wait for more instructions."},
            "FE-3(EV2)": {"text": " Keep the normal activities going."},
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
            "Commander(CMO,IV2)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-2(IV1)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-1(EV1)": {"text": "Wait for more instructions."},
            "FE-3(EV2)": {"text": "Wait for instructions."},
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
            "Commander(CMO,IV2)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-2(IV1)": {"text": "Monitor the situation and assist with anything that the rest of the team might need."},
            "FE-1(EV1)": {"text": "You notice that you can’t feel the right part of you’re face, which makes it difficult to speak."},
            "FE-3(EV2)": {"text": "After 20 minutes, you get close to FE-1(EV1) and notice that he is presenting some facial asymmetry, specifically drooping on the right side of the face. You perform the FAST method with positive results; Report this information to CAPCOM. "},
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
            "Commander(CMO,IV2)": {"text": "Upon receiving the orders from CAPCOM and in discussion with FE-2(IV1), what technical procedures must be prioritised to ensure a safe and efficient re-entry to the airlock during this contingency?", "options": ["A. Ensure suit telemetry is stable, initiate translation path clearance, verify airlock integrity, and coordinate repress sequence timing with MCC.","B. Switch EVA1’s suit to full manual mode to reduce data traffic and speed up the airlock cycle.","C. Instruct EVA2 to enter the airlock first to begin repressurization prep while EVA1 follows at their own pace.","D. Initiate full depressurisation of the airlock while EVA1 is still en route to save time."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2(IV1)": {"text": "Upon receiving the orders from CAPCOM and in discussion with the Commander, what technical procedures must be prioritised to ensure a safe and efficient re-entry to the airlock during this contingency?", "options": ["A. Ensure suit telemetry is stable, initiate translation path clearance, verify airlock integrity, and coordinate repress sequence timing with MCC.","B. Switch EVA1’s suit to full manual mode to reduce data traffic and speed up the airlock cycle.","C. Instruct EVA2 to enter the airlock first to begin repressurization prep while EVA1 follows at their own pace.","D. Initiate full depressurisation of the airlock while EVA1 is still en route to save time."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "Receiving information from the CAPCOM, You are now escorting EVA1 back to the airlock. What is the most effective way to support EVA1 during this phase?", "options": ["A. Maintain physical proximity, monitor EVA1’s mobility and responsiveness, and provide verbal reassurance while relaying updates to CAPCOM.","B. Minimize communication to reduce stress and interference with MCC telemetry.","C. Leave EVA1 briefly to speed up airlock prep steps from outside.","D. Focus on finishing any remaining mission objectives while EVA1 proceeds slowly toward the airlock."],
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
            "Commander(CMO,IV2)": {"text": " Keep preparing for the reentry of the EVs."},
            "FE-2(IV1)": {"text": " Keep preparing for the reentry of the EVs."},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "How should you transport FE-1(EV1) to the crew lock?", "options": ["A. Tow EVA1 using a tether."," B. Carry EVA1 using the SAFER unit."," C. EVA1 should self-rescue using their propulsion system."," D. Assist EVA1 into the MMSEV (Miniature Modular Space Exploration Vehicle)."],
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
            "Commander(CMO,IV2)": {"text": "While the EVs are returning, what should you and FE-2(IV1) do to prepare for their arrival?", "options": ["A. The Commander can confirm the medical emergency protocols with the Flight Surgeon; Flight Engineer 2 can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed","B. The commander  and Flight Engineer 2 can initiate a full cabin depressurisation to speed up EVA2’s reentry.","C. The Flight Engineer 2 can leave the airlock hatch open and wait to pull the patient in manually; the Commander gathers information about the medical emergency","D. The crew can begin unrelated maintenance tasks to stay on schedule."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2(IV1)": {"text": "While the EVs are returning, what should you and the Commander do to prepare for their arrival?", "options": ["A. The Commander can confirm the medical emergency protocols with the Flight Surgeon; Flight Engineer 2 can get the medical equipment needed and the instructions on how to adjust airlock repressurization speed","B. The commander  and Flight Engineer 2 can initiate a full cabin depressurisation to speed up EVA2’s reentry.","C. The Flight Engineer 2 can leave the airlock hatch open and wait to pull the patient in manually; the Commander gathers information about the medical emergency","D. The crew can begin unrelated maintenance tasks to stay on schedule."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":1, "Systems_Procedural_Knowledge":0}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.3, "Systems_Procedural_Knowledge":0}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0.5, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "If asked the last known normal of the FE-1(EV1) state was 10:16:00"},
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
            "Commander(CMO,IV2)": {"text":"Start preparing for the crew lock for repressurization."},
            "FE-2(IV1)": {"text": "What medical equipment should the Crew Medical Officer (CMO) prepare (maxim. 5)?", 
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
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "You’re almost arriving to the Airlock."},
            "FD": {"text": "Start preparing for the crew lock for repressurization."},
            "FS": {"text": "Give assistance to the IVs inside the station."},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Start preparing for the crew lock for repressurization"},
        }
    },

    {"inject": "Decision 15 (10:46:00): ", 
    "text": "TEVs arrive at the crew lock. Due to the high-stress environment, it’s crucial that CAPCOM reminds EVAs of an important step in their training.", "options": ["A. Instruct CAPCOM to remind the EVs to breathe frequently, do not sustain respiration.","B. Instruct CAPCOM to remind the EVs to pay attention to the temperature of the Airlock.","C. Instruct CAPCOM to remind the EVs to make sure the door is well closed.","D. Instruct CAPCOM to remind the BME to keep monitoring EV1 vital signals."],
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
            "Commander(CMO,IV2)": {"text": "At 10:58 AM, you find that the hatch between the crew lock and the station cannot be opened because the pressure readings differ between the two locks. Communicate the situation with the MCC."},
            "FE-2(IV1)": {"text": "At 10:58 AM, you find that the hatch between the crew lock and the station cannot be opened because the pressure readings differ between the two locks. Communicate the situation with the MCC."},
            "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3(EV2)": {"text": "Wait for the repressurization to be completed. Keep monitoring EV1"},
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
            "Commander(CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2(IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
            "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
            "FS": {"text": "Monitor FE-1(EV1) vital signs."},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Report the information given by the IVs."},
        }
    },

    {"inject": "Decision 18 (11:02:00): ", 
        "role_specific": {
            "Commander(CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2(IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
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
            "Commander(CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2(IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
            "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
            "FS": {"text": "Monitor FE-1(EV1) vital signs."},
            "BME": {"text": "Monitor FE-1(EV1) vital signs."},
            "CAPCOM": {"text": "Report the information given by the IVs."},
        }
    },

    {"inject": "Decision 18 (10:52:00): ", 
        "role_specific": {
            "Commander(CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-2(IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
     "scores":  [
      {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
      {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
      {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
      {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
    ],"max_time": 300},
            "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
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
            "Commander(CMO,IV2)": {"text": " Wait for more information"},
            "FE-2(IV1)": {"text": " Wait for more information"},
            "FE-1(EV1)": {"text": "Due to your simptoms you’re no longer able to participate in any discussion"},
            "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander(CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
            "Commander(CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2(IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander(CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander(CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "Repressurization is now completed. Discuss with FE-2(IV1), which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "Repressurization is now completed. Discuss with the Commander, which sequence of actions must be completed before the hatch can be safely opened?", "options": ["A. The repressurization was successful at 12 psi, so ignore the pressure difference and open the hatch immediately.","B. To open the door both sides need to be at the same pressure. This way, continue with the repressurization until the 14 psi.","C. The pressure sensors must be malfunctioning since 12 psi is sufficient—override the sensor data and open the hatch.","D. The hatch should be opened anyway while the system automatically adjusts for the pressure difference."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
                "FD": {"text": "Give support to IVs according to the information transmited by CAPCOM"},
                "FS": {"text": "Monitor FE-1(EV1) vital signs."},
                "BME": {"text": "Monitor FE-1(EV1) vital signs."},
                "CAPCOM": {"text": "Report the information given by the IVs."},
            }
        },

        {"inject": "Decision 18 (11:07:00): ", 
            "role_specific": {
                "Commander(CMO,IV2)": {"text": "You and FE-2(IV1) proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-2(IV1)": {"text": "You and Commander proceed with the opening of the hatch. What are you doing first?", "options": ["A. Doff the EVA1 suit.","B. Doff the EVs suits at the same time.","C. Doff the EVA 2 suit.","D. Give proper medication to EVA 1."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":1, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0.5, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0.3, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "The repressurization is now completed wait for the hatch."},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
            "Commander(CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2(IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
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
                "Commander(CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2(IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": " Wait for more information"},
                "FE-2(IV1)": {"text": " Wait for more information"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
            "Commander(CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2(IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
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
                "Commander(CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2(IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
            "Commander(CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2(IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
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
                "Commander(CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2(IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
            "Commander(CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2(IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
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
                "Commander(CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2(IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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
                "Commander(CMO,IV2)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-2(IV1)": {"text": "You are starting the restrainment of FE-1(EV1) to the Crew Medical Restraint System and measure vital signs of FE-1(EV1)"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You start preparing to realocat the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "You start preparing to realocat the site of treatment to the CRV."},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": "Start relocating the site of treatment to the CRV."},
                "FE-2(IV1)": {"text": "Start relocating the site of treatment to the CRV"},
                "FE-1(EV1)": {"text": "You complain of chest pain. Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re still inside the EVA suit. This way, you need to wait for help to doff the suit."},
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
                "Commander(CMO,IV2)": {"text": " You’re now assessing EVA 1 status."},
                "FE-2(IV1)": {"text": "You’re now unsuiting EVA2"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re now being unsuited from the EVA."},
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
            "Commander(CMO,IV2)": {"text":"You’re in communication with MCC"},
            "FE-2(IV1)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-3(EV2), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #D
        ],"max_time": 300},
            "FE-1(EV1)": {"text": "Due to your simptoms you have difficulties communicating but you can still understand the situation."},
            "FE-3(EV2)": {"text": "After completing the tasks communicated by the CAPCOM. You now start the relocation to the CRV. In discution with FE-2(IV1), how are you transporting FE-1(EV1)?", "options": ["A. Attach EVA 1 securely to the Crew Mobility Restraint (CMR) system to minimise movement and maintain stability throughout transit.","B. Manually guide EVA 1 to the Crew Rescue Vehicle (CRV), ensuring controlled progress along a predetermined path.","C. Integrate both systems—first restrain EVA 1 using the CMR, then guide him toward the CRV—to maximise safety by merging immobilisation with controlled movement.","D. Allow EVA 1 to use a SAFER (Simplified Aid for EVA Rescue) unit for self-mobility while remaining tethered to a guideline, providing flexibility in movement coupled with a safety backup."],
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
                "Commander(CMO,IV2)": {"text": "You perform the orders communicated by CAPCOM."},
                "FE-2(IV1)": {"text": "You, FE-3(EV2) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
        "scores":  [
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":1}, #A
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.3}, #B
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0}, #C
        {"Basic_Life_Support":0,"Primary_Survey":0, "Secondary_Survey":0, "Definitive_Care":0,"Crew_Roles_Communication":0, "Systems_Procedural_Knowledge":0.5}, #D
        ],"max_time": 300},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You, FE-2(EV1) and FE-1(EV1) are now inside the CRV.  Which of the following sets of actions is required to properly prepare the Crew Rescue Vehicle (CRV) for a possible isolation scenario?", "options": ["A. Close the hatches, don IV spacesuits, prepare CRV communications and systems.","B. Open all external hatches to equalise pressure and bypass internal communications.","C. Activate emergency thrusters, disengage life-support controls, and initiate a full system shutdown.","D. Seal off the cabin ventilation, disable navigation systems, and switch to manual engine overrides."],
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
                "Commander(CMO,IV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation."},
                "FE-2(IV1)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
                "FE-1(EV1)": {"text": " Due to your simptoms you’re no longer able to participate in any discussion"},
                "FE-3(EV2)": {"text": "You’re in a joint communication between the flight director, CAPCOM and the astronauts the possible collision situation"},
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

ALL_ROLES = ["FE-3(EV2)","Commander(CMO,IV2)","FE-1(EV1)","FE-2(IV1)","FD","FS","BME","CAPCOM"]


def options_for(prefix, blocks):
    for d in blocks:
        if d["inject"].startswith(prefix):
            return d.get("options", [])
    return []

opt12 = options_for("Decision 12", decisions1to15)
opt15 = options_for("Decision 15", decisions1to15)

# 2) Categories & roles
CATS = [
    "Basic_Life_Support","Primary_Survey","Secondary_Survey",
    "Definitive_Care","Crew_Roles_Communication","Systems_Procedural_Knowledge"
]



# 3) Scoring logic remains unchanged

def max_for_questions(questions):
    out = {
      r: {c: {"max_value": 0.0, "contributors": []} for c in CATS}
      for r in ALL_ROLES
    }

    for d in questions:
        inj = d["inject"]
        for r in ALL_ROLES:
            if "role_specific" in d and r in d["role_specific"]:
                entry = d["role_specific"][r]
                sco_list = entry.get("scores", d.get("scores", []))
                multi    = entry.get("multi", d.get("multi", False))
            else:
                sco_list = d.get("scores", [])
                multi    = d.get("multi", False)

            for cat in CATS:
                vals = [s.get(cat, 0.0) for s in sco_list]
                if multi:
                    top_n = sorted(vals, reverse=True)[:5]
                    best = sum(top_n)
                else:
                    best = max(vals, default=0.0)

                if best > 0:
                    out[r][cat]["max_value"]  += best
                    out[r][cat]["contributors"].append(inj)
    return out

# 4) Build upsert data based on new flow

to_upsert = []

def prefix(ans: str) -> str:
    return ans.split(".")[0].strip().lower()

# Iterate over all combinations of FD’s Decision 12 & Decision 15 options
for a12, a15 in product(opt12, opt15):
    p12, p15 = prefix(a12), prefix(a15)
    code = f"{p12}12,{p15}15"

    # Assemble scenario questions:
    qs = []
    qs += decisions1to15
    if a12.startswith("A"):
        qs += decision16_12A[:]
    elif a12.startswith("B"):
        qs += decisions17to18_12B[:]
    elif a12.startswith("C"):
        qs += decisions17to19_12C[:]
    qs += decisions17to26.get((a12, a15), [])

    maxima = max_for_questions(qs)

    for role, catmap in maxima.items():
        for cat, info in catmap.items():
            to_upsert.append({
                "scenario_code": code,
                "role":          role,
                "category":      f"{cat}_total",
                "max_value":     info["max_value"],
                "contributors":  info["contributors"],
            })

# 5) Batch upsert
for i in range(0, len(to_upsert), 200):
    batch = to_upsert[i:i+200]
    supabase.from_("max_scores") \
      .upsert(batch, on_conflict="scenario_code,role,category") \
      .execute()

print("✅ max_scores populated with contributors.")




