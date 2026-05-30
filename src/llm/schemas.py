# JSON schema for the structured action output.
# Passed to the API as a response schema where supported.

ACTION_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["move", "pick_up", "use_key"]
        },
        "direction": {
            "type": "string",
            "enum": ["north", "south", "east", "west"],
            "description": "Required when action is 'move'."
        },
        "steps": {
            "type": "integer",
            "minimum": 1,
            "description": "Number of steps to move. Optional, defaults to 1."
        },
        "memory_note": {
            "type": "string",
            "description": "Optional note to record in your memory for later."
        }
    },
    "required": ["action"]
}