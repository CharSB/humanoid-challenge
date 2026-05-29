import yaml
from pathlib import Path

from src.environment.grid import Grid
from src.environment.objects import WorldObject, ShortRock, TallRock, Key, Door

OBJECTS: dict[str, callable] = {
    "short_rock": lambda cfg: ShortRock(),
    "tall_rock":  lambda cfg: TallRock(),
    "key":        lambda cfg: Key(cfg["colour"]),
    "door":       lambda cfg: Door(cfg["colour"]),
}

DIRECTION_VECTORS: dict[str, tuple[int, int]] = {
    "north": (0, -1),
    "south": (0,  1),
    "east":  (1,  0),
    "west":  (-1, 0),
}

DIRECTION_SYMBOLS: dict[str, str] = {
    "north": "^",
    "south": "v",
    "east":  ">",
    "west":  "<",
}

class World:
    def __init__(self, grid: Grid, agent_x: int, agent_y: int, agent_facing: str = "north"):
        self.grid = grid
        self.agent_x = agent_x
        self.agent_y = agent_y
        self.agent_facing = agent_facing
        self.tick = 0
        self.inventory: list[WorldObject] = []
        
    @classmethod
    def from_yaml(cls, path: str | Path) -> "World":
        with open(path) as f:
            cfg = yaml.safe_load(f)

        grid = Grid(cfg["grid"]["width"], cfg["grid"]["height"])

        for obj_cfg in cfg.get("objects", []):
            obj_type = obj_cfg["type"]
            if obj_type not in OBJECTS:
                raise ValueError(f"Unknown object type: '{obj_type}'")
            obj = OBJECTS[obj_type](obj_cfg)
            grid.place(obj, obj_cfg["x"], obj_cfg["y"])

        agent_x = cfg["agent"]["start_x"]
        agent_y = cfg["agent"]["start_y"]
        agent_facing = cfg["agent"].get("start_facing", "north")

        return cls(grid, agent_x, agent_y, agent_facing)
    
    def move_agent(self, direction: str) -> bool:
        
        self.agent_facing = direction
        dx, dy = DIRECTION_VECTORS[direction]
        new_x = self.agent_x + dx
        new_y = self.agent_y + dy

        if not self.grid.in_bounds(new_x, new_y):
            return False

        occupant = self.grid.get(new_x, new_y)
        if occupant is not None and occupant.blocks_movement:
            return False

        self.agent_x = new_x
        self.agent_y = new_y
        self.tick += 1
        return True
    
    def pick_up(self) -> WorldObject | None:

        obj = self.grid.get(self.agent_x, self.agent_y)
        if obj is None:
            return None
        self.grid.remove(self.agent_x, self.agent_y)
        self.inventory.append(obj)
        self.tick += 1
        return obj
    
    def unlock(self) -> bool:
        dx, dy = DIRECTION_VECTORS[self.agent_facing]
        door_x = self.agent_x + dx
        door_y = self.agent_y + dy

        if not self.grid.in_bounds(door_x, door_y):
            return False

        target = self.grid.get(door_x, door_y)
        if not isinstance(target, Door):
            return False

        for item in self.inventory:
            if isinstance(item, Key) and item.colour == target.colour:
                if target.unlock(item):
                    self.inventory.remove(item)
                    self.tick += 1
                    return True

        return False

    
    def render(self) -> str:
        agent_symbol = DIRECTION_SYMBOLS[self.agent_facing]
        return self.grid.render(agent_symbol, self.agent_x, self.agent_y)
    
    def __str__(self) -> str:
        lines = [
            f"Tick: {self.tick}",
            f"Agent: ({self.agent_x}, {self.agent_y})",
            f"Inventory: {[obj.name for obj in self.inventory]}",
            "",
            self.render(),
        ]
        return "\n".join(lines)