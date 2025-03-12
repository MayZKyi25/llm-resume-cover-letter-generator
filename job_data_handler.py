import json
import sqlite3
import re  # Fix for splitting JSON arrays correctly

def add_rapid_api_job_search2_to_db(file_name: str, cursor: sqlite3.Cursor):
    """Parses `rapid_jobs2.json` (concatenated JSON arrays) and inserts jobs into the database."""
    insert_statement = """INSERT OR IGNORE INTO jobs_listings
            (job_id, created_at, updated_at, job_title, job_description, seniority, full_time,
            location, company_name, salary, country, url, applicants_count)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""

    with open(file_name, "r", encoding="utf-8") as data_file:
        raw_content = data_file.read().strip()  # Read entire content

        # Fix for splitting concatenated JSON arrays correctly
        json_chunks = re.split(r"]\s*\[", raw_content)  # Splitting on `][` safely

        for i, chunk in enumerate(json_chunks):
            try:
                # Ensure each chunk is a valid JSON array
                if not chunk.startswith("["):
                    chunk = "[" + chunk
                if not chunk.endswith("]"):
                    chunk = chunk + "]"

                jobs = json.loads(chunk)  # Load JSON array
                for job in jobs:
                    job_tuple = (
                        job.get("id", "N/A"),
                        job.get("datePosted", "N/A"),
                        job.get("datePosted", "N/A"),
                        job.get("title", "N/A"),
                        job.get("description", "N/A"),
                        "NOT PROVIDED",
                        job.get("employmentType", "N/A"),
                        job.get("location", "N/A"),
                        job.get("company", "N/A"),
                        job.get("salaryRange", "N/A"),
                        "NOT PROVIDED",
                        job["jobProviders"][0]["url"] if job.get("jobProviders") else "Not Available",
                        "NOT AVAILABLE",
                    )
                    cursor.execute(insert_statement, job_tuple)
            except json.JSONDecodeError as e:
                print(f" Skipping invalid JSON chunk {i} in {file_name}: {e}")

def add_rapid_results_to_db(file_name: str, cursor: sqlite3.Cursor):
    """Parses `rapidResults.json` (JSONL format) and inserts jobs into the database."""
    insert_statement = """INSERT OR IGNORE INTO jobs_listings
                (job_id, created_at, updated_at, job_title, job_description, seniority, full_time,
                location, company_name, salary, country, url, applicants_count)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""

    with open(file_name, "r", encoding="utf-8") as data_file:
        for line_number, job_line in enumerate(data_file, start=1):
            try:
                data = json.loads(job_line.strip())  # Read line by line

                # Fix: Ensure `min_amount` and `max_amount` are handled properly
                min_amount = data.get('min_amount', "N/A")
                max_amount = data.get('max_amount', "N/A")
                salary = f"{min_amount} - {max_amount}" if min_amount != "N/A" and max_amount != "N/A" else "N/A"

                job_tuple = (
                    data.get("id", "N/A"),
                    data.get("datePosted", "N/A"),
                    data.get("datePosted", "N/A"),
                    data.get("title", "N/A"),
                    data.get("description", "N/A"),
                    data.get("job_level", "N/A"),
                    data.get("job_type", "N/A"),
                    data.get("location", "N/A"),
                    data.get("company", "N/A"),
                    salary,  # Fixed salary formatting
                    "US",
                    data.get("job_url_direct", "N/A"),
                    "NOT PROVIDED",
                )
                cursor.execute(insert_statement, job_tuple)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON on line {line_number} in {file_name}: {e}")

def get_jobs_from_db(cursor: sqlite3.Cursor):
    """Retrieves all jobs from the database."""
    select_statement = """SELECT job_id, created_at, updated_at, job_title, job_description, seniority, full_time,
                location, company_name, salary, country, url, applicants_count FROM jobs_listings"""
    cursor.execute(select_statement)
    results = cursor.fetchall()

    jobs_listings = [
        {
            "job_id": result[0], "created_at": result[1], "updated_at": result[2],
            "job_title": result[3], "job_description": result[4], "seniority": result[5],
            "full_time": result[6], "location": result[7], "company_name": result[8],
            "salary": result[9], "country": result[10], "url": result[11], "applicants_count": result[12]
        }
        for result in results
    ]
    return jobs_listings
