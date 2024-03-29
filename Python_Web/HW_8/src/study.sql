-- Table: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	group_code VARCHAR(255) UNIQUE NOT NULL 
);


-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE NOT NULL,
	group_id INTEGER,

	FOREIGN KEY(group_id) REFERENCES groups(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);


-- Table: subjects
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) UNIQUE NOT NULL,
	professor VARCHAR(255) NOT NULL
);


-- Table: marks
DROP TABLE IF EXISTS marks;
CREATE TABLE marks (
	date_of DATE NOT NULL,
	value INTEGER NOT NULL,
	subject_id INTEGER,
	student_id INTEGER,

	FOREIGN KEY(subject_id) REFERENCES subjects(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	FOREIGN KEY(student_id) REFERENCES students(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE  
)

