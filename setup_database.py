import sqlite3

def create_database(db_name="jobs.db"):  # Accept an optional database name
    """Creates the SQLite database and jobs_listings table if it doesn't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs_listings (
            job_id TEXT PRIMARY KEY,
            created_at TEXT,
            updated_at TEXT,
            job_title TEXT,
            job_description TEXT,
            seniority TEXT,
            full_time TEXT,
            location TEXT,
            company_name TEXT,
            salary TEXT,
            country TEXT,
            url TEXT,
            applicants_count TEXT
        )
    """)


    # Create user_info table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_info (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            address TEXT,  -- Added the missing column
            github TEXT,
            linkedin TEXT,
            projects TEXT,
            classes TEXT,
            other TEXT
        )
    """)

    # Check if address column exists, add it if missing
    cursor.execute("PRAGMA table_info(user_info);")
    columns = [row[1] for row in cursor.fetchall()]
    if "address" not in columns:
        cursor.execute("ALTER TABLE user_info ADD COLUMN address TEXT;")
        print("Address column added to user_info table.")

    conn.commit()
    conn.close()

def open_db():
    """Opens a connection to the SQLite database."""
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn):
    """Closes the database connection."""
    conn.commit()
    conn.close()
