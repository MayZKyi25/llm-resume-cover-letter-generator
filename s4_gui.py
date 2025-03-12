import sqlite3
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QListWidget, QTextEdit, QSplitter
)
from s4_generate_documents import generate_ai_documents
from setup_database import open_db

DB_NAME = "jobs.db"  # Ensure this matches your actual database name

class JobApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Job Application System")
        self.setGeometry(100, 100, 1200, 700)  # Bigger UI for better readability

        self.layout = QVBoxLayout()

        # **Job Selection Table**
        self.job_list_label = QLabel("Select a Job:")
        self.layout.addWidget(self.job_list_label)
        self.job_table = QTableWidget()
        self.job_table.setColumnCount(5)
        self.job_table.setHorizontalHeaderLabels(["Job ID", "Title", "Company", "Location", "Description"])
        self.job_table.cellClicked.connect(self.show_job_details)  # Update job details when clicked
        self.layout.addWidget(self.job_table)

        # **Job Details Panel**
        self.details_label = QLabel("Job Details:")
        self.layout.addWidget(self.details_label)
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.layout.addWidget(self.details_text)

        # **Profile Selection List**
        self.profile_list_label = QLabel("Select a Profile:")
        self.layout.addWidget(self.profile_list_label)
        self.profile_list = QListWidget()
        self.layout.addWidget(self.profile_list)

        # **Generate AI Documents Button**
        self.generate_button = QPushButton("Generate AI Documents")
        self.generate_button.clicked.connect(self.generate_documents)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

        self.load_jobs()
        self.load_profiles()

    def load_jobs(self):
        """Load job listings into a table for better readability."""
        conn, cursor = open_db()
        cursor.execute("SELECT job_id, job_title, company_name, location, job_description FROM jobs_listings")
        jobs = cursor.fetchall()
        conn.close()

        self.job_table.setRowCount(len(jobs))

        for row_index, job in enumerate(jobs):
            for col_index, value in enumerate(job):
                self.job_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        # **Auto-Adjust Column Widths**
        self.job_table.resizeColumnsToContents()
        self.job_table.setSortingEnabled(True)  # Enable sorting

    def show_job_details(self, row, column):
        """Display full job details when a job is clicked."""
        job_id = self.job_table.item(row, 0).text()
        title = self.job_table.item(row, 1).text()
        company = self.job_table.item(row, 2).text()
        location = self.job_table.item(row, 3).text()
        description = self.job_table.item(row, 4).text()

        job_details = f"**{title}**\nCompany: {company}\nLocation: {location}\n\nDescription:\n{description}"
        self.details_text.setText(job_details)

    def load_profiles(self):
        """Load user profiles from the database."""
        conn, cursor = open_db()
        cursor.execute("SELECT user_id, name FROM user_info")
        profiles = cursor.fetchall()
        conn.close()

        for profile in profiles:
            self.profile_list.addItem(f"{profile[0]} - {profile[1]}")

    def generate_documents(self):
        """Fetch selected job and profile, then generate AI documents."""
        selected_row = self.job_table.currentRow()
        selected_profile = self.profile_list.currentItem()

        if selected_row == -1 or not selected_profile:
            QMessageBox.warning(self, "Selection Error", "Please select a job and a user profile!")
            return

        job_id = self.job_table.item(selected_row, 0).text()  # Extract job_id
        user_id = selected_profile.text().split(" - ")[0]  # Extract user_id

        generate_ai_documents(job_id, user_id)  # Call LLM function

        QMessageBox.information(self, "Success", "Cover Letter and Resume generated successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JobApplication()
    window.show()
    sys.exit(app.exec())
