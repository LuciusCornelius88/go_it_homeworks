import sqlite3
from datetime import datetime
from faker import Faker
from random import randint, choice


N_STUDENTS = 30
N_PROFESSORS = 3
N_SUBJECTS = 5
N_GROUPS = 3
N_MARKS = 20


def create_data(n_students, n_professors, n_subjects, n_groups):
	
	fake_data_generator = Faker('en-US')

	groups = []
	students = []
	professors = []

	subjects = ['Web development', 'Operational systems', 
				'Data science foundations', 'Calculus', 'English'] 
	

	for _ in range(n_groups):
		groups.append(fake_data_generator.bothify(text='?-##', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

	for _ in range(n_students):
		students.append(fake_data_generator.name())

	for _ in range(n_professors):
		professors.append('Dr. ' + fake_data_generator.name())

	return groups, students, professors, subjects


def prepare_data(groups, students, professors, subjects):

	tup_groups = []
	tup_students = []
	tup_subjects = [] 
	tup_marks = [] 


	for group in groups:
		tup_groups.append((group,))


	for student in students:
		tup_students.append((student, randint(1, N_GROUPS)))


	for subject in subjects:
		tup_subjects.append((subject, choice(professors)))


	for student_id in range(1, N_STUDENTS + 1):
		for _ in range(N_MARKS):
			date = datetime(2022, randint(1, 12), randint(1, 28)).date()
			mark = randint(60, 100) 
			subject_id = randint(1, N_SUBJECTS)
			tup_marks.append((date, mark, subject_id, student_id))


	return tup_groups, tup_students, tup_subjects, tup_marks


def fill_data(groups, students, subjects, marks):
	
	with sqlite3.connect('study.db') as conn:
		cursor = conn.cursor()

		groups_script = '''INSERT INTO groups(group_code) 
						   VALUES (?)'''

		students_script = '''INSERT INTO students(name, group_id)
							 VALUES (?, ?)'''

		subjects_script = '''INSERT INTO subjects(name, professor)
							 VALUES (?, ?)'''

		marks_script = '''INSERT INTO marks(date_of, value, subject_id, student_id)
						  VALUES (?, ?, ?, ?)'''

		cursor.executemany(groups_script, groups)
		cursor.executemany(students_script, students)
		cursor.executemany(subjects_script, subjects)
		cursor.executemany(marks_script, marks)

		conn.commit()


if __name__ == '__main__':
	groups, students, professors, subjects = create_data(N_STUDENTS, N_PROFESSORS, N_SUBJECTS, N_GROUPS)
	groups, students, professors, subjects = prepare_data(groups, students, professors, subjects)
	fill_data(groups, students, professors, subjects)

	print('Done!')