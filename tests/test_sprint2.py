import os
import sqlite3
import unittest
import json
from setup_database import create_database
from job_handler import process_json_file, insert_jobs

DB_FILE = "test_job_postings.db"
JSON_FILE = "test_jobs.json"

test_data = [
    {"id": "111", "title": "Software Engineer", "company": "TechCorp", "location": "Remote"},
    {"id": "222", "title": "Data Scientist", "company": "AI Inc", "location": "San Francisco"},
    {"id": "333", "title": "DevOps Engineer", "company": "CloudOps", "location": "New York"},
]


class TestSprint2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test database and clean environment before running tests."""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

        create_database(DB_FILE)

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            for job in test_data:
                file.write(json.dumps(job) + "\n")

    @classmethod
    def tearDownClass(cls):
        """Clean up test database and JSON file after tests."""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        if os.path.exists(JSON_FILE):
            os.remove(JSON_FILE)

    def test_create_DB(self):
        """Ensure that the database and `job_postings` table are created successfully."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='job_postings';")
        result = cursor.fetchone()

        self.assertIsNotNone(result, "Table `job_postings` should exist in the database.")
        conn.close()

    def test_process_json_file(self):
        """Ensure JSON file processing returns the correct number of job entries."""
        jobs = process_json_file(JSON_FILE)

        self.assertEqual(len(jobs), len(test_data), "Number of jobs should match test data.")
        self.assertEqual(jobs[0]["title"], "Software Engineer")
        self.assertEqual(jobs[1]["title"], "Data Scientist")
        self.assertEqual(jobs[2]["location"], "New York")

    def test_database_insertion(self):
        """Ensure jobs from the JSON file are inserted correctly into the database."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        insert_jobs(JSON_FILE, db_name=DB_FILE)

        cursor.execute("SELECT COUNT(*) FROM job_postings")
        count = cursor.fetchone()[0]

        self.assertEqual(count, len(test_data), "All test jobs should be inserted into the database.")

        cursor.execute("SELECT title, company, location FROM job_postings WHERE id='111'")
        job = cursor.fetchone()

        self.assertIsNotNone(job, "Job should exist in the database.")
        self.assertEqual(job[0], "Software Engineer")
        self.assertEqual(job[1], "TechCorp")
        self.assertEqual(job[2], "Remote")

        conn.close()

    def test_get_full_job_data(self):
        """Ensure that a specific job can be retrieved from the database."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT title, company, location FROM job_postings WHERE id='222'")
        job = cursor.fetchone()

        self.assertIsNotNone(job, "Job should exist in the database.")
        self.assertEqual(job[0], "Data Scientist")
        self.assertEqual(job[1], "AI Inc")
        self.assertEqual(job[2], "San Francisco")

        conn.close()


if __name__ == "__main__":
    unittest.main()
