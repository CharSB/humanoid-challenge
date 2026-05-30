from src.environment.world import World
from src.environment.tasks import Task, ReachGoal, CollectKey, OpenDoor, CollectAndOpen
from src.environment.objects import Key, Door

def check_task_complete(world: World, task: Task) -> bool:
    match task: 
        case ReachGoal(x=x, y=y):
            return world.agent_x == x and world.agent_y == y

        case CollectKey(colour=colour):
            return any(
                isinstance(item, Key) and item.colour == colour
                for item in world.inventory
            )

        case OpenDoor(colour=colour):
            # Check every cell for an unlocked door of this colour
            for y in range(world.grid.height):
                for x in range(world.grid.width):
                    obj = world.grid.get(x, y)
                    if isinstance(obj, Door) and obj.colour == colour and not obj.locked:
                        return True
            return False

        case CollectAndOpen(colour=colour):
            door_open = False
            for y in range(world.grid.height):
                for x in range(world.grid.width):
                    obj = world.grid.get(x, y)
                    if isinstance(obj, Door) and obj.colour == colour and not obj.locked:
                        door_open = True
                        break
            return door_open

        case _:
            raise ValueError(f"Unknown task type: {type(task)}")