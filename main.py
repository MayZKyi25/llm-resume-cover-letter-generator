from setup_database import create_database, open_db, close_db
from job_data_handler import add_rapid_api_job_search2_to_db, add_rapid_results_to_db

def main():
    """Main function to process both JSON files."""
    create_database()
    conn, cursor = open_db()

    print("Processing rapid_jobs2.json...")
    add_rapid_api_job_search2_to_db("rapid_jobs2.json", cursor)  # ✅ JSON array

    print("Processing rapidResults.json...")
    add_rapid_results_to_db("rapidResults.json", cursor)  # ✅ JSONL format

    conn.commit()
    close_db(conn)
    print("✅ Job data insertion complete.")

if __name__ == "__main__":
    main()
