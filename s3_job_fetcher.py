import sqlite3

DB_NAME = "job_postings.db"

def fetch_jobs():
    """Fetch job listings from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, company FROM job_postings")
        return cursor.fetchall()

def get_job_details(job_id):
    """Fetch full job details for a given job ID."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_postings WHERE id=?", (job_id,))
        return cursor.fetchone()

if __name__ == "__main__":
    print(fetch_jobs())
