# generate_sql.py

import os
import teamwork
import sqlite3
import questionnaire1
import streamlit as st
import json
import pandas as pd
from typing import Any, Callable
from questionnaire1 import compute_team_breakdown
from questionnaire1 import compute_totals
from questionnaire1 import st as qst
from questionnaire1 import question_text as qmap



def init_db(simulation_name: str):
    """Create (or open) <simulation_name>.db and ensure all tables exist."""
    db_path = f"{simulation_name}.db"
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    # 1) answers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS answers (
      id                   INTEGER PRIMARY KEY AUTOINCREMENT,
      simulation_name      TEXT    NOT NULL,
      role                 TEXT    NOT NULL,
      inject               TEXT    NOT NULL,
      question_text        TEXT    NOT NULL,
      answer_text          TEXT    NOT NULL,
      score                 REAL,
      Basic_Life_Support    REAL,
      Primary_Survey        REAL,
      Secondary_Survey       REAL,
      Definitive_Care       REAL,         
      Crew_Roles_Communication       REAL,
      Systems_Procedural_Knowledge   REAL,
      response_time_s       INTEGER,
      submitted_at          DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3) individual_scores
    cur.execute("""
    CREATE TABLE IF NOT EXISTS individual_scores (
      id                      INTEGER PRIMARY KEY AUTOINCREMENT,
      simulation_name         TEXT    NOT NULL,
      role                    TEXT    NOT NULL,
      Basic_Life_Support      REAL,
      Primary_Survey          REAL,
      Secondary_Survey         REAL,
      Definitive_Care         REAL,
      medical_knowledge       REAL,
      Crew_Roles_Communication         REAL,
      Systems_Procedural_Knowledge      REAL,
      procedural_knowledge    REAL,
      mental                  INTEGER,
      physical                INTEGER,
      temporal                INTEGER,
      performance             INTEGER,
      effort                  INTEGER,
      frustration             INTEGER,
      taskload                INTEGER,
      computed_at             DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4) team_scoring
    cur.execute("DROP TABLE IF EXISTS team_scoring")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS team_scoring (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,
      simulation_name  TEXT    NOT NULL,
      criterion        TEXT    NOT NULL,
      total_score            REAL    NOT NULL,
      Basic_Life_Support_team      REAL,
      Primary_Survey_team          REAL,
      Secondary_Survey_team        REAL,
      Definitive_Care_team         REAL,
      medical_knowledge_team       REAL,
      Crew_Roles_Communication_team         REAL,
      Systems_Procedural_Knowledge_team     REAL,
      procedural_knowledge_team    REAL,
      mental_team          REAL,
      physical_team        REAL,
      temporal_team        REAL,
      performance_team     REAL,
      effort_team          REAL,
      frustration_team     REAL, 
      taskload             REAL,
      entered_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
      submitted_at     DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS supervisor_scoring (
      id                     INTEGER PRIMARY KEY AUTOINCREMENT,
      simulation_name     TEXT    NOT NULL,
      supervisor          TEXT    NOT NULL,
      leadership_score    INTEGER,
      teamwork_score      INTEGER,
      task_score          INTEGER,
      overall_score       INTEGER,
      total_score         INTEGER,
      comments            TEXT,
      submitted_at           DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

# at the bottom of generate_sql.py, after your write_team_scoring…

def write_csv_exports(sim_name: str):
    """Dump each table out to a CSV named <sim>_answers.csv, etc."""
    db_path = f"{sim_name}.db"
    conn    = sqlite3.connect(db_path)

    # 1) Read each table
    df_answers = pd.read_sql_query("SELECT * FROM answers", conn)
    df_indiv   = pd.read_sql_query("SELECT * FROM individual_scores", conn)
    df_team    = pd.read_sql_query("SELECT * FROM team_scoring", conn)
    df_sup       = pd.read_sql_query("SELECT * FROM supervisor_scoring", conn)
    conn.close()

    # 2) Write CSVs
    df_answers.to_csv(f"{sim_name}_answers.csv", index=False)
    df_indiv.to_csv  (f"{sim_name}_individual_scores.csv", index=False)
    df_team.to_csv   (f"{sim_name}_team_scoring.csv", index=False)
    df_sup.to_csv    (f"{sim_name}_supervisor_score.csv", index=False) 
    print(f"✅ Wrote CSVs: {sim_name}_answers.csv, _individual_scores.csv, _team_scoring.csv")


def write_answers(sim_name: str,answers: dict[str, Any],answer_times: dict[str, int],all_questions: list[dict],dm_role: str,get_score_breakdown: Callable[[str, Any], dict[str, float]]):
    conn = sqlite3.connect(f"{sim_name}.db")
    cur  = conn.cursor()
    # drop the qst.session_state stuff
    qmap = { q["inject"]: q.get("text","") for q in all_questions }

    for inject, answer in answers.items():
        if inject.startswith("Inject "):
             continue

        qtext     = qmap.get(inject, inject)
        elapsed   = answer_times.get(inject)
        breakdown = get_score_breakdown(inject, answer)
        serialized = json.dumps(answer) if isinstance(answer, list) else answer

        cur.execute(
            """
            INSERT INTO answers
              (simulation_name, role, inject, question_text, answer_text,
               score,
               Basic_Life_Support, Primary_Survey, Secondary_Survey ,
               Definitive_Care, Crew_Roles_Communication,
               Systems_Procedural_Knowledge,
               response_time_s)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                sim_name, dm_role, inject, qtext, serialized,
                breakdown["total_score"],
                breakdown["Basic_Life_Support"],
                breakdown["Primary_Survey"],
                breakdown["Secondary_Survey"],
                breakdown["Definitive_Care"],
                breakdown["Crew_Roles_Communication"],
                breakdown["Systems_Procedural_Knowledge"],
                elapsed,
            )
        )

    conn.commit()
    conn.close()


def write_individual_scores(sim_name: str,dm_role: str,totals: dict[str, float],tlx_answers: dict[str, int]):
    conn = sqlite3.connect(f"{sim_name}.db")
    cur  = conn.cursor()
    role = dm_role
    totals = compute_totals()

    mental      = tlx_answers.get("Mental Demand",    0)
    physical    = tlx_answers.get("Physical Demand",  0)
    temporal    = tlx_answers.get("Temporal Demand",  0)
    performance = tlx_answers.get("Performance",      0)
    effort      = tlx_answers.get("Effort",           0)
    frustration = tlx_answers.get("Frustration",      0)

    # compute your taskload only if you have all six, else NULL
    if None not in (mental, physical, temporal, performance, effort, frustration):
        taskload = int((mental + physical + temporal + performance + effort + frustration) / 6)
    else:
        taskload = None

    cur.execute("""
      INSERT INTO individual_scores
        (simulation_name, role,
         Basic_Life_Support, Primary_Survey, Secondary_Survey , Definitive_Care,
         medical_knowledge,                   
         Crew_Roles_Communication, Systems_Procedural_Knowledge, 
         procedural_knowledge,                
         mental, physical, temporal, performance,
         effort, frustration, taskload)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,(
      sim_name, role,
      totals.get("Basic_Life_Support", 0.0),
      totals.get("Primary_Survey",     0.0),
      totals.get("Secondary_Survey ",   0.0),
      totals.get("Definitive_Care",    0.0),
      totals.get("medical_knowledge_total",     0.0),
      totals.get("Crew_Roles_Communication",  0.0),
      totals.get("Systems_Procedural_Knowledge", 0.0),
      totals.get("procedural_knowledge_total",     0.0),
      mental, physical, temporal, performance,
      effort, frustration, taskload
    ))

    conn.commit()
    conn.close()


def compute_team_aggregate(sim_name: str) -> dict[str, float]:
    """
    Load every row from individual_scores for this sim_name,
    sum each of the six categories, plus the two domain‐level sums,
    and return a dict with keys exactly matching your team_scoring columns.
    """
    
    conn = sqlite3.connect(f"{sim_name}.db")
    cur  = conn.cursor()

    # sum up each of the six categories from individual_scores
    cur.execute("""
      SELECT
        SUM(Basic_Life_Support),
        SUM(Primary_Survey),
        SUM(Secondary_Survey ),
        SUM(Definitive_Care),
        SUM(Crew_Roles_Communication),
        SUM(Systems_Procedural_Knowledge)
      FROM individual_scores
      WHERE simulation_name = ?
    """, (sim_name,))
    bls, ps, ss, dc, cr, sp = cur.fetchone()

    cur.execute("""
      SELECT
        SUM(mental), SUM(physical), SUM(temporal),
        SUM(performance), SUM(effort), SUM(frustration)
      FROM individual_scores
      WHERE simulation_name = ?
    """, (sim_name,))
    mental, physical, temporal, performance, effort, frustration = cur.fetchone()

    conn.close()

    # domain‐level totals
    taskload = (mental or 0) + (physical or 0) + (temporal or 0) + (performance or 0) + (effort or 0) + (frustration or 0)
    medical_total    = (bls or 0) + (ps or 0) + (ss or 0) + (dc or 0)
    procedural_total = (cr  or 0) + (sp or 0)

    return {
      # raw category sums
      "Basic_Life_Support_team":           bls or 0.0,
      "Primary_Survey_team":               ps  or 0.0,
      "Secondary_Survey_team":             ss  or 0.0,
      "Definitive_Care_team":              dc  or 0.0,
      "Crew_Roles_Communication_team":     cr  or 0.0,
      "Systems_Procedural_Knowledge_team": sp  or 0.0,
      "medical_knowledge_team":    medical_total,
      "procedural_knowledge_team": procedural_total,
      "total_score": medical_total + procedural_total,
      "mental_team":       mental or 0,
      "physical_team":     physical or 0,
      "temporal_team":     temporal or 0,
      "performance_team":  performance or 0,
      "effort_team":       effort or 0,
      "frustration_team":  frustration or 0,
      "taskload":          taskload or 0
    }

def write_supervisor_scoring(sim_name: str, supervisor: str, comments: str,teamwork_scores: dict[str, int]):
    
    conn = sqlite3.connect(f"{sim_name}.db")
    cur  = conn.cursor()

    # drop any existing row for this sim+supervisor
    cur.execute(
        "DELETE FROM supervisor_scoring WHERE simulation_name = ? AND supervisor = ?",
        (sim_name, supervisor)
    )

    cur.execute("""
        INSERT INTO supervisor_scoring (
          simulation_name, supervisor,
          leadership_score, teamwork_score, task_score,
          overall_score, total_score,
          comments
        )
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        sim_name,
        supervisor,
        teamwork_scores.get("leadership", 0),
        teamwork_scores.get("teamwork", 0),
        teamwork_scores.get("task_management", 0),
        teamwork_scores.get("Overall", 0),
        teamwork_scores.get("Total", 0),
        comments
    ))
    conn.commit()
    conn.close()


def write_team_scoring(sim_name: str):
    tb = compute_team_aggregate(sim_name)
    conn = sqlite3.connect(f"{sim_name}.db")
    cur  = conn.cursor()
    cur.execute("DELETE FROM team_scoring WHERE simulation_name = ?", (sim_name,))
    cur.execute("""
        INSERT INTO team_scoring (
          simulation_name, criterion, total_score,
          Basic_Life_Support_team, Primary_Survey_team, Secondary_Survey_team,
          Definitive_Care_team, medical_knowledge_team,
          Crew_Roles_Communication_team, Systems_Procedural_Knowledge_team,
          procedural_knowledge_team,
          mental_team, physical_team, temporal_team, performance_team,
          effort_team, frustration_team, taskload
        ) VALUES (
          ?, 'AGGREGATE', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?
        )
    """, (
        sim_name,
        tb["total_score"],
        tb["Basic_Life_Support_team"],
        tb["Primary_Survey_team"],
        tb["Secondary_Survey_team"],
        tb["Definitive_Care_team"],
        tb["medical_knowledge_team"],
        tb["Crew_Roles_Communication_team"],
        tb["Systems_Procedural_Knowledge_team"],
        tb["procedural_knowledge_team"],
        tb["mental_team"],
        tb["physical_team"],
        tb["temporal_team"],
        tb["performance_team"],
        tb["effort_team"],
        tb["frustration_team"],
        tb["taskload"]
    ))
    conn.commit()
    conn.close()



def main():
    sim_name = teamwork.simulation_name
    init_db(sim_name)

    write_answers(sim_name)
    write_individual_scores(sim_name)
    write_team_scoring(sim_name)
    print(f"✅ All data written to {sim_name}.db")


if __name__ == "__main__":
    main()

