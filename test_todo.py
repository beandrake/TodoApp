import pytest
from pytest import raises
from pytest import approx
from sqlite3 import ProgrammingError, IntegrityError
from todo import Todo

# Note: a new fixture is generated for every test
@pytest.fixture(autouse=False)
def myTodo():
	thing = Todo()
	return thing

def test_getNotes_empty(myTodo):
	noteList = myTodo.getNotes()
	assert noteList == []

def test_addNote_single(myTodo):
	text = r"Clean your room"
	priority = 3.3
	completedOn = "2024-03-01"
	myTodo.addNote(text, priority, completedOn)
	noteList = myTodo.getNotes()
	note = noteList[0]
	assert note[0] == text and note[1] == approx(priority) and note[2] == completedOn

def test_addNote_multiple(myTodo):	
	# Note: when retrieved, lower priority will be earlier in list
	testData0 = ["Get groceries for the week", 12.1, "2023-02-14"]
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

def test_addNote_below_1(myTodo):
	with raises(ValueError):
		myTodo.addNote(r'Should fail because value is negative', 0.999)

def test_addNote_negative(myTodo):
	with raises(ValueError):
		myTodo.addNote(r'Should fail because value is negative', -5)

def test_addNote_wrongDataTypes(myTodo):
	with raises(ValueError):
		myTodo.addNote(r'abc', 'xyz')
	with raises(ValueError):
		myTodo.addNote(123, 123)
	with raises(ValueError):
		myTodo.addNote(r'Task', 21, 'Steven')


def test_clearNotes(myTodo):
	myTodo.addNote(r"eat cake", 100)
	myTodo.addNote(r"drink fried chicken", 200, "2018-02-01")
	myTodo.addNote(r"breathe air", 300, "2025-07-30")
	myTodo.clearNotes()
	noteList = myTodo.getNotes()

	assert len(noteList) == 0


def test_endSession(myTodo):
	myTodo.endSession()
	with raises(ProgrammingError):
		myTodo.addNote(r"This should fail.", 3.3)

