from sqlite3 import connect

def create_db():

	with open('study.sql', 'r') as file:
		sql = file.read()

	with connect('study.db') as connection:
		cursor = connection.cursor()

		cursor.executescript(sql)


if __name__ == '__main__':
	create_db()

