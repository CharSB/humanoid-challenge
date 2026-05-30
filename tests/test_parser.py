import pytest
from src.agent.parser import parse_action
from src.agent.actions import MoveAction, PickUpAction, UseKeyAction


class TestMoveAction:
    def test_basic_move(self):
        action = parse_action('{"action": "move", "direction": "north", "steps": 1}')
        assert isinstance(action, MoveAction)
        assert action.direction == "north"
        assert action.steps == 1

    def test_multi_step_move(self):
        action = parse_action('{"action": "move", "direction": "east", "steps": 4}')
        assert isinstance(action, MoveAction)
        assert action.steps == 4

    def test_move_defaults_steps_to_one(self):
        action = parse_action('{"action": "move", "direction": "south"}')
        assert isinstance(action, MoveAction)
        assert action.steps == 1

    def test_all_valid_directions(self):
        for direction in ["north", "south", "east", "west"]:
            action = parse_action(f'{{"action": "move", "direction": "{direction}"}}')
            assert isinstance(action, MoveAction)
            assert action.direction == direction

    def test_invalid_direction(self):
        with pytest.raises(ValueError, match="Invalid direction"):
            parse_action('{"action": "move", "direction": "up"}')

    def test_steps_less_than_one(self):
        with pytest.raises(ValueError, match="Steps must be at least 1"):
            parse_action('{"action": "move", "direction": "north", "steps": 0}')


class TestPickUpAction:
    def test_pick_up(self):
        action = parse_action('{"action": "pick_up"}')
        assert isinstance(action, PickUpAction)


class TestUseKeyAction:
    def test_use_key(self):
        action = parse_action('{"action": "use_key"}')
        assert isinstance(action, UseKeyAction)


class TestMemoryNote:
    def test_memory_note_on_move(self):
        action = parse_action('{"action": "move", "direction": "north", "memory_note": "key at (2,3)"}')
        assert action.memory_note == "key at (2,3)"

    def test_memory_note_on_pick_up(self):
        action = parse_action('{"action": "pick_up", "memory_note": "collected red key"}')
        assert action.memory_note == "collected red key"

    def test_missing_memory_note_defaults_to_empty(self):
        action = parse_action('{"action": "pick_up"}')
        assert action.memory_note == ""


class TestInvalidInput:
    def test_invalid_json(self):
        with pytest.raises(ValueError, match="not valid JSON"):
            parse_action("not json at all")

    def test_unknown_action_type(self):
        with pytest.raises(ValueError, match="Unknown action type"):
            parse_action('{"action": "fly"}')

    def test_empty_json_object(self):
        with pytest.raises(ValueError, match="Unknown action type"):
            parse_action('{}')