import time
import signal
import sys

from src.environment.world import World
from src.environment.tasks import Task

from src.agent.observation import build_observation
from src.agent.parser import parse_action
from src.agent.actions import MoveAction, PickUpAction, UseKeyAction

from src.simulation.evaluator import check_task_complete

from src.utils.logging import EpisodeLogger


class AgentHarness:
    def __init__(self, world: World, task: Task, client, max_ticks: int = 100):
        self.world = world
        self.task = task
        self.client = client
        self.max_ticks = max_ticks
        self.logger = EpisodeLogger(task_name=type(task).__name__.lower())
    
    """
        Run the observe -> think -> act loop.
        Returns True if the task was completed, False if max ticks reached.
    """
    def run(self) -> bool:
        print("=== LLM Agent World ===")
        print(f"Task: {self.task.description}")
        print()
        print(self.world)

        success = False

        try:
            while self.world.tick < self.max_ticks:
                if check_task_complete(self.world, self.task):
                    print(f"\nTask complete in {self.world.tick} ticks.")
                    success = True
                    break

                observation = build_observation(self.world, self.task)
                raw = self.client.complete(observation)

                print(f"\n[Tick {self.world.tick}] LLM response: {raw}")

                try:
                    action = parse_action(raw)
                except ValueError as e:
                    result = f"parse_error: {e}"
                    print(f"Parse error: {e} — skipping turn.")
                    self.logger.log_tick(self.world, observation, raw, "invalid", result)
                    continue

                result = self._execute(action)
                print()
                print(self.world)

                self.logger.log_tick(
                    world=self.world,
                    observation=observation,
                    raw_response=raw,
                    parsed_action=str(action),
                    action_result=result,
                )

            if not success:
                print(f"\nMax ticks ({self.max_ticks}) reached. Task incomplete.")

        except KeyboardInterrupt:
            print("\n\nInterrupted.")
            success = False

        finally:
            self.logger.finish(success=success, total_ticks=self.world.tick)
            log_path = self.logger.save()
            print(f"Episode log saved to: {log_path}")

        return success
    
    def _execute(self, action) -> str:
        match action:
            case MoveAction(direction=d, steps=n):
                blocked = False
                for _ in range(n):
                    moved = self.world.move_agent(d)
                    if not moved:
                        blocked = True
                        break
                result = f"moved {d}" + (f" (blocked after {_ } steps)" if blocked else f" x{n}")


            case PickUpAction():
                obj = self.world.pick_up()
                result = f"picked_up {obj.name}" if obj else "pick_up failed: nothing here"
                print(result)


            case UseKeyAction():
                success = self.world.unlock()
                result = "door unlocked" if success else "use_key failed: no unlockable door faced"
                print(result)
        
        if action.memory_note:
            self.world.memory.add(action.memory_note)
            print(f"Memory noted: {action.memory_note}")
            
        return result