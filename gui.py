import os
import sqlite3
import PySimpleGUI as Sg
from main import create_user_table, generate_resume, generate_cover_letter
import pdfkit
import markdown


# Update this path if necessary
WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'
pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)


def save_as_pdf(resume_content, output_path):
    """Convert resume content (Markdown format) to PDF and save it."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = os.path.join(output_path, 'resume.pdf')

    try:
        html_content = markdown.markdown(resume_content)
        pdfkit.from_string(html_content, output_file, configuration=pdfkit_config)
        return output_file
    except Exception as e:
        return f"An error occurred while saving the PDF: {str(e)}"


def fetch_jobs():
    """Fetch job listings from the database."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location, description FROM job_listings")
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def fetch_users():
    """Fetch saved usernames from the database."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM user_details")
    users = cursor.fetchall()
    conn.close()
    return users


def save_user_details(user_details):
    """Save user details into the database."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_details (name, email, phone, github_linkedin, projects, classes, other)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_details["name"],
        user_details["email"],
        user_details["phone"],
        user_details["github_linkedin"],
        ', '.join(user_details["projects"]),
        ', '.join(user_details["classes"]),
        user_details["other"]
    ))
    conn.commit()
    conn.close()


def load_job_details(job_id, window):
    """Load job details into the job description box."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM job_listings WHERE id=?", (job_id,))
    job = cursor.fetchone()
    conn.close()

    if job:
        window['-JOB_DETAILS-'].update(job[0])
    else:
        Sg.popup_error("Job details not found!", font=("Comic Sans MS", 12))


def tuple_to_dict(job_tuple):
    """Convert a job tuple to a dictionary."""
    keys = ["id", "title", "company", "location", "description"]
    return dict(zip(keys, job_tuple))


def load_user_details(user_id, window):
    """Load saved user details into the input fields."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, email, phone, github_linkedin, projects, classes, other "
        "FROM user_details WHERE id=?", (user_id,)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        window['-NAME-'].update(user[0])
        window['-EMAIL-'].update(user[1])
        window['-PHONE-'].update(user[2])
        window['-GITHUB_LINKEDIN-'].update(user[3])
        window['-PROJECTS-'].update(user[4])
        window['-CLASSES-'].update(user[5])
        window['-OTHER-'].update(user[6])
    else:
        Sg.popup_error("User not found!", font=("Comic Sans MS", 12))


def handle_save_information(values, window):
    """Handle saving user information."""
    user_details = {
        "name": values.get('-NAME-', ''),
        "email": values.get('-EMAIL-', ''),
        "phone": values.get('-PHONE-', ''),
        "github_linkedin": values.get('-GITHUB_LINKEDIN-', ''),
        "projects": values.get('-PROJECTS-', '').split(',') if values.get('-PROJECTS-', '') else [],
        "classes": values.get('-CLASSES-', '').split(',') if values.get('-CLASSES-', '') else [],
        "other": values.get('-OTHER-', ''),
    }

    if user_details["name"] and user_details["email"] and user_details["phone"]:
        save_user_details(user_details)
        Sg.popup("User information saved successfully!", font=("Comic Sans MS", 12))

        updated_users = fetch_users()
        user_dropdown_values = [f"{user[0]} - {user[1]}" for user in updated_users]
        window['-USER_SELECT-'].update(values=user_dropdown_values)
    else:
        Sg.popup_error("Please fill out at least Name, Email, and Phone!",
                       font=("Comic Sans MS", 12))


def handle_job_selection(values, window, job_listings):
    """Handle job selection from the table."""
    if values['-JOB_TABLE-']:
        selected_row_index = values['-JOB_TABLE-'][0]
        selected_job = job_listings[selected_row_index]
        load_job_details(selected_job[0], window)


def handle_user_selection(values, window):
    """Handle user selection from the dropdown."""
    if values['-USER_SELECT-']:
        selected_user_text = values['-USER_SELECT-']
        selected_user_id = selected_user_text.split(" - ")[0]
        load_user_details(selected_user_id, window)


def handle_generate_cover_letter(values, job_listings):
    """Handle generating a cover letter."""
    selected_job_index = values.get('-JOB_TABLE-', [])
    if not selected_job_index:
        Sg.popup_error("Please select a job before generating a cover letter.")
        return

    job_index = selected_job_index[0]
    job = job_listings[job_index]

    job_dict = tuple_to_dict(job)
    user_details = {
        "name": values.get('-NAME-', ''),
        "email": values.get('-EMAIL-', ''),
        "phone": values.get('-PHONE-', ''),
        "github_linkedin": values.get('-GITHUB_LINKEDIN-', ''),
        "projects": values.get('-PROJECTS-', '').split(',') if values.get('-PROJECTS-', '') else [],
        "classes": values.get('-CLASSES-', '').split(',') if values.get('-CLASSES-', '') else [],
        "other": values.get('-OTHER-', ''),
    }

    cover_letter_content = generate_cover_letter(job_dict, user_details)
    Sg.popup('Generated Cover Letter', cover_letter_content, font=("Comic Sans MS", 12))


def handle_save_as_pdf(values, job_listings):
    """Handle saving the resume as a PDF."""
    selected_job_index = values.get('-JOB_TABLE-', [])
    if not selected_job_index:
        Sg.popup_error("Please select a job before saving the resume as PDF.")
        return

    job_index = selected_job_index[0]
    job = job_listings[job_index]

    job_dict = tuple_to_dict(job)
    user_details = {
        "name": values.get('-NAME-', ''),
        "email": values.get('-EMAIL-', ''),
        "phone": values.get('-PHONE-', ''),
        "github_linkedin": values.get('-GITHUB_LINKEDIN-', ''),
        "projects": values.get('-PROJECTS-', '').split(',') if values.get('-PROJECTS-', '') else [],
        "classes": values.get('-CLASSES-', '').split(',') if values.get('-CLASSES-', '') else [],
        "other": values.get('-OTHER-', ''),
    }

    resume_content = generate_resume(job_dict, user_details)
    output_dir = os.path.expanduser("~/Downloads")  # or any other directory of your choice

    result = save_as_pdf(resume_content, output_dir)

    if result.startswith("An error"):
        Sg.popup_error(result, font=("Comic Sans MS", 12))
    else:
        Sg.popup(f"Resume saved as PDF successfully: {result}", font=("Comic Sans MS", 12))


def handle_generate_resume(values, job_listings):
    """Handle generating a resume."""
    selected_job_index = values.get('-JOB_TABLE-', [])
    if not selected_job_index:
        Sg.popup_error("Please select a job before generating a resume.")
        return

    job_index = selected_job_index[0]
    job = job_listings[job_index]

    job_dict = tuple_to_dict(job)
    user_details = {
        "name": values.get('-NAME-', ''),
        "email": values.get('-EMAIL-', ''),
        "phone": values.get('-PHONE-', ''),
        "github_linkedin": values.get('-GITHUB_LINKEDIN-', ''),
        "projects": values.get('-PROJECTS-', '').split(',') if values.get('-PROJECTS-', '') else [],
        "classes": values.get('-CLASSES-', '').split(',') if values.get('-CLASSES-', '') else [],
        "other": values.get('-OTHER-', ''),
    }

    resume_content = generate_resume(job_dict, user_details)
    Sg.popup('Generated Resume', resume_content, font=("Comic Sans MS", 12))


def create_gui_layout(job_listings):
    """Create the layout for the GUI."""
    table_data = [[job[0], job[1], job[2], job[3], job[4]] for job in job_listings]
    headings = ['ID', 'Title', 'Company', 'Location', 'Description']

    layout = [
        [Sg.Text('Select a Job from the List', font=("Comic Sans MS", 14, "bold"),
         text_color="#FFFF00", background_color="#1A1A1A")],
        [Sg.Table(
            values=table_data,
            headings=headings,
            auto_size_columns=True,
            display_row_numbers=False,
            justification='left',
            key='-JOB_TABLE-',
            row_height=35,
            num_rows=10,
            background_color="#333333",
            text_color="white",
            font=("Comic Sans MS", 12),
            selected_row_colors=("black", "#5A5AFF"),
            enable_events=True
        )],
        [Sg.Text('Job Details:', font=("Comic Sans MS", 12, "bold"),
                 text_color="white", background_color="#1A1A1A")],
        [Sg.Multiline('', size=(70, 15), key='-JOB_DETAILS-', disabled=True,
                      background_color="#333333", text_color="white", font=("Comic Sans MS", 12))],
        [Sg.Button('Generate Resume', size=(20, 1), font=("Comic Sans MS", 12, "bold")),
         Sg.Button('Generate Cover Letter', size=(20, 1), font=("Comic Sans MS", 12, "bold")),
         Sg.Button('Save as PDF', size=(20, 1), font=("Comic Sans MS", 12, "bold"))],

        [Sg.Text('Enter Your Information', font=("Comic Sans MS", 14, "bold"),
                 text_color="#FFFF00", background_color="#1A1A1A")],
        [Sg.Text('Name', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
         Sg.InputText(key='-NAME-', font=("Comic Sans MS", 12),
                      background_color="#333333", text_color="white")],
        [Sg.Text('Email', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
         Sg.InputText(key='-EMAIL-', font=("Comic Sans MS", 12),
                      background_color="#333333", text_color="white")],
        [Sg.Text('Phone Number', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
         Sg.InputText(key='-PHONE-', font=("Comic Sans MS", 12),
                      background_color="#333333", text_color="white")],
        [Sg.Text('GitHub/LinkedIn', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
         Sg.InputText(key='-GITHUB_LINKEDIN-', font=("Comic Sans MS", 12),
                      background_color="#333333", text_color="white")],
        [Sg.Text('Projects (separate with commas)', font=("Comic Sans MS", 12),
                 background_color="#1A1A1A"),
         Sg.InputText(key='-PROJECTS-', font=("Comic Sans MS", 12),
                      background_color="#333333", text_color="white")],
        [Sg.Text('Classes (separate with commas)', font=("Comic Sans MS", 12),
                 background_color="#1A1A1A"),
         Sg.InputText(key='-CLASSES-', font=("Comic Sans MS", 12),
                      background_color="#333333", text_color="white")],
        [Sg.Text('Other Information', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
         Sg.InputText(key='-OTHER-', font=("Comic Sans MS", 12),
                      background_color="#333333", text_color="white")],
        [Sg.Button('Save Information', size=(20, 1), font=("Comic Sans MS", 12, "bold"))],
        [Sg.Button('Exit', size=(20, 1), font=("Comic Sans MS", 12, "bold"),
                   button_color=("white", "red"))],
        [Sg.Text('Load Saved User', font=("Comic Sans MS", 12), background_color="#1A1A1A"),
         Sg.Combo(values=[], key='-USER_SELECT-', readonly=True, enable_events=True,
                  size=(30, 1), font=("Comic Sans MS", 12), background_color="#333333",
                  text_color="white")],
        [Sg.Button('Clear', size=(20, 1), font=("Comic Sans MS", 12, "bold"))],
    ]

    return layout


def main():
    """Main function to run the GUI."""
    Sg.theme_background_color("#1A1A1A")
    Sg.theme_text_color("white")
    Sg.theme_element_background_color("#333333")
    Sg.theme_element_text_color("white")
    Sg.theme_button_color(("white", "#5A5AFF"))

    job_listings = fetch_jobs()
    layout = create_gui_layout(job_listings)
    window = Sg.Window('Job Listings and Resume Builder', layout,
                       background_color="#1A1A1A", finalize=True)

    saved_users = fetch_users()
    user_dropdown_values = [f"{user[0]} - {user[1]}" for user in saved_users]
    window['-USER_SELECT-'].update(values=user_dropdown_values)

    while True:
        event, values = window.read()

        if event in (Sg.WINDOW_CLOSED, 'Exit'):
            if Sg.popup_yes_no("Are you sure you want to exit?",
                               font=("Comic Sans MS", 12)) == "Yes":
                break

        if event == 'Save Information':
            handle_save_information(values, window)

        if event == '-JOB_TABLE-':
            handle_job_selection(values, window, job_listings)

        if event == '-USER_SELECT-':
            handle_user_selection(values, window)

        if event == 'Clear':
            window['-NAME-'].update('')
            window['-EMAIL-'].update('')
            window['-PHONE-'].update('')
            window['-GITHUB_LINKEDIN-'].update('')
            window['-PROJECTS-'].update('')
            window['-CLASSES-'].update('')
            window['-OTHER-'].update('')

        if event == 'Generate Cover Letter':
            handle_generate_cover_letter(values, job_listings)

        if event == 'Save as PDF':
            handle_save_as_pdf(values, job_listings)

        if event == 'Generate Resume':
            handle_generate_resume(values, job_listings)

    window.close()


if __name__ == "__main__":
    create_user_table()
    main()
