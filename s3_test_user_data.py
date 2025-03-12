import pytest
import sqlite3
from s3_gui import save_user_info

DB_NAME = "jobs.db"  

@pytest.fixture(scope="module")
def db_connection():
    """Fixture to establish and teardown a test database connection."""
    conn = sqlite3.connect(DB_NAME)
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def create_user_table(db_connection):
    """Ensure the `user_info` table exists before running tests."""
    cursor = db_connection.cursor()
    
    # Ensure the address column exists in case the table was created earlier
    cursor.execute("PRAGMA table_info(user_info);")
    columns = [col[1] for col in cursor.fetchall()]
    if "address" not in columns:
        cursor.execute("ALTER TABLE user_info ADD COLUMN address TEXT;")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            address TEXT,  
            github TEXT,
            linkedin TEXT,
            projects TEXT,
            classes TEXT,
            other_info TEXT
        )
    ''')
    db_connection.commit()

@pytest.mark.parametrize("test_user_data, expected_output", [
    (  # ✅ Valid user data (Address Included)
        {
            "name": "Liam",
            "email": "Liam23@gmail.com",
            "phone": "8888888888",
            "address": "123 Tech Street, Seattle, WA",
            "github": "VanessaHyden",
            "linkedin": "linkedin.com/in/vhyden",
            "projects": "Project A, Project B",
            "classes": "CS101, CS102",
            "other_info": "Interested in AI"
        },
        "Success! User information saved to jobs.db (user_info table)"
    ),
    (  # ❌ Missing email (Should fail)
        {
            "name": "Sophia",
            "email": "",
            "phone": "7777777777",
            "address": "456 AI Drive, San Francisco, CA",
            "github": "SophiaGH",
            "linkedin": "linkedin.com/in/sophia",
            "projects": "Project X",
            "classes": "CS103",
            "other_info": "Machine Learning Enthusiast"
        },
        "Name and Email are required."  
    ),
    (  # ✅ Invalid phone format (No strict validation assumed)
        {
            "name": "Ethan",
            "email": "ethan@example.com",
            "phone": "abc123456",
            "address": "789 Cyber Street, Austin, TX",
            "github": "EthanDev",
            "linkedin": "linkedin.com/in/ethan",
            "projects": "Project Y",
            "classes": "CS104",
            "other_info": "Cybersecurity expert"
        },
        "Success! User information saved to jobs.db (user_info table)"
    )
])
def test_save_user_info(create_user_table, test_user_data, expected_output):
    """Test saving user information with different inputs."""
    save_result = save_user_info(test_user_data)
    assert save_result == expected_output

def insert_test_job():
    """Ensure a test job exists before running tests."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO jobs_listings (job_id, job_title, company_name, location, job_description)
            VALUES (1, 'Software Engineer', 'TechCorp', 'Remote', 'Develop software applications.')
        ''')
        conn.commit()

insert_test_job()
print("Test job inserted if not already present.")
