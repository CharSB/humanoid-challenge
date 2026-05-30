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

def build_observation(world: World, task: Task) -> str:
    surroundings = _describe_surroundings(world)
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

    WHAT YOU CAN SEE (? = not visible):
    {world.render_agent_view()}

    ADJACENT CELLS:
    {surroundings}

    AVAILABLE ACTIONS:
    - move:    {{"action": "move", "direction": "<north|south|east|west>", "steps": <int>}}
    - pick_up: {{"action": "pick_up"}}
    - use_key: {{"action": "use_key"}}

    You may optionally include a "memory_note" field in your JSON to record something for later.
    Example: {{"action": "move", "direction": "east", "steps": 2, "memory_note": "red door at (6,5)"}}

    Rules:
    - Cells marked ? are outside your vision — explore to reveal them.
    - You can only unlock a door you are directly facing from an adjacent cell.
    - Movement is blocked by rocks and locked doors.
    - Tall rocks and locked doors block vision.
    - To pick up a key, move onto its cell then use pick_up.

    Respond with a single JSON object. Nothing else."""