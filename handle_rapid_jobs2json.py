import sqlite3
import json
import os

DB_NAME = "job_postings2.db"

def create_database():
    """Creates the job_postings table in the database if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_postings (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            employment_type TEXT,
            date_posted TEXT,
            salary_range TEXT,
            description TEXT,
            image TEXT,
            job_provider TEXT,
            job_url TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def process_job_entry(job):
    """Extracts all job details, ensuring only the first job provider is stored."""
    job_provider = "Unknown"
    job_url = ""

    if "jobProviders" in job and isinstance(job["jobProviders"], list) and len(job["jobProviders"]) > 0:
        first_provider = job["jobProviders"][0]  # Get the first job provider
        job_provider = first_provider.get("jobProvider", "Unknown")
        job_url = first_provider.get("url", "")

    return (
        job.get("id", ""),
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("employmentType", ""),
        job.get("datePosted", ""),
        job.get("salaryRange", ""),
        job.get("description", ""),
        job.get("image", ""),
        job_provider,
        job_url
    )


def insert_jobs_from_rapid_jobs2(json_file):
    """Processes rapid_jobs2.json, handling JSON arrays in each line, and inserts data."""
    if not os.path.exists(json_file):
        print(f"File {json_file} not found.")
        return
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        with open(json_file, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                
                try:
                    job_list = json.loads(line)  # Parse each line as a JSON list
                    print(f"Line {line_number}: Parsed type -> {type(job_list)}")  # Debugging print

                    if isinstance(job_list, list):  # Ensure it's a list of job dictionaries
                        for job in job_list:
                            if isinstance(job, dict):
                                job_data = process_job_entry(job)
                                
                                cursor.execute('''
                                    INSERT OR IGNORE INTO job_postings 
                                    (id, title, company, location, employment_type, date_posted, salary_range, description, image, job_provider, job_url) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', job_data)
                            else:
                                print(f"Skipping non-dictionary entry in list at line {line_number}: {job}")
                    else:
                        print(f"Skipping non-list entry at line {line_number} in {json_file}: {job_list}")
                
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON at line {line_number} in {json_file}: {e}")
                    print(f"Problematic line {line_number}: {line[:200]}")  # Show first 200 chars

        conn.commit()
        print(f"Successfully inserted jobs from {json_file}")

    except Exception as e:
        print(f"Error processing {json_file}: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
    insert_jobs_from_rapid_jobs2("rapid_jobs2.json")
