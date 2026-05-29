from dataclasses import dataclass

@dataclass
class ReachGoal:
    """ Agent must reach a sepciifc cell """
    x: int
    y: int
    description: str = ""
    
    def __post_init__(self):
        if not self.description:
            self.description = f"Reach position ({self.x}, {self.y})."
    
@dataclass
class CollectKey:
    """Agent must pick up a key of a specific colour."""
    colour: str
    description: str = ""

    def __post_init__(self):
        if not self.description:
            self.description = f"Collect the {self.colour} key."

@dataclass
class OpenDoor:
    """Agent must unlock a door of a specific colour."""
    colour: str
    description: str = ""

    def __post_init__(self):
        if not self.description:
            self.description = f"Open the {self.colour} door."


@dataclass
class CollectAndOpen:
    """Agent must collect a key and use it to open the matching door."""
    colour: str
    description: str = ""

    def __post_init__(self):
        if not self.description:
            self.description = f"Collect the {self.colour} key and open the {self.colour} door."


Task = ReachGoal | CollectKey | OpenDoor | CollectAndOpen


def task_from_yaml(cfg: dict) -> Task:
    task_type = cfg["type"]
    match task_type:
        case "reach_goal":
            return ReachGoal(x=cfg["x"], y=cfg["y"])
        case "collect_key":
            return CollectKey(colour=cfg["colour"])
        case "open_door":
            return OpenDoor(colour=cfg["colour"])
        case "collect_and_open":
            return CollectAndOpen(colour=cfg["colour"])
        case _:
            raise ValueError(f"Unknown task type: '{task_type}'")