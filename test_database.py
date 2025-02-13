import sqlite3
import json
import os
import pytest
from database_sprint2 import create_database, insert_jobs, process_json_file

TEST_DB = "test_job_postings.db"

@pytest.fixture
def setup_database():
    """Creates a fresh test database before each test and deletes it after."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    create_database(TEST_DB)

    yield sqlite3.connect(TEST_DB)
    os.remove(TEST_DB)

def test_process_json_file():
    test_json = "test_jobs.json"

    sample_jobs = [
        {"id": "test1", "title": "Job 1", "company": "Company A"},
        {"id": "test2", "title": "Job 2", "company": "Company B"},
        {"id": "test3", "title": "Job 3", "company": "Company C"}
    ]

    with open(test_json, "w") as file:
        for job in sample_jobs:
            file.write(json.dumps(job) + "\n")

    jobs = process_json_file(test_json)

    os.remove(test_json)

    assert len(jobs) == 3
    assert jobs[0]["id"] == "test1"
    assert jobs[0]["title"] == "Job 1"
    assert jobs[0]["company"] == "Company A"
    assert jobs[-1]["id"] == "test3"
    assert jobs[-1]["title"] == "Job 3"
    assert jobs[-1]["company"] == "Company C"

def test_database_insertion(setup_database):
    test_json = "test_jobs.json"

    sample_jobs = [
        {
            "id": "test1",
            "title": "Test Job",
            "company": "TestCorp",
            "location": "NY",
            "employmentType": "Full-time",
            "datePosted": "2025-01-01",
            "salaryRange": "$50,000",
            "currency": "USD",
            "jobProviders": [{"jobProvider": "Indeed", "url": "https://example.com/test1"}]
        }
    ]

    with open(test_json, "w") as file:
        for job in sample_jobs:
            file.write(json.dumps(job) + "\n")

    insert_jobs(test_json, TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_postings WHERE id = 'test1'")
    result = cursor.fetchone()

    os.remove(test_json)
    assert result is not None