import os
import sqlite3
import json
import unittest
import PySimpleGUI as sg
from main import load_json_data

"""This module handles job data loading, insertion into a SQLite database,
and testing the database operations."""


def insert_job_data(job_listings, db_file="test_jobs.db"):
    """Insert job listings into the database."""
    conn = sqlite3.connect(db_file)
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
    conn.close()


def create_database():
    """Create the job_listings table in the database if it does not exist."""
    db_file = "test_jobs.db"
    conn = sqlite3.connect(db_file)
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
    conn.close()


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

    conn = sqlite3.connect(db_file)
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
    conn.close()

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
    test_file = "test_jobs.json"

    with open(test_file, "w", encoding="ascii") as file:
        for job in test_data:
            file.write(json.dumps(job) + "\n")

    loaded_data = load_json_data(test_file)

    assert len(loaded_data) == len(test_data), "Loaded data count mismatch."
    assert loaded_data[0]["title"] == "Software Engineer", "Title mismatch."
    assert loaded_data[1]["company"] == "Data Inc", "Company mismatch."

    os.remove(test_file)


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


class TestApp(unittest.TestCase):

    def test_fetch_job_details(self):
        """Test fetching full job details based on job ID."""
        self.cursor.execute(
            """
            INSERT INTO job_listings (title, company, location, description)
            VALUES ('Software Engineer', 'Tech Corp', 'Remote', 'Full job description here')
            """
        )
        self.conn.commit()

        job_id = self.cursor.lastrowid  # Get last inserted job's ID
        job_details = fetch_job_details(self.conn, job_id)

        self.assertIsNotNone(job_details)
        self.assertEqual(job_details[1], 'Software Engineer')  # Check title
        self.assertEqual(job_details[2], 'Tech Corp')  # Check company
        self.assertEqual(job_details[3], 'Remote')  # Check location
        self.assertEqual(job_details[4], 'Full job description here')  # Check description

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
    """Placeholder for the GUI function."""
    return None


def main():
    """Main function to run the GUI."""
    conn = sqlite3.connect("savedJobs.db")
    window = create_gui()

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, "Exit"):
            if sg.popup_yes_no(
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
                sg.popup("User information saved successfully!", font=("Comic Sans MS", 12))


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


if __name__ == "__main__":
    main()
    unittest.main()

#