## **Jordan DeAndrade - COMP490 Capstone - Project 1**

-Designed to help you create professional resumes and cover letters tailored to specific job postings. It uses AI to generate personalized documents and stores your information and job listings in a database, making it easy to apply for multiple jobs efficiently.

## **How to Run Program**

1. clone the project
   ```sh
   git clone https://github.com/Jdeandrade22/project1JordanDeAndrade.git

2. Install the dependencies
```sh
   pip install google-generativeai
   pip install PySimpleGui
   pip install markdown
   pip install pdfkit
   pip install wkhtmltopdf 
```
3.Install WKHTMLTOPDF.exe from https://wkhtmltopdf.org/downloads.html for your os

4. Change directory path of WKHTMLTOPDF (line 10) to where you would like the pdf's to download AFTER installing the .exe

   MacOS
 ```sh
   WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'
```

windows (some may be version specific)

```sh
   WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
```

5. Ensure api_secrets.py is created and contains your api key
   
```sh
   api_key = "Your_api_key_here"
```

6. run main.py to generate savedJobs.db
7. run Gui.py
8. select a job and it will display in the Job Details: section
9. enter User info in the designated areas then click save information for later use
10. click generate restume
11. once reading the resume in the popup x out and click Generate Cover Letter
12. if both are not up to satisfaction reclick the Generate Resume button and a new resume will apear
13. after both are to your liking make sure all popups are closed then click Save As PDF (will not work if popups are open)
14. ensure the pdf is in the saved location then edit to your liking!
15. run test_data_loading.py

     





## **Sprint 4 (final Sprint)**

Implemented:

-Job Details shown in Job Details box once clicked

-Allow the user to create a profile and save it for later use

-allow the user to select any profile and upload the information

-Generate Cover Letter button added

-Save As  PDF button added

-Implemented PDFkit to allow users to save

-Testing and linted updated aswell

## **sprint3**
-Implemented User features
*save templates for future application use 
*implemented testing 

-testing:
test_database_operations()

Ensures job listings table creation and data insertion work correctly.

test_load_json_data()

Verifies that job listings are correctly loaded from a JSON file.

test_fetch_job_details()

Tests that a job's full details can be retrieved using its ID.

test_save_user_details()

Checks if user details are correctly saved in the database.

test_fetch_users()

Ensures that saved user details can be fetched successfully.

test_fetch_jobs()

Verifies that job listings can be retrieved from the database.

test_generate_llm_response()

verifies that the llm returns a response to the user and API is working. 

test_save_user_details()

ensures that the user's details are saved.
create

-added a requirements.txt


-removed generating features of program for sprint


-New GUI Interface 


## **Author**

Jordan DeAndrade

Email: j2deandrade@student.bridgew.edu

GitHub: www.github.com/jdeandrade22

License

This project is for educational purposes as part of the COMP490 Capstone project.
Partial ReadMe material written by Ollama
