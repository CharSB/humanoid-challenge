import pytest
from src.environment.tasks import (
    task_from_yaml, ReachGoal, CollectKey, OpenDoor, CollectAndOpen
)
from src.environment.objects import Key, Door
from src.simulation.evaluator import check_task_complete


class TestTaskFromYaml:
    def test_reach_goal(self):
        task = task_from_yaml({"type": "reach_goal", "x": 4, "y": 4})
        assert isinstance(task, ReachGoal)
        assert task.x == 4
        assert task.y == 4

    def test_collect_key(self):
        task = task_from_yaml({"type": "collect_key", "colour": "red"})
        assert isinstance(task, CollectKey)
        assert task.colour == "red"

    def test_open_door(self):
        task = task_from_yaml({"type": "open_door", "colour": "red"})
        assert isinstance(task, OpenDoor)
        assert task.colour == "red"

    def test_collect_and_open(self):
        task = task_from_yaml({"type": "collect_and_open", "colour": "red"})
        assert isinstance(task, CollectAndOpen)
        assert task.colour == "red"

    def test_unknown_task_type(self):
        with pytest.raises(ValueError, match="Unknown task type"):
            task_from_yaml({"type": "unknown"})

    def test_description_auto_generated(self):
        task = task_from_yaml({"type": "reach_goal", "x": 2, "y": 3})
        assert "(2, 3)" in task.description


class TestEvaluator:
    def test_reach_goal_success(self, world):
        task = ReachGoal(x=0, y=0)
        assert check_task_complete(world, task)

    def test_reach_goal_failure(self, world):
        task = ReachGoal(x=4, y=4)
        assert not check_task_complete(world, task)

    def test_collect_key_success(self, world):
        task = CollectKey(colour="red")
        world.inventory.append(Key("red"))
        assert check_task_complete(world, task)

    def test_collect_key_failure(self, world):
        task = CollectKey(colour="red")
        assert not check_task_complete(world, task)

    def test_collect_key_wrong_colour(self, world):
        task = CollectKey(colour="red")
        world.inventory.append(Key("blue"))
        assert not check_task_complete(world, task)

    def test_open_door_success(self, world):
        task = OpenDoor(colour="red")
        door = world.grid.get(0, 2)
        assert isinstance(door, Door)
        door.locked = False
        assert check_task_complete(world, task)

    def test_open_door_failure(self, world):
        task = OpenDoor(colour="red")
        assert not check_task_complete(world, task)

    def test_collect_and_open_success(self, world):
        task = CollectAndOpen(colour="red")
        door = world.grid.get(0, 2)
        assert isinstance(door, Door)
        door.locked = False
        assert check_task_complete(world, task)

    def test_collect_and_open_failure(self, world):
        task = CollectAndOpen(colour="red")
        assert not check_task_complete(world, task)