-- ./bin/init.sh
-- sqlite3 var/titan_online.db .dump

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS Student;
CREATE TABLE Student (
    CWID INT PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    email TEXT
);

DROP TABLE IF EXISTS Professor;
CREATE TABLE Professor (
    professorID INT PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    email TEXT
);

DROP TABLE IF EXISTS Class;
CREATE TABLE Class (
    classID INT PRIMARY KEY,
    department TEXT,
    sectionNum INT,
    name TEXT,
    maxEnrollement INT,
    currentEnrollment INT,
    professorID INT,
    FOREIGN KEY (professorID) REFERENCES Professor(professorID)
);

DROP TABLE IF EXISTS Enrollment;
CREATE TABLE Enrollment (
    enrollmentID INT PRIMARY KEY,
    CWID INT,
    classID INT,
    enrollmentDate DATE,
    dropped BOOLEAN,
    FOREIGN KEY (CWID) REFERENCES Student(CWID),
    FOREIGN KEY (classID) REFERENCES Class(classID)
);

DROP TABLE IF EXISTS WaitingList;
CREATE TABLE WaitingList (
    waitingID INT PRIMARY KEY,
    CWID INT,
    classID INT,
    position INT,
    FOREIGN KEY (CWID) REFERENCES Student(CWID),
    FOREIGN KEY (classID) REFERENCES Class(classID)
);

INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(1, 'Jessica', 'Pearson', 'jpearson@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(2, 'David', 'Hardman', 'dhardman@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(3, 'Rahael', 'Zane', 'rzane@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(4, 'Donna', 'Paulson', 'dpaulson@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(5, 'Carl', 'Malone', 'cmalonee@csu.fullerton.edu');

INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(1, 'Louis', 'Litt', 'llitt@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(2, 'Harvey', 'Spector', 'hspector@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(3, 'Mike', 'Ross', 'mross@fullerton.edu');

INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(1, 'Ethics', 2, 'Intro to Ethics',35, 4, 1);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(2, 'Corporate Law', 5, 'Foreign Affairs 101',40, 18, 2);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(3, 'Investment Banking', 9, 'Intro to Stock Regulations',35, 34, 3);

INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(11, 1, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(12, 1, 3, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(21, 2, 2, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(22, 2, 3, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(31, 3, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(32, 3, 2, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(41, 4, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(42, 4, 2, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(43, 4, 3, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(51, 5, 2, '2023-08-5', 1);

INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(11, 2, 3, 1);

COMMIT;