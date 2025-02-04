## **Jordan DeAndrade - COMP490 Capstone - Project 1**

## **Project Overview**

This project is designed to generate tailored resumes based on job listings. It integrates Google Gemini API to generate resume content dynamically. The program processes job listings from a JSON file, prompts the user for relevant details, and constructs a customized resume in markdown format.

## **Features**  

- **Reads and processes job listings** from `rapid_jobs2.json`.  
- **Provides a list of available jobs** for selection.  
- **Prompts the user for personal details** and relevant experience.  
- **Uses Google Gemini AI** to generate a resume.  
- **Saves the generated resume** in a Markdown file.

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

Usage

Run the script:
```sh
python main.py
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

Handles invalid JSON lines in rapid_jobs2.json

Ensures job listings are properly loaded before proceeding

Validates user input for job selection

## output

The generated resume is displayed on the console

A markdown file containing the resume is saved in the project directory

## **Author**

Jordan DeAndrade

Email: j2deandrade@student.bridgew.edu

GitHub: www.github.com/jdeandrade22

License

This project is for educational purposes as part of the COMP490 Capstone project.
