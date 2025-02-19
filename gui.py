import sqlite3
import PySimpleGUI as sg

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
        [sg.Button('Generate resume', size=(20, 1), font=("Comic Sans MS", 12, "bold"))],
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

                conn = sqlite3.connect('Project1ProfDemoPython2025/savedJobs.db')
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