# CPSC 449 - Web Back-End Engineering: Project 1 (Fall 2023)
Created by Group 8: Joel Anil John, Marco Gabriel, Vivian Cao, Maria Fernandez, Anurag Ganji 

## Project Title: Titan-Online 
In this project, we worked together to design and implement a back-end web service to manage course enrollment and waiting lists with functionality similar to TitanOnline. The technical tasks involved defining a RESTful service API that exposes the necessary resources and operations for classes and waiting lists. We created an SQL schema in third normal form and pre-populated the database with sample data. FastAPI was used to define endpoints following RESTful principles and to ensure all I/O representations are in JSON format. A procfile was provided for service start-up and to conduct tests with Foreman.

## Tasks
- Define API.
- Create a RESTful service.
- Design the database and define SQL schema.
- Implement the service using FastAPI.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
What things you need to install beforehand:

- Tuffix 2022 
- Python (version 3.8 or higher is recommended)
- FastAPI
- Uvicorn
- SQLite
- Command Line Shell For SQLite
- Foreman

### Installation 
A step by step series of examples that tell you how to get a development environment running using Tuffix 2022:
1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```

2. **Navigate into the project directory:**
    ```bash
    cd <project_directory>
    ```

3. **Remove Existing Database (if any):**
    If there is a pre-existing `titan_online.db` database file, remove it to start fresh.
    ```bash
    rm var/titan_online.db
    ```
4. **Compile the Database:**
    Initialize the new database using the provided initialization script.
    ```bash
    ./bin/init.sh
    ```
5. **Install any required python libraries**


### Running the Project
1. **Start the FastAPI server:**
    Navigate to the directory containing the titan-online application file and run the following command.
    ```bash
    uvicorn api:app --reload
    ```
2. Start the service using Foreman:
    ```bash
    foreman start
    ```
2. Access the API documentation at http://127.0.0.1:5000/docs.
3. Query the API with example parameters to test the database and verify correct setup.


## API Resources and Operations
### Classes

- Lists available classes
- Enrolls students in classes
- Drops classes
- Provides instructor functionalities: viewing enrollments, dropping students administratively.
- Provides registrar functionalities: adding classes, removing sections, changing instructors, freezing enrollment.

### Waiting Lists

- Automatic waiting list placement for full classes.
- Waiting lists are date-ordered with a max size of 15; students can be on a max of 3 lists.
- Student Functions: View waiting list position, remove from waiting list.
- Instructor Functions: View course waiting list.

#### Note
This is a back-end-only project with no requirement for front-end user interface development.

