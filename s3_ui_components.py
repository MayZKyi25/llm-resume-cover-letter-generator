import tkinter as tk
from tkinter import messagebox
from s3_user_db import save_user_info
from s3_job_fetcher import fetch_jobs, get_job_details

def create_ui():
    root = tk.Tk()
    root.title("Job Finder App")

    # Job Selection Listbox
    job_listbox = tk.Listbox(root, width=50, height=20)
    job_listbox.pack()

    jobs = fetch_jobs()
    for job in jobs:
        job_listbox.insert(tk.END, f"{job[1]} - {job[2]}")  # Display title and company

    # Job Details Frame (To display details inside UI)
    job_details_frame = tk.Frame(root)
    job_details_frame.pack(pady=10)

    label_job_details = tk.Label(job_details_frame, text="Select a job to see details.", justify=tk.LEFT, anchor="w", wraplength=500)
    label_job_details.pack()

    def show_job_details(event):
        selected_job_index = job_listbox.curselection()
        if not selected_job_index:
            return
        job_id = jobs[selected_job_index[0]][0]
        job_details = get_job_details(job_id)

        if not job_details:
            label_job_details.config(text="Error: Job details not found.")
            return

        description = job_details[19] if job_details[19] else "None"

        details_text = f"""
        Job Title: {job_details[4]}
        Company: {job_details[5]}
        Location: {job_details[6]}
        Description: {description}
        """
        label_job_details.config(text=details_text)

    job_listbox.bind('<<ListboxSelect>>', show_job_details)

    # User Information Form
    frame_user_info = tk.Frame(root)
    frame_user_info.pack(pady=20)

    labels = ["Name", "Email", "Phone", "GitHub", "LinkedIn", "Projects", "Classes", "Other Info"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame_user_info, text=label).grid(row=i, column=0)
        entry = tk.Entry(frame_user_info)
        entry.grid(row=i, column=1)
        entries[label.lower().replace(" ", "_")] = entry

    def save_info():
        user_data = {key: entry.get() for key, entry in entries.items()}
        result = save_user_info(user_data)
        messagebox.showinfo("Result", result)

    tk.Button(root, text="Save Info", command=save_info).pack(pady=10)

    return root

if __name__ == "__main__":
    app = create_ui()
    app.mainloop()
