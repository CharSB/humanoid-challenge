import pytest
from src.environment.world import World
from src.environment.objects import Key, Door, ShortRock, TallRock


class TestMovement:
    def test_move_success(self, world: World):
        moved = world.move_agent("south")
        assert moved
        assert world.agent_y == 1

    def test_move_updates_facing(self, world: World):
        world.move_agent("east")
        assert world.agent_facing == "east"

    def test_facing_updates_even_when_blocked(self, world: World):
        # short rock is at (1, 0) — moving east is blocked
        world.move_agent("east")
        assert world.agent_facing == "east"
        assert world.agent_x == 0

    def test_move_blocked_by_short_rock(self, world: World):
        # short rock at (1, 0), agent starts at (0, 0)
        moved = world.move_agent("east")
        assert not moved
        assert world.agent_x == 0

    def test_move_blocked_by_tall_rock(self, world: World):
        # tall rock at (2, 0) — place agent adjacent
        world.agent_x = 1
        moved = world.move_agent("east")
        assert not moved
        assert world.agent_x == 1

    def test_move_blocked_by_locked_door(self, world: World):
        # locked red door at (0, 2), agent at (0, 0)
        world.move_agent("south")  # (0,1)
        moved = world.move_agent("south")  # (0,2) blocked
        assert not moved
        assert world.agent_y == 1

    def test_move_out_of_bounds(self, world: World):
        moved = world.move_agent("north")
        assert not moved
        assert world.agent_y == 0

    def test_move_increments_tick(self, world: World):
        world.move_agent("south")
        assert world.tick == 1

    def test_blocked_move_does_not_increment_tick(self, world: World):
        world.move_agent("north")
        assert world.tick == 0

    def test_multi_step_move(self, world: World):
        world.agent_x = 1
        world.agent_y = 2
        for _ in range(3):
            world.move_agent("east")
        assert world.agent_x == 4
        assert world.agent_y == 2

    def test_multi_step_stops_at_blocker(self, world: World):
        # door at (0,2) — moving south twice from (0,0) should stop at (0,1)
        world.move_agent("south")
        moved = world.move_agent("south")
        assert not moved
        assert world.agent_y == 1


class TestPickUp:
    def test_pick_up_key(self, world: World):
        # red key at (0,1)
        world.move_agent("south")
        obj = world.pick_up()
        assert obj is not None
        assert obj.name == "key_red"

    def test_pick_up_adds_to_inventory(self, world: World):
        world.move_agent("south")
        world.pick_up()
        assert len(world.inventory) == 1

    def test_pick_up_removes_from_grid(self, world: World):
        world.move_agent("south")
        world.pick_up()
        assert world.grid.get(0, 1) is None

    def test_pick_up_empty_cell(self, world: World):
        obj = world.pick_up()
        assert obj is None
        assert len(world.inventory) == 0

    def test_pick_up_increments_tick(self, world: World):
        world.move_agent("south")
        world.pick_up()
        assert world.tick == 2


class TestUnlock:
    def _collect_key_and_face_door(self, world: World):
        """Move to key, pick it up, face the door."""
        world.move_agent("south")   # (0,1) — on key
        world.pick_up()
        world.agent_facing = "south"  # face door at (0,2)

    def test_unlock_success(self, world: World):
        self._collect_key_and_face_door(world)
        success = world.unlock()
        assert success

    def test_unlock_removes_key_from_inventory(self, world: World):
        self._collect_key_and_face_door(world)
        world.unlock()
        assert len(world.inventory) == 0

    def test_unlock_door_is_unlocked(self, world: World):
        self._collect_key_and_face_door(world)
        world.unlock()
        door = world.grid.get(0, 2)
        assert isinstance(door, Door)
        assert not door.locked

    def test_unlock_wrong_key(self, world: World):
        world.inventory.append(Key("blue"))
        world.agent_y = 1
        world.agent_facing = "south"
        success = world.unlock()
        assert not success

    def test_unlock_no_key(self, world: World):
        world.agent_y = 1
        world.agent_facing = "south"
        success = world.unlock()
        assert not success

    def test_unlock_not_facing_door(self, world: World):
        world.move_agent("south")
        world.pick_up()
        world.agent_facing = "east"
        success = world.unlock()
        assert not success

    def test_unlock_increments_tick(self, world: World):
        self._collect_key_and_face_door(world)
        tick_before = world.tick
        world.unlock()
        assert world.tick == tick_before + 1

    def test_unlocked_door_is_passable(self, world: World):
        self._collect_key_and_face_door(world)
        world.unlock()
        moved = world.move_agent("south")
        assert moved
        assert world.agent_y == 2