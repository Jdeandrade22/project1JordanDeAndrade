import sqlite3
import PySimpleGUI as sg
from main import generate_resume

def fetch_jobs():
    """Fetches job listings from the database."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location, description FROM job_listings")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def load_job_details(job_id, window):
    """Loads job details into the job description box."""
    conn = sqlite3.connect('savedJobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM job_listings WHERE id=?", (job_id,))
    job = cursor.fetchone()
    conn.close()

    if job:
        window['-JOB_DETAILS-'].update(job[0])
    else:
        sg.popup_error("Job details not found!", font=("Comic Sans MS", 12))

def tuple_to_dict(job_tuple):
    """Converts a job tuple to a dictionary."""
    keys = ["id", "title", "company", "location", "description"]
    return dict(zip(keys, job_tuple))

def main():
    sg.theme_background_color("#1A1A1A")
    sg.theme_text_color("white")
    sg.theme_element_background_color("#333333")
    sg.theme_element_text_color("white")
    sg.theme_button_color(("white", "#5A5AFF"))

    job_listings = fetch_jobs()

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
        [sg.Button('Generate Resume', size=(20, 1), font=("Comic Sans MS", 12, "bold"))],
        [sg.Button('Exit', size=(20, 1), font=("Comic Sans MS", 12, "bold"), button_color=("white", "red"))]
    ]

    window = sg.Window('Job Listings and Resume Builder', layout, background_color="#1A1A1A")

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            if sg.popup_yes_no("Are you sure you want to exit?", font=("Comic Sans MS", 12)) == "Yes":
                break  # Break the loop and close the window

        if event == 'Generate Resume':
            selected_job_index = values['-JOB_LIST-']
            user_details = {
                "name": values.get('-NAME-', ''),
                "email": values.get('-EMAIL-', ''),
                "phone": values.get('-PHONE-', ''),
                "github_linkedin": values.get('-GITHUB_LINKEDIN-', ''),  # Use .get() to avoid KeyError
                "projects": values.get('-PROJECTS-', '').split(',') if values.get('-PROJECTS-', '') else [],
                "classes": values.get('-CLASSES-', '').split(',') if values.get('-CLASSES-', '') else [],
                "other": values.get('-OTHER-', ''),
            }

            if selected_job_index:
                selected_job_text = selected_job_index[0]
                selected_job = next(
                    (job for job in job_listings if f"{job[1]} - {job[2]} ({job[3]})" == selected_job_text), None)

                if selected_job:
                    # Convert the tuple to a dictionary
                    job_dict = tuple_to_dict(selected_job)
                    # Call generate_resume with job_dict and user_details
                    resume = generate_resume(job_dict, user_details)
                    print(f"Resume output: {resume}")

                else:
                    sg.popup_error("Selected job not found!", font=("Comic Sans MS", 12))
            else:
                sg.popup_error("Please select a job to generate the resume!", font=("Comic Sans MS", 12))

        if event == '-JOB_LIST-' and values['-JOB_LIST-']:
            selected_job_text = values['-JOB_LIST-'][0]
            selected_job = next((job for job in job_listings if f"{job[1]} - {job[2]} ({job[3]})" == selected_job_text),
                                None)
            if selected_job:
                load_job_details(selected_job[0], window)

    window.close()  # Close the window only after breaking the loop

if __name__ == "__main__":
    main()


    add an element that allows the user to save this information - save it to the same database that you created in sprint2
