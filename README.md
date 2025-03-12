## **Jordan DeAndrade - COMP490 Capstone - Project 1**

## **Sprint 4 (final Sprint)**
Implemented:
-Job Details shown in Job Details box once clicked
*Allow the user to create a profile and save it for later use
*allow the user to select any profile and upload the information
*Generate Cover Letter button added
*Save As  PDF button added
*Testing and linted updated aswell

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

 
## **Prerequisites**  
see requirements.txt

## **Installation**  

1. **Install dependencies:**  
   ```sh
   pip install google-generativeai
   pip install PySimpleGui
   pip install SQLite3
   pip install unitTest
   ##api key
Ensure rapid_jobs2.json contains valid job listings in JSON format.
## Usage

Run the script:
```sh
python main.py #1 time to generate savedJobs.db
python gui.py
python test_data_loading.py
```

## **Author**

Jordan DeAndrade

Email: j2deandrade@student.bridgew.edu

GitHub: www.github.com/jdeandrade22

License

This project is for educational purposes as part of the COMP490 Capstone project.
Partial ReadMe material written by Ollama
