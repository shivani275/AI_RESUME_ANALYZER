import sqlite3
import json

DB_NAME = "results.db"

def init_db():
    """Initialize the SQLite database and create or update the results table."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        """)

        # Helper function to add column if missing
        def add_column_if_missing(column_name, column_type="TEXT"):
            c.execute(f"PRAGMA table_info(results)")
            columns = [info[1] for info in c.fetchall()]
            if column_name not in columns:
                c.execute(f"ALTER TABLE results ADD COLUMN {column_name} {column_type}")

        # Ensure all required columns exist
        add_column_if_missing("resume_text", "TEXT")
        add_column_if_missing("job_description", "TEXT")
        add_column_if_missing("score", "REAL")
        add_column_if_missing("matched_skills", "TEXT")
        add_column_if_missing("missing_skills", "TEXT")

        conn.commit()


def save_result(resume_text, job_description, score, matched_skills=None, missing_skills=None):
    """Save a resume analysis result to the database."""
    matched_json = json.dumps(matched_skills or [])
    missing_json = json.dumps(missing_skills or [])
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO results (resume_text, job_description, score, matched_skills, missing_skills)
            VALUES (?, ?, ?, ?, ?)
        """, (resume_text, job_description, score, matched_json, missing_json))
        conn.commit()


def fetch_results(limit=10):
    """Fetch last `limit` results from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM results ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
    return rows
