import time
from src.environment.world import World
from src.environment.tasks import Task
from src.agent.observation import build_observation
from src.agent.parser import parse_action
from src.agent.actions import MoveAction, PickUpAction, UseKeyAction
from src.simulation.evaluator import check_task_complete

class AgentHarness:
    def __init__(self, world: World, task: Task, client, max_ticks: int = 100):
        self.world = world
        self.task = task
        self.client = client
        self.max_ticks = max_ticks
    
    def run(self) -> bool:
        """
        Run the observe -> think -> act loop.
        Returns True if the task was completed, False if max ticks reached.
        """
        
        print("=== LLM Agent World ===")
        print(f"Task: {self.task.description}")
        print()
        print(self.world)
        
        while self.world.tick < self.max_ticks:
            if check_task_complete(self.world, self.task):
                print(f"\nTask complete in {self.world.tick} ticks.")
                return True

            observation = build_observation(self.world, self.task)
            raw = self.client.complete(observation)

            print(f"\n[Tick {self.world.tick}] LLM response: {raw}")

            try:
                action = parse_action(raw)
            except ValueError as e:
                print(f"Parse error: {e} — skipping turn.")
                continue

            self._execute(action)
            print()
            print(self.world)

        print(f"\nMax ticks ({self.max_ticks}) reached. Task incomplete.")
        return False
    
    def _execute(self, action) -> None:
        match action:
            case MoveAction(direction=d, steps=n):
                for _ in range(n):
                    moved = self.world.move_agent(d)
                    if not moved:
                        print(f"Blocked moving {d}.")
                        break

            case PickUpAction():
                obj = self.world.pick_up()
                if obj:
                    print(f"Picked up: {obj.name}")
                else:
                    print("Nothing to pick up.")

            case UseKeyAction():
                success = self.world.use_key_on_door()
                if success:
                    print("Door unlocked.")
                else:
                    print("Could not unlock door.")
        
        if action.memory_note:
            self.world.memory.add(action.memory_note)
            print(f"Memory noted: {action.memory_note}")