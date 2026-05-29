from dataclasses import dataclass

@dataclass
class WorldObject:
    name: str
    symbol: str
    
    @property
    def blocks_movement(self) -> bool:
        return False

    @property
    def blocks_vision(self) -> bool:
        return False

class ShortRock(WorldObject):
    
    def __init__(self):
        super().__init__("short_rock", "r")
    
    @property
    def blocks_movement(self):
        return True
    
class TallRock(WorldObject):
    
    def __init__(self):
        super().__init__("tall_rock", "R")
    
    @property
    def blocks_movement(self):
        return True
    
    @property
    def blocks_vision(self):
        return True

class Key(WorldObject):
    def __init__(self, key_id: str):
        super().__init__(f"key_{key_id}", "k")
        self.key_id = key_id

class Door(WorldObject):
    def __init__(self, key_id: str):
        super().__init__(f"door_{key_id}", "D")
        self.key_id = key_id
        self.locked = True
        
        @property
        def blocks_movement(self):
            return self.locked


