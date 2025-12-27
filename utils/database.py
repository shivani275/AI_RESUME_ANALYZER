# utils/database.py

import sqlite3
import json
from pathlib import Path
from typing import List, Tuple, Optional

DB_PATH = Path("resume_analyzer.db")


def init_db() -> None:
    """Initialize SQLite database with the results table."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_name TEXT,
                    job_description TEXT,
                    score INTEGER,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to initialize database: {e}")


def save_result(
    candidate_name: str = "Candidate",
    resume_text: str = "",
    job_description: str = "",
    score: int = 0,
    matched_skills: Optional[List[str]] = None,
    missing_skills: Optional[List[str]] = None
) -> None:
    """Save ATS analysis result to the database."""
    matched_skills = matched_skills or []
    missing_skills = missing_skills or []

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO results (candidate_name, job_description, score, matched_skills, missing_skills)
                VALUES (?, ?, ?, ?, ?)
            """, (
                candidate_name,
                job_description,
                score,
                json.dumps(matched_skills),
                json.dumps(missing_skills)
            ))
            conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to save result: {e}")


def fetch_results(limit: int = 10) -> List[Tuple]:
    """Fetch past analysis results from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT * FROM results ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to fetch results: {e}")
        return []
