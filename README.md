Jordan DeAndrade - COMP490 Capstone - Project 1

Project Overview

This project is designed to generate tailored resumes based on job listings. It integrates Google Gemini API to generate resume content dynamically. The program processes job listings from a JSON file, prompts the user for relevant details, and constructs a customized resume in markdown format.

Features

Reads and processes job listings from rapid_jobs2.json

Provides a list of available jobs for the user to choose from

Prompts the user for personal details and relevant experience

Constructs an AI-generated resume using Google Gemini API

Saves the generated resume in a markdown file

Prerequisites

Python 3.x

google-generativeai package

A valid API key stored in api.py

rapid_jobs2.json containing job listings in JSON format

Installation

Install dependencies:

pip install google-generativeai

Ensure api.py contains your API key:

api_key = "your_api_key_here" (key may be provided)

Ensure rapid_jobs2.json contains valid job listings in JSON format.

Usage

Run the script:

python script.py

Follow the on-screen prompts:

Select a job listing from the displayed list

Enter personal details such as name, education, and experience

Enter key projects (optional)

The AI will generate a resume based on the input.

The generated resume will be saved as generated_resume_<job_title>.md.

Error Handling

Handles invalid JSON lines in rapid_jobs2.json

Ensures job listings are properly loaded before proceeding

Validates user input for job selection

Output

The generated resume is displayed on the console

A markdown file containing the resume is saved in the project directory

Author

Jordan DeAndrade

Email: j2deandrade@student.bridgew.edu

GitHub: www.github.com/jdeandrade22

License

This project is for educational purposes as part of the COMP490 Capstone project.
