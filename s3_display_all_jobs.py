import sqlite3
import os

# Function to display job listings from a given database
def display_job_list(db_name="job_postings.db"):
    if not os.path.exists(db_name):
        print(f"Error: Database file '{db_name}' not found.")
        return []

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Query job titles and companies from the database
        cursor.execute('SELECT id, title, company, location FROM job_postings')
        jobs = cursor.fetchall()

        if not jobs:
            print(f"No jobs available in {db_name}.")
            conn.close()
            return []

        # Display job titles and companies
        print(f"\nJob Listings from {db_name}:")
        for i, job in enumerate(jobs, start=1):
            print(f"{i}. {job[1]} at {job[2]} - {job[3]}")

        conn.close()
        return jobs
    except sqlite3.Error as e:
        print(f"Error while querying {db_name}: {e}")
        return []

# Function to display detailed information about a selected job from a given database
def display_job_details(job_id, db_name="job_postings.db"):
    if not os.path.exists(db_name):
        print(f"Error: Database file '{db_name}' not found.")
        return

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Query detailed information for the selected job
        cursor.execute('''
            SELECT title, company, location, employment_type, date_posted, salary_range, description, image, job_provider, job_url 
            FROM job_postings WHERE id = ?
        ''', (job_id,))
        job_details = cursor.fetchone()

        if not job_details:
            print("Job details not found.")
            conn.close()
            return

        # Display detailed information
        print("\nJob Details:")
        print(f"Title: {job_details[0]}")
        print(f"Company: {job_details[1]}")
        print(f"Location: {job_details[2]}")
        print(f"Employment Type: {job_details[3]}")
        print(f"Date Posted: {job_details[4]}")
        print(f"Salary Range: {job_details[5]}")
        print(f"Description: {job_details[6]}")
        print(f"Image: {job_details[7]}")
        print(f"Job Provider: {job_details[8]}")
        print(f"Job URL: {job_details[9]}")

        conn.close()
    except sqlite3.Error as e:
        print(f"Error while fetching details from {db_name}: {e}")

# Function to display job listings from both databases
# Function to display job listings from both databases
def display_jobs_from_both_databases():
    jobs_db1 = display_job_list("job_postings.db")  # First database
    jobs_db2 = display_job_list("job_postings2.db")  # Second database

    if not jobs_db1 and not jobs_db2:
        print("No jobs available in either database.")
        return

    # Determine the offset based on the length of jobs in db1
    offset = len(jobs_db1)  # This will be the next available job ID starting point

    # Adjust job IDs for jobs from db2, only if job[0] can be cast to an integer
    adjusted_jobs_db2 = []
    for job in jobs_db2:
        try:
            # Try converting job[0] (job_id) to an integer and adjust
            job_id = int(job[0])
            adjusted_jobs_db2.append((job_id + offset, job[1], job[2], job[3]))
        except ValueError:
            # If conversion fails, leave job_id unchanged (or handle differently)
            adjusted_jobs_db2.append(job)

    # Combine jobs from both databases
    combined_jobs = jobs_db1 + adjusted_jobs_db2

    # Display the combined job listings
    print(f"\nCombined Job Listings:")
    for i, job in enumerate(combined_jobs, start=1):
        print(f"{i}. {job[1]} at {job[2]} - {job[3]}")

    # Let user choose a job from the combined list
    try:
        job_index = int(input("\nEnter the job number to view more details: ")) - 1
        if 0 <= job_index < len(combined_jobs):
            selected_job = combined_jobs[job_index]
            if selected_job in jobs_db1:
                display_job_details(selected_job[0], "job_postings.db")
            else:
                display_job_details(selected_job[0], "job_postings2.db")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a valid job number.")


# Main execution to display job listings and let the user select
if __name__ == "__main__":
    display_jobs_from_both_databases()
