import sqlite3

class Todo():
	"""
	Contains a set of prioritized notes that get saved locally to an sqlite3 database.
	"""
	def __init__(self, filename=":memory:"):
		self.database = sqlite3.connect(filename)
		self.cursor = self.database.cursor()

		# if our table doesn't already exist, make it
		self.cursor.execute(r"SELECT name FROM sqlite_schema WHERE type='table' AND name='notes'")
		listOfTablesNamedNotes = self.cursor.fetchall()

		if len(listOfTablesNamedNotes) == 0:
			self._createTable()
	
	def _createTable(self):
		self.cursor.execute(r"""	
			CREATE TABLE notes(
				id INTEGER PRIMARY KEY,
				priority FLOAT NOT NULL,
				dueDate date,
				text varchar(250) NOT NULL UNIQUE
			)		
		""")

# close database connection
	def endSession(self):
		#self.cursor.close()
		self.database.close()

# clear notes
	def clearNotes(self):
		# sqlite doesn't have truncate; this is the advised alternative
		self.cursor.execute(r"DROP TABLE notes")
		self._createTable()

# see my existing notes
	def getNotes(self):
		"""
		Returns a list of tuples containing [id, text, priority, dueDate]
		"""
		self.cursor.execute(r"SELECT id, text, priority, dueDate FROM notes ORDER BY priority ASC, dueDate DESC, text ASC")
		noteList = []
		for note in self.cursor:
			noteList.append(note)
		return noteList

# add new note
	def addNote(self, text, priority, dueDate=None):
		if priority < 0:
			raise ValueError(r"Priority must have a non-negative value.")
		
		insertQuery = r"INSERT INTO notes(text, priority, dueDate) VALUES(?, ?, ?)"
		values = [text, priority, dueDate]
		self.cursor.execute(insertQuery, values)
		self.database.commit()
		return self.cursor.fetchall()


# remove note
	

# update note









if __name__ == '__main__':
	pass







######################################################

def testDatabaseFunctionality():
	# connect to DB (makes it if it doesn't exist)
	tempConnection = sqlite3.connect("temp.db")
	
	# execute a query that returns a list of all tables named BestDataEver
	tempCursor = tempConnection.cursor()
	output = tempCursor.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name='BestDataEver'")

	# Here's something a bit weird; the execute method returns an alias of the cursor that calls it.
	if tempCursor is output:
		print(r"Oh, it looks like cursor.execute() returns cursor...?")

	#

class easySQL:
	"""
	A wrapper for an sqlite3 connection/cursor that automates the extraction of results after queries.
	"""
	def __init__(self, databaseFilename):
		self.connection = sqlite3.connect(databaseFilename)
		self.cursor = self.connection.cursor()

	def query(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def commit(self):
		return self.connection.commit()


def fakeStuff():
	database = easySQL("mystery.db")
	
	# query checks if a table exists
	output = database.query("SELECT name FROM sqlite_schema WHERE type='table' AND name='notes'")
	print(output)

	if len(output) == 0:
		database.query("""	
			CREATE TABLE notes(
				id INTEGER PRIMARY KEY,
				importance FLOAT NOT NULL,
				note varchar(250) NOT NULL UNIQUE
			)		
		""")

		output = database.query("SELECT name FROM sqlite_schema WHERE type='table' AND name='notes'")
		print(output)
		
		database.query("INSERT INTO notes(importance, note) VALUES(3.5, 'eat a sandwich')")
		database.query("INSERT INTO notes(importance, note) VALUES(86, 'do a stretch')")
		database.connection.commit()

	output = database.query("SELECT * FROM notes")
	print(output)





	
