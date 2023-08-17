import pytest
from pytest import raises
from pytest import approx
from sqlite3 import ProgrammingError
from todo import Todo

# Note: a new fixture is generated for every test
@pytest.fixture(autouse=False)
def myTodo():
	thing = Todo(":memory:")
	return thing


def test_addNote(myTodo):
	text = r"Clean your room"
	priority = 3.3
	dueDate = "2024-03-01"
	myTodo.addNote(text, priority, dueDate)
	noteList = myTodo.getNotes()
	note = noteList[0]
	assert note[1] == text and note[2] == approx(3.3) and note[3] == dueDate


def test_addNote_negative(myTodo):
	with raises(ValueError):
		myTodo.addNote(r'Should fail because value is negative', -5)


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

