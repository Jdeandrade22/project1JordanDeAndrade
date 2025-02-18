"""This script processes job listings, generates resumes, and stores data in an SQLite database."""

import json
import sys
import sqlite3
import PySimpleGUI as sg
import google.generativeai as genai
from api import api_key  # Ensure 'api.py' exists


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
    """Generates resume with user info while prompting AI."""
    job = reformat_job_data(job)
    job_description = job.get("description", "No description available")
    job_title = job.get("title", "Unknown Job Title")
    company_name = job.get("company", "Unknown Company")

    personal_description = (
        f"My name is {user_details['name']}, and I am a student at {user_details['university']}. "
        f"I have experience in {user_details['experience']}.\n"
        f"I have worked on various projects, including:\n"
        f"{chr(10).join(user_details['projects'])}"
        if user_details["projects"]
        else "- No projects listed"
    )

    prompt = f"""Given the following job title: {job_title} at {company_name}\n"
        f"Job description:\n{job_description}\n"
        f"And the following personal description: {personal_description}\n"
        f"Please generate a resume in markdown format tailored to this job."""

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
import PySimpleGUI as sg

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

    #########################################################################

    import PySimpleGUI as sg
    import sqlite3

    def create_user_data_table():
        """Creates the user_data table if it doesn't exist."""
        conn = sqlite3.connect('savedJobs.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                github_linkedin TEXT,
                projects TEXT,
                classes TEXT,
                other TEXT
            )
        """)
        conn.commit()
        conn.close()

    def fetch_jobs():
        """Fetches job listings from the database."""
        conn = sqlite3.connect('savedJobs.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id, title, company, location FROM job_listings")
            jobs = cursor.fetchall()
        except sqlite3.OperationalError as e:
            sg.popup_error(f"Database error: {e}", font=("Comic Sans MS", 12))
            jobs = []

        conn.close()
        return jobs

    def save_user_data(user_info):
        """Saves the user's data into the database."""
        conn = sqlite3.connect('savedJobs.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO user_data (name, email, phone, github_linkedin, projects, classes, other)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_info['name'], user_info['email'], user_info['phone'],
              user_info['github_linkedin'], user_info['projects'], user_info['classes'], user_info['other']))
        conn.commit()
        conn.close()

    create_user_data_table()

    job_listings = fetch_jobs()

    def main():
        sg.theme_background_color("#1A1A1A")
        sg.theme_text_color("white")
        sg.theme_element_background_color("#333333")
        sg.theme_element_text_color("white")
        sg.theme_button_color(("white", "#5A5AFF"))

        layout = [
            [sg.Text('Select a Job from the List', font=("Comic Sans MS", 14, "bold"), text_color="#FFFF00",
                     background_color="#1A1A1A")],
            [sg.Listbox(values=[f"{job[1]} - {job[2]} ({job[3]})" for job in job_listings],
                        size=(50, 10), key='-JOB_LIST-', enable_events=True,
                        background_color="#333333", text_color="white", font=("Comic Sans MS", 12))],
            [sg.Text('Job Details:', font=("Comic Sans MS", 12, "bold"), text_color="white",
                     background_color="#1A1A1A")],
            [sg.Multiline('', size=(50, 5), key='-JOB_DETAILS-', disabled=True,
                          background_color="#333333", text_color="white", font=("Comic Sans MS", 12))],

            [sg.Text('Enter Your Information', font=("Comic Sans MS", 14, "bold"), text_color="#FFFF00",
                     background_color="#1A1A1A")],
            [sg.Text('Name', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
             sg.InputText(key='-NAME-', font=("Comic Sans MS", 12), background_color="#333333", text_color="white")],
            [sg.Text('Email', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
             sg.InputText(key='-EMAIL-', font=("Comic Sans MS", 12), background_color="#333333", text_color="white")],
            [sg.Text('Phone Number', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
             sg.InputText(key='-PHONE-', font=("Comic Sans MS", 12), background_color="#333333", text_color="white")],
            [sg.Text('GitHub/LinkedIn', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
             sg.InputText(key='-GITHUB_LINKEDIN-', font=("Comic Sans MS", 12), background_color="#333333",
                          text_color="white")],
            [sg.Text('Projects (separate with commas)', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
             sg.InputText(key='-PROJECTS-', font=("Comic Sans MS", 12), background_color="#333333",
                          text_color="white")],
            [sg.Text('Classes (separate with commas)', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
             sg.InputText(key='-CLASSES-', font=("Comic Sans MS", 12), background_color="#333333", text_color="white")],
            [sg.Text('Other Information', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
             sg.InputText(key='-OTHER-', font=("Comic Sans MS", 12), background_color="#333333", text_color="white")],

            [sg.Button('Save Information', size=(20, 1), font=("Comic Sans MS", 12, "bold"))],
            [sg.Button('Exit', size=(20, 1), font=("Comic Sans MS", 12, "bold"), button_color=("white", "red"))]
        ]

        window = sg.Window('Job Listings and Resume Builder', layout, background_color="#1A1A1A")

        while True:
            event, values = window.read()

            if event in (sg.WINDOW_CLOSED, 'Exit'):
                break

            if event == '-JOB_LIST-':
                if values['-JOB_LIST-']:
                    selected_job_text = values['-JOB_LIST-'][0]
                    selected_job_id = next(
                        (job[0] for job in job_listings if f"{job[1]} - {job[2]} ({job[3]})" == selected_job_text),
                        None
                    )

                    if selected_job_id is None:
                        sg.popup_error("Job not found in database!", font=("Comic Sans MS", 12))
                        continue

                    conn = sqlite3.connect('savedJobs.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM job_listings WHERE id=?", (selected_job_id,))
                    job_details = cursor.fetchone()
                    conn.close()

                    if job_details:
                        job_details_text = f"Title: {job_details[1]}\nCompany: {job_details[2]}\nLocation: {job_details[3]}\n" \
                                           f"Description: {job_details[4]}\nSalary: {job_details[5]} - {job_details[6]}"
                        window['-JOB_DETAILS-'].update(job_details_text)
                    else:
                        sg.popup_error("Job details not found!", font=("Comic Sans MS", 12))

            if event == 'Save Information':
                user_info = {
                    'name': values['-NAME-'],
                    'email': values['-EMAIL-'],
                    'phone': values['-PHONE-'],
                    'github_linkedin': values['-GITHUB_LINKEDIN-'],
                    'projects': values['-PROJECTS-'],
                    'classes': values['-CLASSES-'],
                    'other': values['-OTHER-'],
                }

                save_user_data(user_info)
                sg.popup('Your information has been saved!', font=("Comic Sans MS", 12))

        window.close()

    if __name__ == "__main__":
        main()


# Some functions and comments added by Google AI

if __name__ == "__main__":
    main()
