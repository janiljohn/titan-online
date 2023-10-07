# Science Fiction Novel API - FastAPI Edition
#
# Adapted from "Creating Web APIs with Python and Flask"
# <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>.
#

import collections
import contextlib
import logging.config
import sqlite3
import typing

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlite3 import Connection, connect
from datetime import datetime
from fastapi import HTTPException, Depends, status
from fastapi import status

class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

class Class(BaseModel):
    classID: int
    department: str
    sectionNum: int
    maxEnrollment: int
    currentEnrollment: int
    professorID: int

class Professor(BaseModel):
    professorID: int
    firstName: str
    lastName: str
    email: str

class Enrollment(BaseModel):
    enrollmentID: int
    CWID: int
    classID: int
    enrollmentDate: str
    dropped: bool

class WaitingList(BaseModel):
    waitingID: int
    CWID: int
    classID: int
    position: int

class Database:
    def __init__(self, database_path):
        self._database_path = database_path
        self._pool = []

    def get_connection(self) -> Connection:
        if not self._pool:
            connection = connect(self._database_path)
        else:
            connection = self._pool.pop()
        connection.row_factory = sqlite3.Row
        return connection

    def return_connection(self, connection: Connection):
        self._pool.append(connection)

# Create a global instance of the Database class
database = Database("var/titan_online.db")

def get_db():
    db = database.get_connection()
    try:
        yield db
    finally:
        database.return_connection(db)

def get_logger():
    return logging.getLogger(__name__)


settings = Settings()
app = FastAPI()

logging.config.fileConfig(settings.logging_config, disable_existing_loggers=False)


# Students
## GET
@app.get("/students/")
def get_students(db: sqlite3.Connection = Depends(get_db)):
  cur = db.execute("SELECT * FROM Student")
  return {"Class": cur.fetchall()}

# Class
## GET
@app.get("/class/")
def get_classes(db: sqlite3.Connection = Depends(get_db)):
  cur = db.execute("SELECT * FROM Class")
  return {"Class": cur.fetchall()}

## POST
@app.post("/student/class/enroll/")
def enroll_in_class(student_id: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):
    enrollment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = db.execute("SELECT auto_enrollment FROM Settings")
    setting = cur.fetchone()

    if not setting or not setting[0]: 
      raise HTTPException(status_code=400, detail="Auto enrollment is currently disabled")
    # Check if student exists
    cur = db.execute("SELECT * FROM Student WHERE CWID = ?", (student_id,))
    student = cur.fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if class exists
    cur = db.execute("SELECT * FROM Class WHERE classID = ?", (class_id,))
    class_info = cur.fetchone()
    if not class_info:
        raise HTTPException(status_code=400, detail="Class not found")

    # Check if already enrolled 
    cur = db.execute("SELECT * FROM Enrollment WHERE CWID = ? AND classID = ? AND dropped = 0", (student_id, class_id))
    enrollment = cur.fetchone()
    if enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in the class")
    
    # Check if already in the waiting list
    cur = db.execute("SELECT * FROM WaitingList WHERE CWID = ? AND classID = ?", (student_id, class_id))
    waiting = cur.fetchone()
    if waiting:
        raise HTTPException(status_code=400, detail="Already on the waiting list for this class")

    # Check if class is full
    if class_info['currentEnrollment'] < class_info['maxEnrollment']:
        # Enroll student
        cur = db.execute("INSERT INTO Enrollment (CWID, classID, enrollmentDate, dropped) VALUES (?, ?, ?, 0)", (student_id, class_id, enrollment_date))
        cur = db.execute("UPDATE Class SET currentEnrollment = currentEnrollment + 1 WHERE classID = ?", (class_id,))
        db.commit()
        return {"status": "success", "message": "Enrollment successful"}
    else:
        # Check if student is in fewer than 3 waiting lists
        cur = db.execute("SELECT COUNT(*) FROM WaitingList WHERE CWID = ?", (student_id,))
        waiting_count = cur.fetchone()[0]
        if waiting_count >= 3:
            raise HTTPException(status_code=400, detail="Cannot be on more than 3 waiting lists")

        # Check if waiting list is full (max is 15)
        cur = db.execute("SELECT COUNT(*) FROM WaitingList WHERE classID = ?", (class_id,))
        waiting_list_count = cur.fetchone()[0]
        if waiting_list_count >= 15:
            raise HTTPException(status_code=400, detail="Waiting list is full, cannot add more students")

        # Add student to waiting list
        position = waiting_list_count + 1  # Next position in the waiting list
        cur = db.execute("INSERT INTO WaitingList (CWID, classID, position, enrollmentDate) VALUES (?, ?, ?, ?)", (student_id, class_id, position, enrollment_date))
        db.commit()
        return {"status": "success", "message": "Class is full. Added to waiting list at position {}".format(position)}

def handle_waiting_list(class_id: int, db: sqlite3.Connection):
    # Check the setting here
    cur = db.execute("SELECT auto_enrollment FROM Settings")
    setting = cur.fetchone()
    if not setting or not setting[0]:
        raise HTTPException(status_code=400, detail="Auto enrollment is currently disabled")
    # Get the student at the front of the waiting list
    cur = db.execute("SELECT * FROM WaitingList WHERE classID = ? ORDER BY enrollmentDate ASC LIMIT 1", (class_id,))
    waiting_student = cur.fetchone()

    if waiting_student:
        # Enroll this student
        student_id = waiting_student['CWID']
        enrollment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur = db.execute("INSERT INTO Enrollment (CWID, classID, enrollmentDate, dropped) VALUES (?, ?, ?, 0)", (student_id, class_id, enrollment_date))
        cur = db.execute("UPDATE Class SET currentEnrollment = currentEnrollment + 1 WHERE classID = ?", (class_id,))

        # Remove this student from the waiting list
        cur = db.execute("DELETE FROM WaitingList WHERE waitingID = ?", (waiting_student['waitingID'],))

        # Optionally, update positions of remaining students in the waiting list if you are maintaining 'position' values
        # (this part can be omitted if 'position' values are not crucial for your application)
        cur = db.execute("SELECT * FROM WaitingList WHERE classID = ? ORDER BY enrollmentDate ASC", (class_id,))
        remaining_students = cur.fetchall()
        for position, student in enumerate(remaining_students, start=1):
            cur = db.execute("UPDATE WaitingList SET position = ? WHERE waitingID = ?", (position, student['waitingID']))

        db.commit()

# PUT
@app.put("/student/class/drop")
def drop_class(student_id: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):
  # Check if student exists
  cur = db.execute("SELECT * FROM Student WHERE CWID = ?", (student_id,))
  student = cur.fetchone()
  if not student:
      raise HTTPException(status_code=404, detail="Student not found")

  # Check if already enrolled
  cur = db.execute("SELECT * FROM Enrollment WHERE CWID = ? AND classID = ? AND dropped = 0", (student_id, class_id))
  enrollment = cur.fetchone()
  if enrollment==False:
      raise HTTPException(status_code=400, detail="Never enrolled in the class")

  # Delete enrollment
  # cur = db.execute("DELETE FROM Enrollment WHERE CWID = ? AND classID = ?", (student_id, class_id))
  cur = db.execute("UPDATE Enrollment SET dropped = 1 WHERE classID = ? AND CWID = ?", (class_id, student_id))
  cur = db.execute("UPDATE Class SET currentEnrollment = currentEnrollment - 1 WHERE classID = ?", (class_id,))
  db.commit()
  return {"status": "success", "message": "Disenrollment successful"}

# Enrollment
## GET
@app.get("/enrollment/")
def get_enrollment(db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM Enrollment WHERE dropped = 0")
  return {"Class": books.fetchall()}

# Professor
## GET
@app.get("/professor/")
def get_professor(db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM Professor")
  return {"Class": books.fetchall()}

## GET
@app.get("/professor/{professorID}/class/enrollment/")
def get_prof_enrollment(professorID: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT Enrollment.enrollmentID, Enrollment.CWID, Enrollment.classID, Enrollment.enrollmentDate, Enrollment.dropped FROM Enrollment JOIN Class ON Enrollment.classID = Class.classID AND Enrollment.dropped = 0 JOIN Professor ON Professor.professorID=? AND Class.professorID=?", (professorID, professorID))
  return {"Class": books.fetchall()}

## PUT
@app.put("/professor/class/drop_student")
def drop_student(professorID: int, CWID: int, class_id: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
  cur = db.execute("SELECT * FROM Professor WHERE professorID = ?", (professorID,))
  professor = cur.fetchone()

  # check if professor exists
  if not professor:
     raise HTTPException(status_code=404, detail="Professor not found")
  # Delete enrollment
  cur = db.execute("UPDATE Enrollment SET dropped = 1 WHERE classID = ? AND CWID = ?", (class_id, CWID))
  cur = db.execute("UPDATE Class SET currentEnrollment = currentEnrollment - 1 WHERE classID = ?", (class_id,))
  db.commit()
  return {"message": f"Student {CWID} dropped from classes by Professor {professorID}"}

# Registrar
## POST
@app.post("/registrar/class/add", status_code=status.HTTP_201_CREATED)
def create_class(department: str, sectionNum: int, name: str ,maxEnrollment: int ,currentEnrollment: int ,professorID: int, db: sqlite3.Connection = Depends(get_db)
):
  
  try:
    # Insert class details into the database
    class_number = db.execute("SELECT COUNT(*) FROM Class")
    num = class_number.fetchone()[0] + 1

    cur = db.execute(
        """
        INSERT INTO Class (classID, department, sectionNum, name, maxEnrollment, currentEnrollment, professorID)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (num, department, sectionNum, name, maxEnrollment, currentEnrollment, professorID)
    )
    db.commit()
    return {"message": f"Class {num} added successfully"}
  except sqlite3.IntegrityError as e:
      raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail={"type": type(e).__name__, "msg": str(e)},
      )

## DELETE
@app.delete("/registrar/class/remove")
def remove_class(classID: int, db: sqlite3.Connection = Depends(get_db)):

  try:
      # Delete class from the database
      cur = db.execute("DELETE FROM Class WHERE classID = ?", (classID,))
      db.commit()
      return {"message": f"Class {classID} removed successfully"}
  except Exception as e:
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail={"type": type(e).__name__, "msg": str(e)},
      )

# PUT
@app.put("/registrar/class/changeProfessor")
def change_professor(classID: int, professorID: int , db: sqlite3.Connection = Depends(get_db)):
  # gotta add more stuff here
  try:
      # Update professor for the class in the database
      cur = db.execute("UPDATE Class SET professorID = ? WHERE classID = ?", (professorID, classID))
      db.commit()
      return {"message": f"Professor for class {classID} changed successfully"}
  except Exception as e:
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail={"type": type(e).__name__, "msg": str(e)},
      )

## POST
@app.post("/registrar/waitinglist")
async def set_auto_enrollment(auto_enrollment_status: bool, db: sqlite3.Connection = Depends(get_db)):
    try:
        # Update the auto_enrollment setting
        db.execute("UPDATE Settings SET auto_enrollment = ?", (auto_enrollment_status,))
        db.commit()
        return {"status": "success", "message": f"Auto enrollment set to {auto_enrollment_status}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Waiting List
## GET
@app.get("/waitinglist/")
def get_waitinglist(db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM WaitingList")
  return {"Class": books.fetchall()}

## GET
@app.get("/students/{CWID}/waiting_list_position")
def get_student_waitlist_pos(CWID: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT position from WaitingList WHERE CWID = ?", (CWID,))
  return {"Class": books.fetchall()}

# DELETE
@app.delete("/students/{CWID}/waiting_list/remove/{classID}")
def remove_student_from_waiting_list(CWID: int, classID: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        # Check if student exists
        cur = db.execute("SELECT * FROM Student WHERE CWID = ?", (CWID,))
        student = cur.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Check if student is in waiting list for a specific class
        cur = db.execute("SELECT * FROM WaitingList WHERE CWID = ? AND classID = ?", (CWID, classID))
        waiting_entry = cur.fetchone()
        if not waiting_entry:
            raise HTTPException(status_code=400, detail="Student is not in waiting list for the specified class")

        # Remove student from waiting list
        cur = db.execute("DELETE FROM WaitingList WHERE CWID = ? AND classID = ?", (CWID, classID))

        # Get the next student in the waiting list for the specific class
        cur = db.execute("SELECT * FROM WaitingList WHERE classID = ? ORDER BY position ASC LIMIT 1", (classID,))
        next_waiting_student = cur.fetchone()
        if next_waiting_student:
            # Promote the next student in the waiting list
            cur = db.execute("UPDATE WaitingList SET position = position - 1 WHERE classID = ?", (classID,))
        db.commit()

        return {"message": f"Student {CWID} removed from waiting list"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
  
## GET
@app.get("/professor/{professorID}/classes/{classID}/waitlist")
def get_class_waitlist(professorID: int, classID: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
    # Check if professor exists
    cur = db.execute("SELECT * FROM Professor WHERE professorID = ?", (professorID,))
    professor = cur.fetchone()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    # Check if class belongs to the professor
    cur = db.execute("SELECT * FROM Class WHERE classID = ? AND professorID = ?", (classID, professorID))
    class_info = cur.fetchone()
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found or does not belong to the professor")

    # Get the waiting list for the specified class
    cur = db.execute("SELECT * FROM WaitingList WHERE classID = ?", (classID,))
    waitlist_entries = cur.fetchall()

    return {"Class": waitlist_entries}

