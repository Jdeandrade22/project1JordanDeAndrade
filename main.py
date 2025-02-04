# # Jordan DeAndrade
# # comp490 capstone
# # project1
# # 1/29/25

import google.generativeai as genai
import json
from api import api_key

genai.configure(api_key=api_key) #API.py

# Looks at JSON
job_listings = []
with open("rapid_jobs2.json", "r") as file:
    for line in file:
        try:
            job_listings.append(json.loads(line.strip()))
        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON line: {e}")



# Exception Handling
if not job_listings or not isinstance(job_listings, list):
    raise ValueError("Job listings were not properly loaded.")




# Flatten the job listings
if isinstance(job_listings[0], list):
    job_listings = job_listings[0]




# Displays jobs to user
print("\nAvailable Job Listings:")
for index, job in enumerate(job_listings, start=1):
    if isinstance(job, dict):
        print(f"{index}. {job.get('title', 'Unknown Job')} at {job.get('company', 'Unknown Company')}")
    else:
        print(f"{index}. Invalid job format")




# Prompt user to choose a job
while True:
    try:
        choice = int(input("\nEnter the number of the job you'd like to apply for: ")) - 1
        if 0 <= choice < len(job_listings):
            job = job_listings[choice]
            break
        else:
            print("Invalid choice, please enter a valid job number.")
    except ValueError:
        print("Invalid input, please enter a number.")




# basecases
print(f"Selected job: {job.get('title', 'Unknown Job Title')} at {job.get('company', 'Unknown Company')}")

job_description = job.get("description", "No description available")
job_title = job.get("title", "Unknown Job Title")
company_name = job.get("company", "Unknown Company")

#questions


print("\nLet's customize your resume. Please answer the following questions:")

name = input("Full Name: ").strip()
university = input("University (or education background): ").strip()
experience = input("Briefly describe your experience (e.g., programming languages, software development, etc.): ").strip()
projects = []
print("\nEnter your key projects (press Enter when done):")
while True:
    project = input("Project: ").strip()
    if project == "":
        break
    projects.append(f"- {project}")



# Build personal description dynamically
personal_description = f"""
My name is {name}, and I am a student at {university}. I have experience in {experience}.
I have worked on various projects, including:
{chr(10).join(projects) if projects else '- No projects listed'}
"""

# Construct AI prompt
prompt = f"""Given the following job title: {job_title} at {company_name}
Job description:
{job_description} And the following personal description: {personal_description}
Please generate a resume in markdown format tailored to this job.
"""



# AI response
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
resume_text = response.text
print("\nGenerated Resume:\n")
print(resume_text)




# Saves resume
save_path = f"generated_resume_{job_title.replace(' ', '_')}.md"
with open(save_path, "w") as file:
    file.write(resume_text)

print(f"\nResume saved to {save_path}")
