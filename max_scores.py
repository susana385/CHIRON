import os
from itertools import product
#from supabase import create_client
from supabase_client import supabase
import questionnaire1
from questionnaire1 import (
    decisions1to13,
    decisions14to23, decisions24to28,
    decisions29to32, decisions33to34, decisions35to43,
)
# from dotenv import load_dotenv
# import os

# # point load_dotenv at your env-file
# load_dotenv(dotenv_path="supabase.env")

# # now os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY") will be set
# url = os.getenv("SUPABASE_URL")
# key = os.getenv("SUPABASE_KEY")

# load_dotenv(dotenv_path="supabase.env")
# import os
# print("URL:", os.getenv("SUPABASE_URL"))
# print("KEY:", os.getenv("SUPABASE_KEY"))



# 1) Pull out the FD key‐decision options exactly as you already do:
def options_for(prefix, blocks):
    for d in blocks:
        if d["inject"].startswith(prefix):
            return d.get("options", [])
    return []

opt7   = options_for("Decision 7",  decisions1to13)
opt13  = options_for("Decision 13", decisions1to13)
all14  = [d for blk in decisions14to23.values() for d in blk]
opt23  = options_for("Decision 23", all14)
all33  = [d for blk in decisions33to34.values() for d in blk]
opt34  = options_for("Decision 34", all33)

# 2) Categories & roles
CATS = [
    "Basic_Life_Support","Primary_Survey","Secondary_Survey",
    "Definitive_Care","Crew_Roles_Communication","Systems_Procedural_Knowledge"
]
ROLES = ["FE-3 (EVA2)","Commander (CMO, IV2)","FE-1 (EVA1)",
         "FE-2 (IV1)","FD","FS","BME","CAPCOM"]

def max_for_questions(questions):
    """
    Returns for each role→category a dict with:
      'max_value': sum of best points,
      'contributors': list of inject names that drove that sum
    """
    out = {
      r: {c: {"max_value": 0.0, "contributors": []} for c in CATS}
      for r in ROLES
    }

    for d in questions:
        inj = d["inject"]
        for r in ROLES:
            # pick the right scores list, falling back if missing
            if "role_specific" in d and r in d["role_specific"]:
                entry = d["role_specific"][r]
                sco_list = entry.get("scores", d.get("scores", []))
                multi    = entry.get("multi", d.get("multi", False))
            else:
                sco_list = d.get("scores", [])
                multi    = d.get("multi", False)

            for cat in CATS:
                # gather all the option‐scores for this category
                vals = [s.get(cat, 0.0) for s in sco_list]

                if multi:
                    # sum the top 5 (or fewer) choices
                    top_n = sorted(vals, reverse=True)[:5]
                    best = sum(top_n)
                else:
                    # single‐choice question
                    best = max(vals, default=0.0)

                if best > 0:
                    out[r][cat]["max_value"]  += best
                    out[r][cat]["contributors"].append(inj)

    return out


# 3) Supabase client
# url = os.environ["SUPABASE_URL"]
# key = os.environ["SUPABASE_KEY"]
#sb  = create_client(url, key)

to_upsert = []

# 4) Build all 72 scenarios
for a7, a13, a23, a34 in product(opt7, opt13, opt23, opt34):
    code = f"7({a7})&13({a13})&23({a23})&34({a34})"
    # assemble full question list
    qs = []
    qs += decisions1to13
    qs += decisions14to23.get((a7,a13), [])
    qs += decisions24to28.get((a7,a13), [])
    qs += decisions29to32.get((a7,a13), [])
    qs += decisions33to34.get((a7,a13,a23), [])
    qs += decisions35to43.get((a7,a13,a23,a34), [])

    maxima = max_for_questions(qs)

    for role, catmap in maxima.items():
        for cat, info in catmap.items():
            to_upsert.append({
                "scenario_code": code,
                "role":          role,
                "category":         f"{cat}_total",
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



