from dataclasses import dataclass

@dataclass
class Tile:
    """
    A single location on the world grid
    """
    
    x: int
    y: int
    object: "WorldObject | None" = None