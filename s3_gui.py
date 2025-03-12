import sqlite3
from setup_database import open_db
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox, QSizePolicy
)


class JobApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Job Application System")
        self.resize(1200, 800)  # Set a larger initial window size

        # Main layout
        self.layout = QVBoxLayout()

        # Horizontal layout for job listings and details
        job_layout = QHBoxLayout()

        # Job List - Expands Horizontally
        self.job_list = QListWidget()
        self.job_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Job Details - Expands Horizontally
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add job list and job details to horizontal layout
        job_layout.addWidget(self.job_list, 2)  # Give 3:2 width ratio
        job_layout.addWidget(self.details_text, 4)

        # User Input Section
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")

        self.github_input = QLineEdit()
        self.github_input.setPlaceholderText("Enter your GitHub Profile")

        self.linkedin_input = QLineEdit()
        self.linkedin_input.setPlaceholderText("Enter your LinkedIn Profile")

        self.projects_input = QTextEdit()
        self.projects_input.setPlaceholderText("Describe your projects")
        self.projects_input.setFixedHeight(50)  # Reduce height

        self.classes_input = QTextEdit()
        self.classes_input.setPlaceholderText("List relevant classes")
        self.classes_input.setFixedHeight(50)  # Reduce height

        self.other_input = QTextEdit()
        self.other_input.setPlaceholderText("Any other important information")
        self.other_input.setFixedHeight(50)  # Reduce height

        self.save_button = QPushButton("Save Information")
        self.save_button.clicked.connect(self.handle_save_user_info)

        # Add widgets to main layout
        self.layout.addWidget(QLabel("Job Listings:"))
        self.layout.addLayout(job_layout)  # Add job listings and details in one row
        self.layout.addWidget(QLabel("Enter Your Information:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.phone_input)
        self.layout.addWidget(self.github_input)
        self.layout.addWidget(self.linkedin_input)
        self.layout.addWidget(QLabel("Projects:"))
        self.layout.addWidget(self.projects_input)
        self.layout.addWidget(QLabel("Classes:"))
        self.layout.addWidget(self.classes_input)
        self.layout.addWidget(QLabel("Other Information:"))
        self.layout.addWidget(self.other_input)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.load_jobs()
        self.job_list.itemClicked.connect(self.display_job_details)

    def load_jobs(self):
        """Loads job listings from the database into the job list widget."""
        conn, cursor = open_db()
        cursor.execute("SELECT job_id, job_title, company_name, location FROM jobs_listings")
        jobs = cursor.fetchall()
        conn.close()

        for job in jobs:
            self.job_list.addItem(f"{job[1]} at {job[2]} ({job[3]})")

    def display_job_details(self):
        """Displays full details of the selected job."""
        selected_item = self.job_list.currentRow()
        if selected_item == -1:
            return

        conn, cursor = open_db()
        cursor.execute("SELECT * FROM jobs_listings")
        jobs = cursor.fetchall()
        conn.close()

        if 0 <= selected_item < len(jobs):
            job = jobs[selected_item]
            details = f"Title: {job[3]}\nCompany: {job[8]}\nLocation: {job[7]}\n\nDescription:\n{job[4]}"
            self.details_text.setPlainText(details)

    def handle_save_user_info(self):
        """Handles user input and calls `save_user_info` to save data."""
        user_data = {
            "name": self.name_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "github": self.github_input.text(),
            "linkedin": self.linkedin_input.text(),
            "projects": self.projects_input.toPlainText(),
            "classes": self.classes_input.toPlainText(),
            "other_info": self.other_input.toPlainText(),
        }

        result = save_user_info(user_data)
        QMessageBox.information(self, "Success", result)


def save_user_info(user_data):
    """Saves user information into the database."""
    if not user_data["name"] or not user_data["email"]:
        return "Name and Email are required."

    conn, cursor = open_db()
    
    cursor.execute("""
        INSERT INTO user_info (name, email, phone, github, linkedin, projects, classes, other)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_data["name"],
        user_data["email"],
        user_data["phone"],
        user_data["github"],
        user_data["linkedin"],
        user_data["projects"],
        user_data["classes"],
        user_data["other_info"]
    ))

    conn.commit()
    conn.close()

    return "Success! Saved users' info can be found in jobs.db's user_info table"


if __name__ == "__main__":
    app = QApplication([])
    window = JobApplication()
    window.show()
    app.exec()
