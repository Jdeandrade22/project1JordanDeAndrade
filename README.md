Sprint1:
## **Jordan DeAndrade - COMP490 Capstone - Project 1**

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
Follow the on-screen prompts:

## **Error Handling**

Handles invalid JSON lines in rapid_jobs2.json and rapidResults (1).json

Ensures job listings are properly loaded before proceeding

Validates user input for job selection

## output

The generated resume is displayed on the console

A markdown file containing the resume is saved in the project directory
A database where all of the potential jobs are listed

## Sprint2:
Able to read rapidResults.json

implimented test cases in test_data_loading.py to test json loading and db table creation
all scripts were linted with flake8



## **Author**

Jordan DeAndrade

Email: j2deandrade@student.bridgew.edu

GitHub: www.github.com/jdeandrade22

License

This project is for educational purposes as part of the COMP490 Capstone project.
Partial ReadMe material written by Ollama
