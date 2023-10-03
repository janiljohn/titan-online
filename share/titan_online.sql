PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Class;
CREATE TABLE Class (
    classID INT PRIMARY KEY,
    department TEXT,
    sectionNum INT,
    name TEXT,
    maxEnrollement INT,
    currentEnrollment INT,
    professorID INT
    -- FOREIGN KEY (professorID) REFERENCES Professor(professorID)
);

INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) VALUES(1, 'Computer Science', 2, 'test',3, 4, 5);
COMMIT;

DROP TABLE IF EXISTS Enrollment;
CREATE TABLE Enrollment (
    enrollmentID INT PRIMARY KEY,
    CWID INT,
    classID INT,
    enrollmentDate DATE,
    dropped BOOLEAN
    -- FOREIGN KEY (CWID) REFERENCES Student(CWID),
    -- FOREIGN KEY (classID) REFERENCES Class(classID)
);

DROP TABLE IF EXISTS Professor;
CREATE TABLE Professor (
    professorID INT PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    email TEXT
);

DROP TABLE IF EXISTS Student;
CREATE TABLE Student (
    CWID INT PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    email TEXT
);

DROP TABLE IF EXISTS WaitingList;
CREATE TABLE WaitingList (
    waitingID INT PRIMARY KEY,
    CWID INT,
    classID INT,
    position INT
    -- FOREIGN KEY (CWID) REFERENCES Student(CWID),
    -- FOREIGN KEY (classID) REFERENCES Class(classID)
);