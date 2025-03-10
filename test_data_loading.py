import os
import sqlite3
import json
import unittest
import tempfile
import PySimpleGUI as Sg
from main import load_json_data

# Check if the environment is headless
def is_headless():
    """Check if the environment is headless (no display available)."""
    return os.getenv("DISPLAY") is None or os.getenv("PYTHONUNBUFFERED") is not None


def insert_job_data(job_listings, db_file="test_jobs.db"):
    """Insert job listings into the database."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        for job in job_listings:
            cursor.execute(
                """
                INSERT INTO job_listings (title, company, location)
                VALUES (?, ?, ?)
                """,
                (job["title"], job["company"], job["location"]),
            )
        conn.commit()


def create_database():
    """Create the job_listings table in the database if it does not exist."""
    db_file = "test_jobs.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                location TEXT
            )
            """
        )
        conn.commit()


def test_database_operations():
    """Test creating the database and inserting job data."""
    db_file = "test_jobs.db"

    if os.path.exists(db_file):
        os.remove(db_file)

    create_database()

    test_job = {
        "title": "Backend Developer",
        "company": "StartupX",
        "location": "San Francisco",
    }

    insert_job_data([test_job])

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='job_listings'"
        )
        table_exists = cursor.fetchone()
        assert table_exists, "Table 'job_listings' does not exist!"

        cursor.execute("SELECT * FROM job_listings")
        all_rows = cursor.fetchall()
        print("Contents of job_listings table:", all_rows)

        cursor.execute("SELECT title, company, location FROM job_listings")
        result = cursor.fetchone()

    assert result is not None, "No job was inserted!"
    assert result[0] == "Backend Developer"
    assert result[1] == "StartupX"

    os.remove(db_file)


def test_load_json_data():
    """Test loading job data from a JSON file."""
    test_data = [
        {"title": "Software Engineer", "company": "Tech Corp", "location": "Remote"},
        {"title": "Data Scientist", "company": "Data Inc", "location": "New York"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
        for job in test_data:
            temp_file.write(json.dumps(job) + "\n")
        temp_file_path = temp_file.name

    loaded_data = load_json_data(temp_file_path)

    assert len(loaded_data) == len(test_data), "Loaded data count mismatch."
    assert loaded_data[0]["title"] == "Software Engineer", "Title mismatch."
    assert loaded_data[1]["company"] == "Data Inc", "Company mismatch."

    os.remove(temp_file_path)


def fetch_jobs(conn):
    """Fetch job listings from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location FROM job_listings")
    return cursor.fetchall()


def fetch_job_details(conn, job_id):
    """Fetch full job details from the database using the job ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_listings WHERE id = ?", (job_id,))
    return cursor.fetchone()


def fetch_users(conn):
    """Fetch user details from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM user_details")
    return cursor.fetchall()


def save_user_details(conn, user_details):
    """Save user details into the database."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_details (name, email, phone, github_linkedin, projects, classes, other)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_details["name"],
            user_details["email"],
            user_details["phone"],
            user_details["github_linkedin"],
            ", ".join(user_details["projects"]),
            ", ".join(user_details["classes"]),
            user_details["other"],
        ),
    )
    conn.commit()


def create_gui():
    """Create and return the PySimpleGUI window."""
    layout = [
        [Sg.Text("Name:"), Sg.Input(key="-NAME-")],
        [Sg.Text("Email:"), Sg.Input(key="-EMAIL-")],
        [Sg.Text("Phone:"), Sg.Input(key="-PHONE-")],
        [Sg.Text("GitHub/LinkedIn:"), Sg.Input(key="-GITHUB_LINKEDIN-")],
        [Sg.Text("Projects (comma-separated):"), Sg.Input(key="-PROJECTS-")],
        [Sg.Text("Classes (comma-separated):"), Sg.Input(key="-CLASSES-")],
        [Sg.Text("Other:"), Sg.Input(key="-OTHER-")],
        [Sg.Button("Save Information"), Sg.Button("Exit")],
    ]
    return Sg.Window("User Details", layout)


def main():
    """Main function to run the GUI or tests."""
    if is_headless():
        print("Running in headless mode. Skipping GUI.")
        unittest.main()
    else:
        print("Running in GUI mode.")
        conn = sqlite3.connect("savedJobs.db")
        window = create_gui()

        while True:
            event, values = window.read()

            if event in (Sg.WINDOW_CLOSED, "Exit"):
                if Sg.popup_yes_no(
                    "Are you sure you want to exit?", font=("Comic Sans MS", 12)
                ) == "Yes":
                    break

            if event == "Save Information":
                user_details = {
                    "name": values.get("-NAME-", ""),
                    "email": values.get("-EMAIL-", ""),
                    "phone": values.get("-PHONE-", ""),
                    "github_linkedin": values.get("-GITHUB_LINKEDIN-", ""),
                    "projects": values.get("-PROJECTS-", "").split(",")
                    if values.get("-PROJECTS-", "")
                    else [],
                    "classes": values.get("-CLASSES-", "").split(",")
                    if values.get("-CLASSES-", "")
                    else [],
                    "other": values.get("-OTHER-", ""),
                }

                if user_details["name"] and user_details["email"] and user_details["phone"]:
                    save_user_details(conn, user_details)
                    Sg.popup("User information saved successfully!", font=("Comic Sans MS", 12))


class TestApp(unittest.TestCase):
    """Unit tests for the application."""

    def setUp(self):
        """Create a test database for the test cases."""
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE user_details (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT,
                github_linkedin TEXT,
                projects TEXT,
                classes TEXT,
                other TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE job_listings (
                id INTEGER PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                description TEXT
            )
            """
        )
        self.conn.commit()

    def tearDown(self):
        """Close the database connection after tests."""
        self.conn.close()

    def test_save_user_details(self):
        """Test saving user details to the database."""
        user_details = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "github_linkedin": "https://github.com/johndoe",
            "projects": ["Project1", "Project2"],
            "classes": ["Class1", "Class2"],
            "other": "Additional Info",
        }
        save_user_details(self.conn, user_details)
        self.cursor.execute(
            "SELECT * FROM user_details WHERE name=?", (user_details["name"],)
        )
        saved_user = self.cursor.fetchone()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user[1], user_details["name"])

    def test_fetch_users(self):
        """Test fetching users from the database."""
        user_details = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "0987654321",
            "github_linkedin": "https://github.com/janedoe",
            "projects": ["ProjectA"],
            "classes": ["ClassA"],
            "other": "Info",
        }
        save_user_details(self.conn, user_details)
        users = fetch_users(self.conn)
        self.assertGreater(len(users), 0)

    def test_fetch_jobs(self):
        """Test fetching jobs from the database."""
        self.cursor.execute(
            """
            INSERT INTO job_listings (title, company, location, description)
            VALUES ('Software Engineer', 'Tech Company', 'Remote', 'Job description here')
            """
        )
        self.conn.commit()
        jobs = fetch_jobs(self.conn)
        self.assertGreater(len(jobs), 0)

    def test_fetch_job_details(self):
        """Test fetching full job details from the database."""
        self.cursor.execute(
            """
            INSERT INTO job_listings (title, company, location, description)
            VALUES ('Frontend Developer', 'Web Corp', 'New York', 'Job details here')
            """
        )
        self.conn.commit()
        self.cursor.execute("SELECT id FROM job_listings WHERE title='Frontend Developer'")
        job_id = self.cursor.fetchone()[0]
        job_details = fetch_job_details(self.conn, job_id)
        self.assertIsNotNone(job_details)

    def test_create_prompt_with_job_and_user_info(self):
        """Test creating a prompt with job and user information."""
        job = {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "location": "Remote",
            "description": "Develop and maintain software applications."
        }

        user = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "github_linkedin": "https://github.com/johndoe",
            "projects": ["Project1", "Project2"],
            "classes": ["CS101", "CS102"],
            "other": "Additional info"
        }

        expected_prompt = (
            "Job Title: Software Engineer\n"
            "Company: Tech Corp\n"
            "Location: Remote\n"
            "Description: Develop and maintain software applications.\n\n"
            "User Name: John Doe\n"
            "Email: john.doe@example.com\n"
            "Phone: 1234567890\n"
        )

        generated_prompt = create_prompt_with_job_and_user_info(job, user)
        self.assertEqual(generated_prompt, expected_prompt)


def create_prompt_with_job_and_user_info(job, user):
    """Create a prompt combining job and user information."""
    prompt = (
        f"Job Title: {job['title']}\n"
        f"Company: {job['company']}\n"
        f"Location: {job['location']}\n"
        f"Description: {job['description']}\n\n"
        f"User Name: {user['name']}\n"
        f"Email: {user['email']}\n"
        f"Phone: {user['phone']}\n"
    )
    return prompt

#some functions provided through Google Ai

if __name__ == "__main__":
    main()