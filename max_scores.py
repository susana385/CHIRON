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
import questionnaire1
from questionnaire1 import (
    decisions1to15,
    decision16_12A,
    decisions17to18_12B,
    decisions17to19_12C,
    decisions17to26,
)


# 1) Load from env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY as environment variables")

# 2) Initialize the client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


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
ROLES = [
    "FE-3 (EVA2)","Commander (CMO, IV2)","FE-1 (EVA1)",
    "FE-2 (IV1)","FD","FS","BME","CAPCOM"
]

# 3) Scoring logic remains unchanged

def max_for_questions(questions):
    out = {
      r: {c: {"max_value": 0.0, "contributors": []} for c in CATS}
      for r in ROLES
    }

    for d in questions:
        inj = d["inject"]
        for r in ROLES:
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




