import sqlite3
from typing import List, Optional
from models.incident import Incident
import uuid
from datetime import date

# This DB_FILE must be the same as the one in the HR system
DB_FILE = "company_data.db"

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the incidents table if it doesn't exist."""
    with get_db_connection() as conn:
        # Note: The employees table is managed by the HR system's database module.
        # This module only ensures the incidents table exists.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                employee_id TEXT NOT NULL,
                incident_date TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            );
        """)
        conn.commit()

def add_incident(incident: Incident) -> None:
    """Adds an incident to the database."""
    with get_db_connection() as conn:
        conn.execute(
            """INSERT INTO incidents (id, employee_id, incident_date, location, description, severity)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (str(incident.id), incident.employee_id, incident.incident_date.isoformat(), incident.location, incident.description, incident.severity),
        )
        conn.commit()

def list_incidents() -> List[Incident]:
    """Lists all incidents."""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM incidents ORDER BY incident_date DESC;")
        rows = cursor.fetchall()
        return [
            Incident(
                id=uuid.UUID(row["id"]),
                employee_id=row["employee_id"],
                incident_date=date.fromisoformat(row["incident_date"]),
                location=row["location"],
                description=row["description"],
                severity=row["severity"],
            )
            for row in rows
        ]

# Initialize the database when this module is first imported
init_db()
