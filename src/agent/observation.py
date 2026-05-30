from src.environment.world import World, DIRECTION_VECTORS
from src.environment.tasks import Task

ALL_DIRECTIONS = ["north", "east", "south", "west"]

def _describe_cell(world: World, x: int, y: int) -> str:
    if not world.grid.in_bounds(x,y):
        return "a wall"
    obj = world.grid.get(x,y)
    if obj is None:
        return "empty"
    return obj.name.replace("_", " ")

def _describe_surroundings(world: World) -> str:
    visible = world.visible_cells()
    lines = []
    for direction in ALL_DIRECTIONS:
        dx, dy = DIRECTION_VECTORS[direction]
        nx,ny = world.agent_x + dx, world.agent_y + dy
        if (nx,ny) in visible:
            description = _describe_cell(world, nx, ny)
        else:
            description = "not visible"
        lines.append(f" {direction}: {description}")
    return "\n".join(lines)

def _door_warning(world: World) -> str:
    """Warn the agent if it is facing a door it cannot unlock."""
    from src.environment.objects import Door, Key
    dx, dy = DIRECTION_VECTORS[world.agent_facing]
    nx, ny = world.agent_x + dx, world.agent_y + dy

    if not world.grid.in_bounds(nx, ny):
        return ""

    target = world.grid.get(nx, ny)
    if not isinstance(target, Door) or not target.locked:
        return ""

    has_key = any(
        isinstance(item, Key) and item.colour == target.colour
        for item in world.inventory
    )

    if not has_key:
        return f"\nWARNING: You are facing a {target.colour} locked door but do not have the {target.colour} key. Do not use_key — find the {target.colour} key first.\n"

    return ""

def _standing_on_notice(world: World) -> str:
    """Notify the agent if it is standing on any object."""
    obj = world.grid.get(world.agent_x, world.agent_y)
    if obj is None:
        return ""
    return f"\nNOTICE: You are standing on {obj.name.replace('_', ' ')}. Use pick_up to collect it.\n"

def build_observation(world: World, task: Task) -> str:
    surroundings = _describe_surroundings(world)
    warning = _door_warning(world)
    standing_notice = _standing_on_notice(world)
    inventory = (
        ", ".join(obj.name.replace("_", " ") for obj in world.inventory)
        if world.inventory else "empty"
    )

    return f"""You are an agent navigating a 2D grid world. You can only see part of the world.

TASK:
{task.description}

YOUR STATE:
- Position: ({world.agent_x}, {world.agent_y})
- Facing: {world.agent_facing}
- Inventory: {inventory}

YOUR MEMORY NOTES:
{world.memory.as_text()}
{standing_notice}{warning}

WHAT YOU CAN SEE (? = not visible):
{world.render_agent_view()}

ADJACENT CELLS:
{surroundings}

AVAILABLE ACTIONS:
- move:    {{"action": "move", "direction": "<north|south|east|west>", "steps": <int>}}
           Use steps > 1 to move multiple cells in one action. e.g. {{"action": "move", "direction": "east", "steps": 4}}
- pick_up: {{"action": "pick_up"}}
- use_key: {{"action": "use_key"}} — only valid if you have the matching key in your inventory

Rules:
- You SHOULD use steps > 1 whenever moving more than one cell in the same direction — do not move one step at a time.
- Cells marked ? are outside your current field of view — explore to reveal them.
- You can only unlock a door you are directly facing from an adjacent cell.
- Movement is blocked by rocks and locked doors.
- Tall rocks and locked doors block vision.
- To pick up a key, move onto its cell then use pick_up.
- Do NOT attempt use_key unless the matching key is in your inventory.

Respond with a single JSON object. Nothing else."""