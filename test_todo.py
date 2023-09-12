import pytest
from pytest import raises
from pytest import approx
from sqlite3 import ProgrammingError, IntegrityError
from todo import Todo
from datetime import date
import os

TEST_DB_FILE = r'test_savedNotes.db'

# Note: a new fixture is generated for every test
@pytest.fixture(autouse=False)
def myTodo():
	thing = Todo()
	yield thing
	# teardown
	try:
		os.remove(TEST_DB_FILE)
	except FileNotFoundError:
		pass
	


def test_getNotes_empty(myTodo):
	noteList = myTodo.getNotes()
	assert noteList == []


def test_addNote_single(myTodo):
	text = r"Clean your room"
	priority = 3.3
	completedOn = date.fromisoformat("2024-03-01")
	myTodo.addNote(text, priority, completedOn)
	noteList = myTodo.getNotes()
	note = noteList[0]
	assert note[0] == text and note[1] == approx(priority) and note[2] == completedOn


def test_addNote_multiple(myTodo):	
	# Note: when retrieved, lower priority will be earlier in list
	testData0 = ["Get groceries for the week", 12.1, date.fromisoformat('2023-02-14')]
	testData1 = ["Clean my room", 20, None]
	testData2 = ["135091241351352460989", 1000]
	
	# inserting in non-linear order to test ordering by priority
	myTodo.addNote(*testData1)
	myTodo.addNote(*testData2)
	myTodo.addNote(*testData0)

	# Returned data will contail null values for dates that weren't provided, so let's add that to our test data
	testData2.append(None)

	# Now convert testData to tuples
	testList = [ tuple(testData0), tuple(testData1), tuple(testData2)]	

	noteList = myTodo.getNotes()
	assert testList == noteList


def test_addNote_duplicate(myTodo):
	myTodo.addNote(r'SameExactText', 1)
	with raises(IntegrityError):
		myTodo.addNote(r'SameExactText', 2)


def test_updateNote(myTodo):
	originalText = r"bake cake"
	myTodo.addNote(originalText, 29)
	
	text01 = r"smash cake"
	firstUpdate = [text01, 36, ]
	myTodo.updateNote(originalText, *firstUpdate)
	noteList = myTodo.getNotes()
	
	assert len(noteList) == 1
	
	firstUpdate.append(None) # add completedOn	
	assert noteList[0] == tuple(firstUpdate)


def test_updateNote_duplicate(myTodo):
	sameText = r'SameExactText'
	differentText = r'DifferentText'
	myTodo.addNote(sameText, 1)
	myTodo.addNote(differentText, 2)
	with raises(IntegrityError):
		myTodo.updateNote(differentText, sameText, 3)


def test_updateNote_notExist(myTodo):
	record = [r'Chill', 2301, date.fromisoformat('2025-12-31')]
	myTodo.addNote(*record)
	myTodo.updateNote(r'Work hard', r'Work even harder', 3, None, failOnNotFound=False)

	noteList = myTodo.getNotes()
	assert noteList[0] == tuple(record)

	with raises(RuntimeError):
		myTodo.updateNote(r'Work hard', r'Work even harder', 3, None, failOnNotFound=True)


def test_removeNote(myTodo):
	text = r"eat cake"
	myTodo.addNote(text, 1)
	myTodo.removeNote(text)

	noteList = myTodo.getNotes()
	found = False
	for note in noteList:
		if note[0] == text:
			found=True
	assert found == False


def test_removeNote_notExist(myTodo):
	text = r"eat cake"
	myTodo.removeNote(text, failOnNotFound=False)

	with raises(RuntimeError):
		myTodo.removeNote(text)


def test_clearNotes(myTodo):
	myTodo.addNote(r"eat cake", 100)
	myTodo.addNote(r"drink fried chicken", 200, date.fromisoformat("2018-02-01") )
	myTodo.addNote(r"breathe air", 300, date.fromisoformat("2025-07-30") )
	myTodo.clearNotes()
	noteList = myTodo.getNotes()

	assert len(noteList) == 0


def test_endSession(myTodo):
	myTodo.endSession()
	with raises(ProgrammingError):
		myTodo.addNote(r"This should fail.", 3.3)


def test_saveNotes(myTodo):
	myNote = [r"Write code", 42, date.fromisoformat("2030-01-01")]
	myTodo.addNote(*myNote)
	myTodo.save(TEST_DB_FILE)

	myTodo.clearNotes()
	myTodo.addNote(r"Live laugh love", 31)
	myTodo.load(TEST_DB_FILE)
	myTodo.addNote(r"Live laugh love", 31)

	myTodo.load(TEST_DB_FILE)
	noteList = myTodo.getNotes()
	
	assert len(noteList) == 1
	assert noteList[0] == tuple(myNote)


def test_saveNotes_empty(myTodo):
	myTodo.save(TEST_DB_FILE)
	myTodo.addNote(r"Live laugh love", 31)
	myTodo.load(TEST_DB_FILE)
	noteList = myTodo.getNotes()
	assert noteList == []

