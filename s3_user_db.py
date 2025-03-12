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

    return "Success! Saved users' info can be found in job_postings.db's user_info table"


def get_user_info(email):
    """Fetch user information by email."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, email, phone, github, linkedin, projects, classes, other_info
            FROM user_info WHERE email = ?
        ''', (email,))
        user = cursor.fetchone()

    if user:
        return {
            "name": user[0],
            "email": user[1],
            "phone": user[2],
            "github": user[3],
            "linkedin": user[4],
            "projects": user[5],
            "classes": user[6],
            "other_info": user[7],
        }
    return None  # Return None if the user is not found


if __name__ == "__main__":
    create_user_info_table()
    print("User database initialized.")
