import sqlite3
from random import randint

# 5 студентов с наибольшим средним баллом по всем предметам
def best_avg_marks(cursor):
	query = '''SELECT ROUND(AVG(m.value), 2) AS avarage_mark, s.name
			   FROM marks AS m
			   LEFT JOIN students AS s ON s.id = m.student_id
			   GROUP BY s.name
			   ORDER BY avarage_mark DESC
			   LIMIT 5;
			'''

	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# 1 студент с наивысшим средним баллом по одному предмету
def max_avg_mark_pro_subj(cursor):
	query = '''SELECT MAX(max_avarage_mark) AS max_avarage_mark, avg.subject AS subject, avg.student AS student 
			   FROM(
				   SELECT ROUND(AVG(m.value), 2) AS max_avarage_mark, sub.name AS subject, s.name AS student
				   FROM marks AS m
				   LEFT JOIN students AS s ON s.id = m.student_id
   				   LEFT JOIN subjects AS sub ON sub.id = m.subject_id
				   GROUP BY s.name
			   ) AS avg
			   GROUP BY avg.subject;
			'''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# средний балл в группе по одному предмету
def avg_mark_pro_group_and_subj(cursor):
	query = '''SELECT ROUND(AVG(m.value), 2) AS avarage_mark, g.group_code, sub.name AS subject
			   FROM marks AS m
			   LEFT JOIN students AS s ON s.id = m.student_id
			   LEFT JOIN subjects AS sub ON sub.id = m.subject_id
			   LEFT JOIN groups AS g ON g.id = s.group_id
			   GROUP BY sub.name, g.group_code
			'''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Средний балл в потоке
def avg_mark_pro_group(cursor):
	query = '''SELECT ROUND(AVG(m.value)) as avarage_mark, g.group_code
			   FROM marks as m
			   LEFT JOIN students AS s ON s.id = m.student_id
			   LEFT JOIN groups as g ON g.id = s.group_id
			   GROUP BY g.group_code
			'''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Какие курсы читает преподаватель
def subjs_pro_prof(cursor, prof_name):
	query = f'''SELECT sub.name, sub.professor 
			    FROM subjects AS sub
			    WHERE sub.professor = '{prof_name}'
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Список студентов в группе
def students_in_group(cursor, group_id):
	query = f'''SELECT s.name AS student, g.group_code AS group_name
			    FROM students AS s
			    LEFT JOIN groups AS g ON g.id = s.group_id
			    WHERE s.group_id = {group_id}
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Оценки студентов в группе по предмету
def students_marks_in_group(cursor, group_id, subject):
	query = f'''SELECT s.name AS student, m.value AS mark
			    FROM marks AS m
			    LEFT JOIN students AS s ON s.id = m.student_id
			    LEFT JOIN subjects AS sub ON sub.id = m.subject_id
			    WHERE s.group_id = {group_id} AND sub.name = '{subject}'
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Оценки студентов в группе по предмету на последнем занятии
def last_students_marks_in_group(cursor, group_id, subject):
	query = f'''SELECT s.name, m.value, s.group_id, sub.name, m.date_of
				FROM students AS s
				JOIN marks AS m ON s.id = m.student_id
				JOIN subjects AS sub ON sub.id = m.subject_id
				WHERE s.group_id = {group_id} AND sub.name = '{subject}' AND 
					  m.date_of = (SELECT max(m.date_of) AS max_date
								   FROM marks AS m
								   JOIN students AS s ON s.id = m.student_id
								   JOIN subjects AS sub ON sub.id = m.subject_id
								   WHERE s.group_id = {group_id} AND sub.name = '{subject}'
								   );
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Список курсов, которые посещает студент
def subjects_by_student(cursor, student):
	query = f'''SELECT sub.name, s.name
				FROM subjects AS sub
				LEFT JOIN marks AS m ON sub.id = m.subject_id
				LEFT JOIN students AS s ON s.id = m.student_id
				WHERE s.name = '{student}'
				GROUP BY sub.name
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Список курсов, которые студенту читает преподаватель
def subjects_by_prof(cursor, student, prof):
	query = f'''SELECT sub.name, sub.professor, s.name
				FROM subjects AS sub
				LEFT JOIN marks AS m ON sub.id = m.subject_id
				LEFT JOIN students AS s ON s.id = m.student_id
				WHERE s.name = '{student}' AND sub.professor = '{prof}'
				GROUP BY sub.name
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Средний балл, который преподаватель ставит студенту
def avg_mark_by_prof_for_stud(cursor, student, prof):
	query = f'''SELECT ROUND(AVG(m.value), 2) AS avarage_mark, sub.name, sub.professor, s.name AS student
				FROM marks AS m
				LEFT JOIN subjects AS sub ON sub.id = m.subject_id
				LEFT JOIN students AS s ON s.id = m.student_id
				WHERE s.name = '{student}' AND sub.professor = '{prof}'
				GROUP BY sub.name
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


# Средний балл, который ставит преподаватель
def avg_mark_by_prof_for_stud(cursor, prof):
	query = f'''SELECT ROUND(AVG(m.value), 2) AS avarage_mark, sub.name, sub.professor
				FROM marks AS m
				LEFT JOIN subjects AS sub ON sub.id = m.subject_id
				WHERE sub.professor = '{prof}'
				GROUP BY sub.name
			 '''
	cursor.execute(query)

	headers = [cursor.description[i][0] for i in range(len(cursor.description))]
	result = cursor.fetchall()

	return headers, result


if __name__ == '__main__':
	with sqlite3.connect('study.db') as conn:
		cursor = conn.cursor()

		print('5 студентов с наибольшим средним баллом по всем предметам')
		headers, result = best_avg_marks(cursor)

		# print('1 студент с наивысшим средним баллом по одному предмету.')
		# headers, result = max_avg_mark_pro_subj(cursor)

		# print('средний балл в группе по одному предмету.')
		# headers, result = avg_mark_pro_group_and_subj(cursor)

		# print('Средний балл в потоке.')
		# headers, result = avg_mark_pro_group(cursor)

		# print('Какие курсы читает преподаватель.')
		# headers, result = subjs_pro_prof(cursor, 'Dr. David Wagner')

		# print('Список студентов в группе.')
		# headers, result = students_in_group(cursor, randint(1,3))

		# print('Оценки студентов в группе по предмету.')
		# headers, result = students_marks_in_group(cursor, randint(1,3), 'Web development')

		# print('Оценки студентов в группе по предмету на последнем занятии.')
		# headers, result = last_students_marks_in_group(cursor, randint(1,3), 'Web development')

		# print('Список курсов, которые посещает студент.')
		# headers, result = subjects_by_student(cursor, 'Denise Black')

		# print('Список курсов, которые студенту читает преподаватель.')
		# headers, result = subjects_by_prof(cursor, 'Denise Black', 'Dr. David Wagner')

		# print('Средний балл, который преподаватель ставит студенту.')
		# headers, result = avg_mark_by_prof_for_stud(cursor, 'Denise Black', 'Dr. David Wagner')

		# print('Средний балл, который ставит преподаватель.')
		# headers, result = avg_mark_by_prof_for_stud(cursor, 'Dr. David Wagner')


		print(headers)
		print('-' * 100)
		print(result)
