from dataclasses import dataclass, field

@dataclass
class WorldObject:
    name: str
    
    @property
    def symbol(self) -> str:
        return "?"
    
    @property
    def blocks_movement(self) -> bool:
        return False

    @property
    def blocks_vision(self) -> bool:
        return False

class ShortRock(WorldObject):
    
    def __init__(self):
        super().__init__("short_rock")
    
    @property
    def symbol(self) -> str:
        return "r"
    
    @property
    def blocks_movement(self) -> bool:
        return True
    
class TallRock(WorldObject):
    
    def __init__(self):
        super().__init__("tall_rock")
    
    @property
    def symbol(self) -> str:
        return "R"
    
    @property
    def blocks_movement(self) -> bool:
        return True
    
    @property
    def blocks_vision(self) -> bool:
        return True

class Key(WorldObject):
    def __init__(self, colour: str):
        super().__init__(f"key_{colour}")
        self.colour = colour
        
    @property
    def symbol(self) -> str:
        return "k"

class Door(WorldObject):
    def __init__(self, colour: str):
        super().__init__(f"door_{colour}")
        self.colour = colour
        self.locked = True
    
    @property
    def symbol(self) -> str:
        return "D" if self.locked else "d"
    
    @property
    def blocks_movement(self) -> bool:
        return self.locked
    
    @property
    def blocks_vision(self) -> bool:
        return self.locked
    
    def unlock(self, key: Key) -> bool:
        """ Try to unlock door with key. Return True if successful. """
        if key.colour == self.colour:
            self.locked = False
            return True
        return False
    


