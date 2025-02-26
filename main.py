from s3_user_db import create_user_info_table
from s3_ui_components import create_ui

if __name__ == "__main__":
    create_user_info_table()  # Ensure user table exists
    app = create_ui()  # Start UI
    app.mainloop()
