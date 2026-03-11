import sqlite3
import os

# Use a consistent absolute path for the database inside the project's data/ folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # task_manager/
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "tasks.db")


def get_connection():
    # ensure data directory exists before connecting
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # ensure data directory exists and database file location is consistent
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = get_connection()

    conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        priority TEXT DEFAULT 'medium',
        created_date TEXT,
        due_date TEXT
    )""")

    conn.commit()
    conn.close()
