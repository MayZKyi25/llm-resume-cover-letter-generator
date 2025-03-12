import sqlite3
import json
import os
import time


# Function to create the job postings database table
def create_database():
    conn = sqlite3.connect("job_postings.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job_postings (
            id TEXT PRIMARY KEY,
            site TEXT,
            job_url TEXT,
            job_url_direct TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            job_type TEXT,
            date_posted TEXT,
            salary_source TEXT,
            interval TEXT,
            min_amount REAL,
            max_amount REAL,
            currency TEXT,
            is_remote BOOLEAN,
            job_level TEXT,
            job_function TEXT,
            company_industry TEXT,
            listing_type TEXT,
            emails TEXT,
            description TEXT,
            company_url TEXT,
            company_url_direct TEXT,
            company_addresses TEXT,
            company_num_employees INTEGER,
            company_revenue TEXT,
            company_description TEXT,
            logo_photo_url TEXT,
            ceo_name TEXT,
            ceo_photo_url TEXT,
            job_providers TEXT
        )
    """
    )

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

