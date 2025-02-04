import google.generativeai as genai
import json
from api import api_key

# Configure the API
genai.configure(api_key=api_key)

# Load job listings from JSON
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

# Flatten the job listings if needed
if isinstance(job_listings[0], list):
    job_listings = job_listings[0]

# Display jobs to the user
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
        print("Invalid choice, please enter a valid job number.")
    except ValueError:
        print("Invalid input, please enter a number.")

# Selected job details
print(f"Selected job: {job.get('title', 'Unknown Job Title')} at {job.get('company', 'Unknown Company')}")

job_description = job.get("description", "No description available")
job_title = job.get("title", "Unknown Job Title")
company_name = job.get("company", "Unknown Company")

# Gather user details
print("\nLet's customize your resume. Please answer the following questions:")
name = input("Full Name: ").strip()
university = input("University (or education background): ").strip()
experience = input("Briefly describe your experience (e.g., programming languages, software development, etc.): ").strip()

# Collect projects
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
{job_description}
And the following personal description: {personal_description}
Please generate a resume in markdown format tailored to this job.
"""

# AI response
gen_model = genai.GenerativeModel("gemini-1.5-flash")
response = gen_model.generate_content(prompt)
resume_text = response.text

# Display generated resume
print("\nGenerated Resume:\n")
print(resume_text)

# Save resume
save_path = f"generated_resume_{job_title.replace(' ', '_')}.md"
with open(save_path, "w") as file:
    file.write(resume_text)

print(f"\nResume saved to {save_path}")
