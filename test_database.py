import pytest
import sqlite3
import json
import os
from setup_database import create_database
from job_data_handler import add_rapid_results_to_db

DB_FILE = "test_jobs.db"
JSON_FILE = "test_jobs.json"

test_data = [
    {"id": "111", "title": "Software Engineer", "company": "TechCorp", "location": "Remote"},
    {"id": "222", "title": "Data Scientist", "company": "AI Inc", "location": "San Francisco"},
    {"id": "333", "title": "DevOps Engineer", "company": "CloudOps", "location": "New York"},
]

@pytest.fixture(scope="module")
def setup_and_teardown():
    """Set up test database and clean environment before running tests."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    create_database(DB_FILE)

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        for job in test_data:
            file.write(json.dumps(job) + "\n")

    yield

    """Clean up test database and JSON file after tests."""
    try:
        os.remove(DB_FILE)
        os.remove(JSON_FILE)
    except FileNotFoundError:
        pass


def test_create_DB(setup_and_teardown):
    """Ensure that the database and `jobs_listings` table are created successfully."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs_listings';")
    result = cursor.fetchone()

    assert result is not None, "Table `jobs_listings` should exist in the database."
    conn.close()


def test_database_insertion(setup_and_teardown):
    """Ensure jobs from the JSON file are inserted correctly into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    add_rapid_results_to_db(JSON_FILE, cursor)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM jobs_listings")
    count = cursor.fetchone()[0]

    assert count == len(test_data), "All test jobs should be inserted into the database."

    cursor.execute("SELECT job_title, company_name, location FROM jobs_listings WHERE job_id='111'")
    job = cursor.fetchone()

    assert job is not None, "Job should exist in the database."
    assert job[0] == "Software Engineer"  # job_title
    assert job[1] == "TechCorp"  # company_name
    assert job[2] == "Remote"  # location

    conn.close()
