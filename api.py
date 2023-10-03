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

class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

class Class(BaseModel):
    classID: int
    department: str
    sectionNum: int
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

def get_db():
    with contextlib.closing(sqlite3.connect(settings.database)) as db:
        db.row_factory = sqlite3.Row
        yield db


def get_logger():
    return logging.getLogger(__name__)


settings = Settings()
app = FastAPI()

logging.config.fileConfig(settings.logging_config, disable_existing_loggers=False)


@app.get("/class/")
def get_classes(db: sqlite3.Connection = Depends(get_db)):
    books = db.execute("SELECT * FROM Class")
    return {"Class": books.fetchall()}

@app.get("/enrollement/")
def get_enrollement(db: sqlite3.Connection = Depends(get_db)):
    books = db.execute("SELECT * FROM Enrollment")
    return {"Class": books.fetchall()}

@app.get("/professor/")
def get_professor(db: sqlite3.Connection = Depends(get_db)):
    books = db.execute("SELECT * FROM Professor")
    return {"Class": books.fetchall()}

@app.get("/student/")
def get_student(db: sqlite3.Connection = Depends(get_db)):
    books = db.execute("SELECT * FROM Student")
    return {"Class": books.fetchall()}

@app.get("/waitinglist/")
def get_waitinglist(db: sqlite3.Connection = Depends(get_db)):
    books = db.execute("SELECT * FROM WaitingList")
    return {"Class": books.fetchall()}

@app.post("/class/add", status_code=status.HTTP_201_CREATED)
def create_book(
    course: Class, response: Response, db: sqlite3.Connection = Depends(get_db)
):
    c = dict(Class)
    try:
        cur = db.execute(
            """
            INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID)
            VALUES(:classID, :department, :sectionNum, :name, :maxEnrollement, :currentEnrollment, :professorID)
            """,
            c,
        )
        db.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    c["classID"] = cur.lastrowid
    response.headers["Location"] = f"/books/{c['classID']}"
    return c


# @app.get("/books/{id}")
# def retrieve_book(
#     id: int, response: Response, db: sqlite3.Connection = Depends(get_db)
# ):
#     cur = db.execute("SELECT * FROM books WHERE id = ? LIMIT 1", [id])
#     books = cur.fetchall()
#     if not books:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
#         )
#     return {"books": books}


# SearchParam = collections.namedtuple("SearchParam", ["name", "operator"])
# SEARCH_PARAMS = [
#     SearchParam(
#         "author",
#         "LIKE",
#     ),
#     SearchParam(
#         "published",
#         "=",
#     ),
#     SearchParam(
#         "title",
#         "LIKE",
#     ),
#     SearchParam(
#         "first_sentence",
#         "LIKE",
#     ),
# ]


# @app.get("/search")
# def search(
#     author: typing.Optional[str] = None,
#     published: typing.Optional[str] = None,
#     title: typing.Optional[str] = None,
#     first_sentence: typing.Optional[str] = None,
#     db: sqlite3.Connection = Depends(get_db),
#     logger: logging.Logger = Depends(get_logger),
# ):
#     sql = "SELECT * FROM books"

#     conditions = []
#     values = []
#     arguments = locals()

#     for param in SEARCH_PARAMS:
#         if arguments[param.name]:
#             if param.operator == "=":
#                 conditions.append(f"{param.name} = ?")
#                 values.append(arguments[param.name])
#             else:
#                 conditions.append(f"{param.name} LIKE ?")
#                 values.append(f"%{arguments[param.name]}%")

#     if conditions:
#         sql += " WHERE "
#         sql += " AND ".join(conditions)

#     logger.debug(sql)
#     books = db.execute(sql, values)

#     return {"books": books.fetchall()}
