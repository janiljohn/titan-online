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
VALUES(5, 'Carl', 'Malone', 'cmalone@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(6, 'Alice', 'Johnson', 'ajohnson@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(7, 'Jackson', 'Smith', 'jsmith@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(8, 'Charlie', 'Brown', 'cbrown@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(9, 'Diana', 'Ross', 'dross@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(10, 'Edward', 'Norton', 'enorton@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(11, 'Fiona', 'Apple', 'fapple@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(12, 'George', 'Clooney', 'gclooney@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(13, 'Hannah', 'Montana', 'hmontana@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(14, 'Isabel', 'Diaz', 'idiaz@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(15, 'Nick', 'Miller', 'nmiller@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(16, 'Kevin', 'Hart', 'khart@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(17, 'Laura', 'Dern', 'ldern@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(18, 'Mike', 'Myers', 'mmyers@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(19, 'Nicole', 'Kidman', 'nkidman@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(20, 'Oprah', 'Winfrey', 'owinfrey@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(21, 'Paul', 'Rudd', 'prudd@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(22, 'Quincy', 'Jones', 'qjones@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(23, 'Robert', 'Downey', 'rdowney@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(24, 'Sandra', 'Bullock', 'sbullock@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(25, 'Tom', 'Hanks', 'thanks@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(26, 'Uma', 'Thurman', 'uthurman@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(27, 'Vin', 'Diesel', 'vdiesel@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(28, 'Will', 'Smith', 'wsmith@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(29, 'Xena', 'Warrior', 'xwarrior@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(30, 'Yara', 'Shahidi', 'yshahidi@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(31, 'Zach', 'Efron', 'zefron@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(32, 'Alan', 'Turing', 'aturing@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(33, 'Ada', 'Lovelace', 'alovelace@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(34, 'Elon', 'Musk', 'emusk@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(35, 'Isaac', 'Newton', 'inewton@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(36, 'Steve', 'Jobs', 'sjobs@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(37, 'Bill', 'Gates', 'bgates@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(38, 'Margaret', 'Hamilton', 'mhamilton@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(39, 'Katherine', 'Johnson', 'kjohnson@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(40, 'Grace', 'Hopper', 'ghopper@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(41, 'Albert', 'Einstein', 'aeinstein@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(42, 'Marie', 'Curie', 'mcurie@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(43, 'Neil', 'Armstrong', 'narmstrong@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(44, 'Buzz', 'Aldrin', 'baldrin@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(45, 'Yuri', 'Gagarin', 'ygagarin@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(46, 'Mae', 'Jemison', 'mjemison@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(47, 'Chris', 'Hadfield', 'chadfield@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(48, 'Sally', 'Ride', 'sride@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(49, 'Carl', 'Sagan', 'csagan@csu.fullerton.edu');
INSERT INTO Student(CWID, firstName, lastName, email)
VALUES(50, 'Stephen', 'Hawking', 'shawking@csu.fullerton.edu');

INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(1, 'Louis', 'Litt', 'llitt@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(2, 'Harvey', 'Spector', 'hspector@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(3, 'Mike', 'Ross', 'mross@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(4, 'Jack', 'Black', 'jblack@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(5, 'Alice', 'Johnson', 'ajohnson@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(6, 'Brian', 'Smith', 'bsmith@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(7, 'Catherine', 'Taylor', 'ctaylor@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(8, 'Daniel', 'Lee', 'dlee@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(9, 'Elizabeth', 'Brown', 'ebrown@fullerton.edu');
INSERT INTO Professor(professorID, firstName, lastName, email) 
VALUES(10, 'Frank', 'Wilson', 'fwilson@fullerton.edu');


INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(1, 'Ethics', 2, 'Intro to Ethics',35, 4, 1);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(2, 'Corporate Law', 5, 'Foreign Affairs 101',40, 18, 2);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(3, 'Investment Banking', 9, 'Intro to Stock Regulations',35, 34, 3);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(4, 'Computer Science', 10, 'Data Structures', 30, 20, 9);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(5, 'Physics', 15, 'Quantum Mechanics', 25, 15, 5);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(6, 'Mathematics', 3, 'Linear Algebra', 28, 22, 6);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(7, 'History', 7, 'World History 101', 35, 30, 7);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(8, 'Biology', 12, 'Human Anatomy', 30, 25, 8);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(9, 'Music', 5, 'Intro to Rock Music', 25, 20, 4);
INSERT INTO Class(classID, department, sectionNum, name, maxEnrollement, currentEnrollment, professorID) 
VALUES(10, 'Chemistry', 8, 'Organic Chemistry', 28, 24, 10);


INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(11, 1, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(13, 1, 3, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(22, 2, 2, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(23, 2, 3, '2023-08-5', 0);
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
VALUES(52, 5, 2, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(64, 6, 4, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(74, 7, 4, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(85, 8, 5, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(95, 9, 5, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(106, 10, 6, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(116, 11, 6, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(110, 11, 10, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(124, 12, 4, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(127, 12, 7, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(131, 13, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(137, 13, 7, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(147, 14, 7, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(148, 14, 8, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(158, 15, 8, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(169, 16, 9, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(1710, 17, 10, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(181, 18, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(192, 19, 2, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(205, 20, 5, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(2110, 21, 10, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(222, 22, 2, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(233, 23, 3, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(244, 24, 4, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(257, 25, 7, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(268, 26, 8, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(279, 27, 9, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(2810, 28, 10, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(291, 29, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(303, 30, 3, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(315, 31, 5, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(324, 32, 4, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(336, 33, 6, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(347, 34, 7, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(358, 35, 8, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(369, 36, 9, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(3710, 37, 10, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(381, 38, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(392, 39, 2, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(403, 40, 3, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(415, 41, 5, '2023-08-5', 1);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(424, 42, 4, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(436, 43, 6, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(447, 44, 7, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(451, 45, 1, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(463, 46, 3, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(478, 47, 8, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(484, 48, 4, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(4910, 49, 10, '2023-08-5', 0);
INSERT INTO Enrollment(enrollmentID, CWID, classID, enrollmentDate, dropped)
VALUES(509, 50, 9, '2023-08-5', 1);


INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(11, 2, 3, 1);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(12, 5, 3, 2);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(13, 7, 3, 3);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(14, 12, 1, 1);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(15, 15, 1, 2);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(16, 20, 1, 3);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(17, 22, 5, 1);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(18, 25, 5, 2);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(19, 28, 6, 1);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(20, 32, 6, 2);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(21, 36, 2, 1);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(22, 40, 2, 2);
INSERT INTO WaitingList(waitingID, CWID, classID, position)
VALUES(23, 44, 4, 1);

COMMIT;