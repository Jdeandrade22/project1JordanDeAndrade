Sprint1:
## **Jordan DeAndrade - COMP490 Capstone - Project 1**
I decided to choose Google AI for this project because it did what I needed it to do and it was free and quick

The AI Prompt that I chose in this script is: prompt = (
        f"""Given the following job title: {job_title} at {company_name}\n"
        f"Job description:\n{job_description}\n"
        f"And the following personal description: {personal_description}\n"
        f"Please generate a resume in markdown format tailored to this job."""
    )

I found this to work the best because it is the most specific with the user inputs and would return the closest presentable resume
 
## **Prerequisites**  
- **Python 3.x**  
- **`google-generativeai` package**  
- **A valid API key** stored in `api.py`  
- **`rapid_jobs2.json`** containing job listings in JSON format  

## **Installation**  

1. **Install dependencies:**  
   ```sh
   pip install google-generativeai

   

Ensure api.py contains your API key
```sh
api_key = "your_api_key_here" (key may be provided)
```


Ensure rapid_jobs2.json contains valid job listings in JSON format.

## Usage

Run the script:
```sh
python main.py
python test_data_loading.py
```
Follow the on-screen prompts:

Select a job listing from the displayed list

Enter personal details such as name, education, and experience

Enter key projects (optional)

The AI will generate a resume based on the input.
```sh
The generated resume will be saved as generated_resume_<job_title>.md.
```
## **Error Handling**

Handles invalid JSON lines in rapid_jobs2.json and rapidResults (1).json

Ensures job listings are properly loaded before proceeding

Validates user input for job selection

## output

The generated resume is displayed on the console

A markdown file containing the resume is saved in the project directory
A database where all of the potential jobs are listed

Sprint2:
Able to read rapidResults.json

implimented test cases in test_data_loading.py to test json loading and db table creation
both scripts were linted with flake8
## **Author**

Jordan DeAndrade

Email: j2deandrade@student.bridgew.edu

GitHub: www.github.com/jdeandrade22

License

This project is for educational purposes as part of the COMP490 Capstone project.
Partial ReadMe material written by Ollama
