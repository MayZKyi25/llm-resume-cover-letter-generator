import sqlite3

DB_NAME = "job_postings.db"

def create_user_info_table():
    """Creates the user_info table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
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
        conn.commit()

def save_user_info(data):
    """Saves user information to the database."""
    if not data["name"] or not data["email"]:
        return "Name and Email are required."

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_info (name, email, phone, github, linkedin, projects, classes, other_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data["name"], data["email"], data["phone"], data["github"], 
              data["linkedin"], data["projects"], data["classes"], data["other_info"]))
        conn.commit()

    return "Success"

if __name__ == "__main__":
    create_user_info_table()
    print("User database initialized.")
