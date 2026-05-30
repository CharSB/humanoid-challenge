from dataclasses import dataclass

@dataclass
class MoveAction:
    direction: str
    steps: int = 1
    memory_note: str = ""
    
@dataclass
class PickUpAction:
    memory_note: str = ""
    
@dataclass
class UseKeyAction:
    memory_note: str = ""


Action = MoveAction | PickUpAction | UseKeyAction