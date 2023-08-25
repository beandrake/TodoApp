import sqlite3

class Todo():
	"""
	Contains a set of prioritized notes that get saved locally to an sqlite3 database.
	"""
	def __init__(self):
		# Makes our database in memory, as opposed to in a file.
		self.database = sqlite3.connect(":memory:")
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
				completedOn date,
				text varchar(250) NOT NULL UNIQUE
			)		
		""")

	def _flushExceptions(self):
		"""
		do i need this to get exceptions?  pyodbc needed something like this, but it seems like sqlite3 may not.  do more tests!
		"""
		#return
		self.cursor.fetchall()

# close database connection
	def endSession(self):
		"""
		Closes the connection to the database, allowing memory to be freed and making this object unusable.
		"""
		#self.cursor.close()
		self.database.close()

# clear notes
	def clearNotes(self):
		"""
		Removes all records from the database.
		"""
		# sqlite doesn't have truncate; this is the advised alternative
		self.cursor.execute(r"DROP TABLE notes")
		self._createTable()

# see my existing notes
	def getNotes(self):
		"""
		Returns a list of tuples containing (text, priority, completedOn)
		"""
		self.cursor.execute(r"SELECT text, priority, completedOn FROM notes ORDER BY priority ASC, completedOn DESC, text ASC")
		noteList = []
		for note in self.cursor:
			noteList.append(note)
		
		self._flushExceptions()
		return noteList

# add new note
	def addNote(self, text, priority, completedOn=None):
		"""
		Add a new note to the Todo.  Lower values for priority are considered more important.
		"""
		if priority < 1:
			raise ValueError(r"Priority must have a non-negative value.")
		
		insertQuery = r"INSERT INTO notes(text, priority, completedOn) VALUES(?, ?, ?)"
		values = [text, priority, completedOn]
		self.cursor.execute(insertQuery, values)
		self.database.commit()
		
		self._flushExceptions()


# remove note
	

# update note
	

# save note


# load note






if __name__ == '__main__':
	myTodo = Todo()