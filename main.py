"""This script processes job listings, generates resumes, and stores data in an SQLite database."""

import json
import sys
import google.generativeai as genai
from api_secrets import api_key


# Configure the API
genai.configure(api_key=api_key)

# Helps configure JSON files to proper format
sys.stdout.reconfigure(encoding="utf-8")


# Mapping inconsistent fields
inconsistent_fields = {
    "employment_type": "job_type",
    "url": "job_url",
    "salary_range": "salary_source",
}

# Params the script filters through the JSON with
fields = [
    "site",
    "job_url",
    "job_url_direct",
    "title",
    "company",
    "location",
    "job_type",
    "date_posted",
    "salary_source",
    "interval",
    "min_amount",
    "max_amount",
    "currency",
    "is_remote",
    "job_level",
    "job_function",
    "company_industry",
    "listing_type",
    "emails",
    "description",
    "company_addresses",
    "company_num_employees",
    "company_revenue",
    "company_description",
]


def load_json_data(file_path):
    """Loads JSON as ASCII for proper identification and structure."""
    job_listings = []
    try:
        with open(file_path, "r", encoding="ascii") as file:
            for line in file:
                try:
                    job_entry = json.loads(line.strip())
                    if isinstance(job_entry, list):
                        job_listings.extend(job_entry)
                    else:
                        job_listings.append(job_entry)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line in {file_path}: {e}")
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Skipping.")
    return job_listings


def reformat_job_data(job):
    """Reformat JSON structure if needed."""
    reformatted_job = {col: None for col in fields}
    for key, value in job.items():
        mapped_key = inconsistent_fields.get(key, key)
        if mapped_key in reformatted_job:
            reformatted_job[mapped_key] = str(value) if value is not None else None
    return reformatted_job


def select_job(job_listings):
    """Selects a job from the list."""
    print("\nAvailable Job Listings:")
    for index, job in enumerate(job_listings, start=1):
        if isinstance(job, dict):
            print(
                f"{index}. {job.get('title', 'Unknown Job')} at "
                f"{job.get('company', 'Unknown Company')}"
            )
        else:
            print(f"{index}. Invalid job format")

    while True:
        try:
            choice = (
                int(input("\nEnter the number of the job you'd like to apply for: "))
                - 1
            )
            if 0 <= choice < len(job_listings):
                return job_listings[choice]
            print("Invalid choice, please enter a valid job number.")
        except ValueError:
            print("Invalid input, please enter a number.")


def gather_user_details():
    """Gathers user information for the resume."""
    print("\nLet's customize your resume. Please answer the following questions:")
    name = input("Full Name: ").strip()
    university = input("University (or education background): ").strip()
    experience = input(
        "Briefly describe your experience "
        "(e.g., programming languages, software development, etc.): "
    ).strip()

    projects = []
    print("\nEnter your key projects (press Enter when done):")
    while True:
        project = input("Project: ").strip()
        if project == "":
            break
        projects.append(f"- {project}")

    return {
        "name": name,
        "university": university,
        "experience": experience,
        "projects": projects,
    }

def generate_resume(job, user_details):
    """Generates a tailored resume based on the job posting and user details."""

    job = reformat_job_data(job)
    job_description = job.get("description", "No description available")
    job_title = job.get("title", "Unknown Job Title")
    company_name = job.get("company", "Unknown Company")

    # Build personal details section dynamically
    personal_details = (
        f"My name is {user_details.get('name', 'N/A')}, and I am a student at {user_details.get('university', 'an unspecified university')}.\n"
        f"I have experience in {user_details.get('experience', 'relevant fields')}.\n"
        f"I have worked on projects including:\n"
        f"{chr(10).join(user_details.get('projects', ['No projects listed']))}\n"
        f"I have taken courses such as:\n"
        f"{chr(10).join(user_details.get('classes', ['No classes listed']))}\n"
        f"My GitHub or LinkedIn profile can be found here: {user_details.get('github_linkedin', 'N/A')}.\n"
        f"Additional information:\n{user_details.get('other', 'No additional information provided.')}"
    )

    # Improved AI prompt
    prompt = f"""You are an expert resume writer. Generate a resume in **Markdown format** that highlights my skills, experience, and projects while aligning with the given job.

**Job Details:**
- **Job Title:** {job_title}
- **Company:** {company_name}
- **Description:** {job_description}

**Personal Information:**
{personal_details}

### Instructions:
- Format the resume professionally using Markdown.
- Tailor the resume to match the job description.
- Highlight relevant skills, coursework, and projects.
- Keep it concise but impactful.

Please generate the resume now."""

    # Call AI model to generate response
    gen_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gen_model.generate_content(prompt)

    return response.text


def create_database():
    """Creates the database."""
    conn = sqlite3.connect("savedJobs.db")
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS job_listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT, job_url TEXT, job_url_direct TEXT, title TEXT, company TEXT,
        location TEXT, job_type TEXT, date_posted TEXT, salary_source TEXT,
        interval TEXT, min_amount REAL, max_amount REAL, currency TEXT,
        is_remote TEXT, job_level TEXT, job_function TEXT, company_industry TEXT,
        listing_type TEXT, emails TEXT, description TEXT, company_addresses TEXT,
        company_num_employees TEXT, company_revenue TEXT, company_description TEXT
    )"""
    )

    conn.commit()
    conn.close()
def create_user_table():
    """Creates a table for storing user details if it does not exist."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            github_linkedin TEXT,
            projects TEXT,
            classes TEXT,
            other TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_job_data(jobs):
    """Inserts job data into the database."""
    conn = sqlite3.connect("savedJobs.db")
    cursor = conn.cursor()

    for job in jobs:
        columns = tuple(job.keys())
        values = tuple(job.values())

        placeholders = ", ".join(["?"] * len(values))
        sql_query = (
            f"INSERT INTO job_listings ({', '.join(columns)}) VALUES ({placeholders})"
        )

        cursor.execute(sql_query, values)

    conn.commit()
    conn.close()


import sqlite3


def main():
    """Main function."""
    data_files = ["rapidResults (1).json", "rapid_jobs2.json"]
    job_listings = []
    for file_path in data_files:
        job_listings.extend(load_json_data(file_path))

    if not job_listings:
        print("No job listings found. Please check the files.")
        return

    reformatted_jobs = [reformat_job_data(job) for job in job_listings]
    create_database()
    insert_job_data(reformatted_jobs)

# Some functions and comments added by Google AI

if __name__ == "__main__":
    main()