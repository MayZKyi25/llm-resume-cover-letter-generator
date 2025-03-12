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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            github TEXT,
            linkedin TEXT,
            projects TEXT,
            classes TEXT,
            other_info TEXT
        )
    ''')
    db_connection.commit()

@pytest.mark.parametrize("test_user_data, expected_output", [
    (  # Valid user data
        {
            "name": "Liam",
            "email": "Liam23@gmail.com",
            "phone": "8888888888",
            "github": "VanessaHyden",
            "linkedin": "linkedin.com/in/vhyden",
            "projects": "Project A, Project B",
            "classes": "CS101, CS102",
            "other_info": "Interested in AI"
        },
        "Success! Saved users' info can be found in jobs.db's user_info table"
    ),
    (  # Missing email
        {
            "name": "Sophia",
            "email": "",
            "phone": "7777777777",
            "github": "SophiaGH",
            "linkedin": "linkedin.com/in/sophia",
            "projects": "Project X",
            "classes": "CS103",
            "other_info": "Machine Learning Enthusiast"
        },
        "Name and Email are required."  
    ),
    (  # Invalid phone number (Test assumes no strict validation)
        {
            "name": "Ethan",
            "email": "ethan@example.com",
            "phone": "abc123456",
            "github": "EthanDev",
            "linkedin": "linkedin.com/in/ethan",
            "projects": "Project Y",
            "classes": "CS104",
            "other_info": "Cybersecurity expert"
        },
        "Success! Saved users' info can be found in jobs.db's user_info table"
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
