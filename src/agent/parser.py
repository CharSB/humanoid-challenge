import json
from src.agent.actions import Action, MoveAction, PickUpAction, UseKeyAction

VALID_DIRECTIONS = {"north", "east", "south", "west"}

def parse_action(raw: str) -> Action:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM output is not valid JSON: {e}\nRaw: {raw}")
    
    note = data.get("memory_note", "")
    action_type = data.get("action")
    
    match action_type:
        case "move":
            direction = data.get("direction", "").lower()
            if direction not in VALID_DIRECTIONS:
                raise ValueError(f"Invalid direction: '{direction}'")
            steps = int(data.get("steps", 1))
            if steps < 1:
                raise ValueError(f"Steps must be at least 1, got {steps}")
            return MoveAction(direction=direction, steps=steps, memory_note=note)

        case "pick_up":
            return PickUpAction(memory_note=note)

        case "use_key":
            return UseKeyAction(memory_note=note)

        case _:
            raise ValueError(f"Unknown action type: '{action_type}'")