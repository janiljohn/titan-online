PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Class;
CREATE TABLE Class (
    classID INT PRIMARY KEY,
    department TEXT,
    sectionNum INT,
    -- name TEXT,
    maxEnrollement INT,
    currentEnrollment INT,
    professorID INT
    -- FOREIGN KEY (professorID) REFERENCES Professor(professorID)
);

INSERT INTO Class(classID, department, sectionNum, maxEnrollement, currentEnrollment, professorID) VALUES(1, 'Computer Science', 2, 3, 4, 5);