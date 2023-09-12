import sqlite3
import datetime

class Todo():
	"""
	Contains a set of prioritized notes that get saved locally to an sqlite3 database.
	"""

	# Without PARSE_DECLTYPES, a datetime.date that is inserted into the sqlite database will be retrieved as a different datatype.
	DETECT_TYPES=sqlite3.PARSE_DECLTYPES
	

	def __init__(self):
		# Makes our database in memory, as opposed to in a file.
		databaseLocation = ":memory:"
		
		self.database = sqlite3.connect(databaseLocation, detect_types=Todo.DETECT_TYPES)
		self.cursor = self.database.cursor()

		# if our table doesn't already exist, make it
		self.cursor.execute(r"SELECT name FROM sqlite_schema WHERE type='table' AND name='notes'")
		listOfTablesNamedNotes = self.cursor.fetchall()
		if len(listOfTablesNamedNotes) == 0:
			self._createTable()


	def _createTable(self):
		# NOTE: sqlite3 doesn't do any checks to verify that the value being inserted into a column is of the appropriate SQL datatype: https://www.sqlite.org/datatype3.html
		self.cursor.execute(r"""	
			CREATE TABLE notes(
				id INTEGER PRIMARY KEY,
				priority FLOAT NOT NULL,
				completedOn date,
				text varchar(250) NOT NULL UNIQUE
			)		
		""")


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
		
		return noteList

# add new note
	def addNote(self, text:str, priority:float, completedOn:datetime.date=None):
		"""
		Add a new note to the Todo.  Lower values for priority are considered more important.
		"""
		insertQuery = r"INSERT INTO notes(text, priority, completedOn) VALUES(?, ?, ?)"
		values = [text, priority, completedOn]
		self.cursor.execute(insertQuery, values)
		self.database.commit()


# remove note
	def removeNote(self, text:str, failOnNotFound=True):
		"""
		Remove an existing note.
		"""
		removeQuery = r"DELETE FROM notes WHERE text = ?"
		values = [text]
		self.cursor.execute(removeQuery, values)
		self.database.commit()
		
		# check to see if a record was actually deleted
		if failOnNotFound:
			if self.cursor.rowcount < 1:
				raise RuntimeError


# update note
	def updateNote(self, oldText:str, newText:str, newPriority:float, newCompletedOn:datetime.date=None, failOnNotFound=True):		
		"""
		Update an existing note.
		"""
		updateQuery = r"UPDATE notes SET text=?, priority=?, completedOn=? WHERE text=?"
		values = [newText, newPriority, newCompletedOn, oldText]
		self.cursor.execute(updateQuery, values)
		self.database.commit()

		# check to see if a record was actually updated
		if failOnNotFound:
			if self.cursor.rowcount < 1:
				raise RuntimeError


# save note
	def save(self, filename):		
		"""
		Saves your notes as a file.
		"""
		savedDatabase = sqlite3.connect(filename, detect_types=Todo.DETECT_TYPES)
		
		# this copies our database from memory into the newly-created database file
		with savedDatabase: 
			self.database.backup(savedDatabase, pages=1)
		savedDatabase.close()


# load note
	def load(self, filename):
		"""
		Loads your notes from a file.
		"""
		loadedDatabase = sqlite3.connect(filename, detect_types=Todo.DETECT_TYPES)
		
		# this copies our database from a file into our in-memory database
		loadedDatabase.backup(self.database, pages=1)
		loadedDatabase.close()

		#self.cursor = self.database.cursor()
		





if __name__ == '__main__':
	myTodo = Todo()