import sys
from pathlib import Path

import yaml

from src.environment.world import World
from src.environment.tasks import task_from_yaml

from src.simulation.runner import run_episode

CONFIG_PATH = Path("configs/world.yaml")

def main():
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)
        
    world = World.from_yaml(CONFIG_PATH)
    task = task_from_yaml(cfg["task"])
    
    print("=== LLM Agent World ===")
    print(f"Task: {task.description}")
    print()
    print(world)

    MOVE_KEYS = {
        "w": "north",
        "s": "south",
        "a": "west",
        "d": "east",
    }
    
    while True:
            print()
            cmd = input("Move (wasd) | (p)ick up | (u)se key on door | (q)uit: ").strip().lower()

            if cmd == "q":
                print("Exiting.")
                sys.exit(0)

            elif cmd in MOVE_KEYS:
                direction = MOVE_KEYS[cmd]
                moved = world.move_agent(direction)
                if not moved:
                    print(f"Blocked - now facing {direction}.")

            elif cmd == "p":
                obj = world.pick_up()
                if obj:
                    print(f"Picked up: {obj.name}")
                else:
                    print("Nothing to pick up here.")

            elif cmd.startswith("u"):
                success = world.unlock()
                if success: 
                    print("Door unlocked.")
                else:
                    print("No unlockable door in that direction.")

            else:
                print("Unknown command.")
                continue

            print()
            print(world)


if __name__ == "__main__":
    run_episode()