import os
import sqlite3
import json
from main import load_json_data, create_database, insert_job_data


# Module docstring
"""This module handles job data loading, insertion into a SQLite database, 
and testing the database operations."""

# Insert job data into the database
def insert_job_data(job_listings, db_file="test_jobs.db"):
    """Insert job listings into the database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    for job in job_listings:
        cursor.execute("""
            INSERT INTO job_listings (title, company, location)
            VALUES (?, ?, ?)
        """, (job["title"], job["company"], job["location"]))

    conn.commit()
    conn.close()


# Create the database
def create_database():
    """Create the job_listings table in the database if it does not exist."""
    db_file = "test_jobs.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT
        )
    """)

    conn.commit()
    conn.close()


# Test database operations
def test_database_operations():
    """Test creating the database and inserting job data."""
    db_file = "test_jobs.db"

    if os.path.exists(db_file):
        os.remove(db_file)

    # Create the database
    create_database()

    # Dummy job data
    test_job = {
        "title": "Backend Developer",
        "company": "StartupX",
        "location": "San Francisco"
    }

    # Insert job data into the database
    insert_job_data([test_job])

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='job_listings'"
    )
    table_exists = cursor.fetchone()
    assert table_exists, "Table 'job_listings' does not exist!"

    # Retrieve all rows from the table
    cursor.execute("SELECT * FROM job_listings")
    all_rows = cursor.fetchall()
    print("Contents of job_listings table:", all_rows)

    # Retrieve specific job data
    cursor.execute("SELECT title, company, location FROM job_listings")
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Assertions
    assert result is not None, "No job was inserted!"
    assert result[0] == "Backend Developer"
    assert result[1] == "StartupX"

    # Cleanup
    os.remove(db_file)


# Test loading JSON data
def test_load_json_data():
    """Test loading job data from a JSON file."""
    test_data = [
        {"title": "Software Engineer", "company": "Tech Corp", "location": "Remote"},
        {"title": "Data Scientist", "company": "Data Inc", "location": "New York"}
    ]
    test_file = "test_jobs.json"

    # Write test data to a file
    with open(test_file, "w", encoding="ascii") as file:
        for job in test_data:
            file.write(json.dumps(job) + "\n")

    # Load data from the JSON file
    loaded_data = load_json_data(test_file)

    # Assertions
    assert len(loaded_data) == len(test_data), "Loaded data count does not match expected count."
    assert loaded_data[0]["title"] == "Software Engineer", "First job title does not match."
    assert loaded_data[1]["company"] == "Data Inc", "Second job company does not match."

    # Cleanup
    os.remove(test_file)
