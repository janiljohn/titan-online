# Science Fiction Novel API - FastAPI Edition
#
# Adapted from "Creating Web APIs with Python and Flask"
# <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>.
#
# Remove database
# rm var/titan_online.db
# compile the database
# ./bin/init.sh

import collections
import contextlib
import logging.config
import sqlite3
import typing

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlite3 import Connection, connect

class Settings(BaseSettings, env_file=".env", extra="ignore"):
  database: str
  logging_config: str

class Class(BaseModel):
  classID: int
  department: str
  sectionNum: int
  name: str
  maxEnrollement: int
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

# class
## GET
@app.get("/class/")
def get_classes(db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM Class")
  return {"Class": books.fetchall()}

## POST
@app.post("/class/enroll/")
def enroll_in_class(student_id: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):
  # cursor = db.cursor()

  # Check if student exists
  cur = db.execute("SELECT * FROM Student WHERE CWID = ?", (student_id,))
  student = cur.fetchone()
  if not student:
      raise HTTPException(status_code=404, detail="Student not found")

  # Check if class exists and is not full
  cur = db.execute("SELECT * FROM Class WHERE classID = ? AND currentEnrollment < maxEnrollement", (class_id,))
  class_info = cur.fetchone()
  if not class_info:
      raise HTTPException(status_code=400, detail="Class not found or is full")
  
  # Check if already enrolled
  cur = db.execute("SELECT * FROM Enrollment WHERE CWID = ? AND classID = ? AND dropped = 0", (student_id, class_id))
  enrollment = cur.fetchone()
  if enrollment:
      raise HTTPException(status_code=400, detail="Already enrolled in the class")

  newID = str(student_id) + "" + str(class_id)

  # Enroll student
  cur = db.execute("INSERT INTO Enrollment (enrollmentID, CWID, classID, enrollmentDate, dropped) VALUES (?, ?, ?, ?, 0)", (newID, student_id, class_id, 'your_enrollment_date'))
  cur = db.execute("UPDATE Class SET currentEnrollment = currentEnrollment + 1 WHERE classID = ?", (class_id,))
  db.commit()

  return {"status": "success", "message": "Enrollment successful"}

## POST
@app.post("/class/drop")
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

## POST
@app.post("/class/add", status_code=status.HTTP_201_CREATED)
def create_class(department: str, sectionNum: int, name: str ,maxEnrollement: int ,currentEnrollment: int ,professorID: int, db: sqlite3.Connection = Depends(get_db)
):
  
  try:
    # Insert class details into the database
    class_number = db.execute("SELECT COUNT(*) FROM Class")
    num = class_number.fetchone()[0] + 1

    cur = db.execute(
        """
        INSERT INTO Class (classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (num, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID)
    )
    db.commit()
    return {"message": f"Class {num} added successfully"}
  except sqlite3.IntegrityError as e:
      raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail={"type": type(e).__name__, "msg": str(e)},
      )

## POST
@app.post("/class/remove")
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

## POST
@app.post("/class/changeProfessor")
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

# professor
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

## GET
@app.get("/professor/{professorID}/class/dropped/")
def get_prof_dropped_students(professorID: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT Enrollment.enrollmentID, Enrollment.CWID, Enrollment.classID, Enrollment.enrollmentDate, Enrollment.dropped FROM Enrollment JOIN Class ON Enrollment.classID = Class.classID AND Enrollment.dropped = 1 JOIN Professor ON Professor.professorID=? AND Class.professorID=?", (professorID, professorID))
  return {"Class": books.fetchall()}

# enrollment
## GET
@app.get("/enrollement/")
def get_enrollement(db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM Enrollment")
  return {"Class": books.fetchall()}

## GET
@app.get("/instructors/classes/{classID}/waitlist")
def get_class_waitlist(classID: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM WaitingList WHERE classID = ?", (classID,))
  return {"Class": books.fetchall()}

## POST
@app.post("/professor/class/drop_student")
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

# student
## GET
@app.get("/student/")
def get_student(db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM Student")
  return {"Class": books.fetchall()}

## GET
@app.get("/students/{CWID}/waiting_list_position")
def get_student_waitlist_pos(CWID: int, response: Response, db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT position from WaitingList WHERE CWID = ?", (CWID,))
  return {"Class": books.fetchall()}

# waiting list
## GET
@app.get("/waitinglist/")
def get_waitinglist(db: sqlite3.Connection = Depends(get_db)):
  books = db.execute("SELECT * FROM WaitingList")
  return {"Class": books.fetchall()}

@app.post("/students/{CWID}/waiting_list/remove")
def remove_student_from_waiting_list(CWID: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        # Check if student exists
        cur = db.execute("SELECT * FROM Student WHERE CWID = ?", (CWID,))
        student = cur.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Check if student is in waiting list
        cur = db.execute("SELECT * FROM WaitingList WHERE CWID = ?", (CWID,))
        waiting_entry = cur.fetchone()
        if not waiting_entry:
            raise HTTPException(status_code=400, detail="Student is not in waiting list")

        # Remove student from waiting list
        cur = db.execute("DELETE FROM WaitingList WHERE CWID = ?", (CWID,))
        db.commit()

        return {"message": f"Student {CWID} removed from waiting list"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
