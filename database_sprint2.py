import sqlite3
import json
import os
import time


# Function to create the job postings database table
def create_database(db_name="job_postings.db"):
    conn = sqlite3.connect(db_name)
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
            job_providers TEXT -- Store all job providers as a comma-separated string
        )
    """
    )

    conn.commit()
    conn.close()


# Process a single job entry
def process_single_job(job):
    job_providers = job.get("jobProviders", [])  # Extract jobProviders list
    providers_str = ", ".join(
        f"{p.get('jobProvider', 'Unknown')}: {p.get('url', 'No URL')}"
        for p in job_providers
    )

    return {
        "id": job.get("id"),
        "site": job.get("site", ""),
        "job_url": job.get("job_url", ""),
        "job_url_direct": job.get("job_url_direct", ""),
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "job_type": job.get("employmentType", ""),
        "date_posted": job.get("datePosted", ""),
        "salary_source": job.get("salary_source", ""),
        "interval": job.get("interval", ""),
        "min_amount": job.get("min_amount"),
        "max_amount": job.get("max_amount"),
        "currency": job.get("currency", ""),
        "is_remote": job.get("is_remote", False),
        "job_level": job.get("job_level", ""),
        "job_function": job.get("job_function", ""),
        "company_industry": job.get("company_industry", ""),
        "listing_type": job.get("listing_type", ""),
        "emails": ", ".join(
            job.get("emails", [])
        ),  # Store emails as a comma-separated string
        "description": job.get("description", ""),
        "company_url": job.get("company_url", ""),
        "company_url_direct": job.get("company_url_direct", ""),
        "company_addresses": ", ".join(job.get("company_addresses", [])),
        "company_num_employees": job.get("company_num_employees"),
        "company_revenue": job.get("company_revenue", ""),
        "company_description": job.get("company_description", ""),
        "logo_photo_url": job.get("logo_photo_url", ""),
        "ceo_name": job.get("ceo_name", ""),
        "ceo_photo_url": job.get("ceo_photo_url", ""),
        "job_providers": providers_str,  # Insert job providers string
    }


# Analysis of rapid_jobs2.json
# The file Newline Delimited JSON format, each line is a standalone JSON object.
# Instead of loading the entire file as a JSON array, need to process it line by line to decode each JSON entry separately.


# Process JSON file
import json


def process_json_file(json_file):
    job_entries = []

    try:
        with open(json_file, "r", encoding="utf-8") as file:
            first_char = file.read(1).strip()  # Read first character to check format
            file.seek(0)  # Reset file pointer

            if first_char == "[":
                # JSON Array format (like rapidResults.json)
                try:
                    data = json.load(file)  # Load entire JSON file
                    if isinstance(data, list):
                        job_entries = [process_single_job(job) for job in data]
                    else:
                        print(f"Skipping unknown JSON structure in {json_file}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON array in {json_file}: {e}")

            else:
                # NDJSON format (like rapid_jobs2.json) - Read line by line
                print(f"Processing {json_file} as NDJSON...")

                for line_number, line in enumerate(file, start=1):
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    try:
                        job = json.loads(line)  # Parse each line separately
                        if isinstance(job, dict):  # Ensure it's a valid job entry
                            job_entries.append(process_single_job(job))
                        else:
                            print(
                                f"Skipping non-dictionary entry at line {line_number} in {json_file}"
                            )

                    except json.JSONDecodeError as e:
                        print(
                            f"Skipping invalid JSON at line {line_number} in {json_file}: {e}"
                        )

    except Exception as e:
        print(f"Error reading {json_file}: {e}")

    return job_entries


def insert_jobs(json_file, db_name="job_postings.db"):
    retries = 5
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            job_entries = process_json_file(json_file)

            if not job_entries:
                print(f"No job entries found in {json_file}")

            for job_data in job_entries:
                if not job_data.get("id"):
                    print(f"Skipping job with missing ID: {job_data}")
                    continue

                print("Inserting job:", job_data)

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO job_postings (
                        id, site, job_url, job_url_direct, title, company, location, job_type, date_posted, 
                        salary_source, interval, min_amount, max_amount, currency, is_remote, job_level, 
                        job_function, company_industry, listing_type, emails, description, company_url, 
                        company_url_direct, company_addresses, company_num_employees, company_revenue, 
                        company_description, logo_photo_url, ceo_name, ceo_photo_url, job_providers
                    ) VALUES (
                        :id, :site, :job_url, :job_url_direct, :title, :company, :location, :job_type, :date_posted, 
                        :salary_source, :interval, :min_amount, :max_amount, :currency, :is_remote, :job_level, 
                        :job_function, :company_industry, :listing_type, :emails, :description, :company_url, 
                        :company_url_direct, :company_addresses, :company_num_employees, :company_revenue, 
                        :company_description, :logo_photo_url, :ceo_name, :ceo_photo_url, :job_providers
                    )
                """,
                    job_data,
                )

            conn.commit()
            conn.close()
            print(f"Data inserted successfully from {json_file}")
            return
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < retries - 1:
                time.sleep(1)
            else:
                print(f"Failed to insert data from {json_file}: {e}")


# Get JSON file paths dynamically
def get_json_files():
    return [file for file in os.listdir() if file.endswith(".json")]


# Main Execution
if __name__ == "__main__":
    create_database()

    json_files = get_json_files()  # Dynamically get JSON files
    if not json_files:
        print("No JSON files found in the directory.")
    else:
        for file in json_files:
            insert_jobs(file)

    print("All job postings have been inserted successfully.")
