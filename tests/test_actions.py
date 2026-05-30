import pytest
from src.agent.actions import MoveAction, PickUpAction, UseKeyAction


class TestMoveAction:
    def test_default_steps(self):
        action = MoveAction(direction="north")
        assert action.steps == 1

    def test_default_memory_note(self):
        action = MoveAction(direction="north")
        assert action.memory_note == ""

    def test_custom_steps(self):
        action = MoveAction(direction="east", steps=3)
        assert action.steps == 3

    def test_with_memory_note(self):
        action = MoveAction(direction="south", memory_note="explored south corridor")
        assert action.memory_note == "explored south corridor"


class TestPickUpAction:
    def test_default_memory_note(self):
        action = PickUpAction()
        assert action.memory_note == ""

    def test_with_memory_note(self):
        action = PickUpAction(memory_note="picked up red key")
        assert action.memory_note == "picked up red key"


class TestUseKeyAction:
    def test_default_memory_note(self):
        action = UseKeyAction()
        assert action.memory_note == ""

    def test_with_memory_note(self):
        action = UseKeyAction(memory_note="unlocked red door")
        assert action.memory_note == "unlocked red door"