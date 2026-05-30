from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

from src.environment.world import World
from src.environment.tasks import Task

LOGS_DIR = Path("logs/episodes/")

@dataclass
class TickLog:
    tick: int
    observation: str
    raw_response: str
    parsed_action: str
    agent_position: tuple[int, int]
    agent_facing: str
    inventory: list[str]
    memory_notes: list[str]
    action_result: str
    
@dataclass
class EpisodeLogger:
    task_name: str
    started_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    ticks: list[TickLog] = field(default_factory=list)
    outcome: str = "incomplete"
    total_ticks: int = 0

    def log_tick(
        self,
        world: World,
        observation: str,
        raw_response: str,
        parsed_action: str,
        action_result: str,
    ) -> None:
        self.ticks.append(TickLog(
            tick=world.tick,
            observation=observation,
            raw_response=raw_response,
            parsed_action=parsed_action,
            agent_position=(world.agent_x, world.agent_y),
            agent_facing=world.agent_facing,
            inventory=[obj.name for obj in world.inventory],
            memory_notes=list(world.memory.notes),
            action_result=action_result,
        ))

    def finish(self, success: bool, total_ticks: int) -> None:
        self.outcome = "success" if success else "max_ticks_reached"
        self.total_ticks = total_ticks

    def save(self) -> Path:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        base = f"{self.started_at}_{self.task_name}"

        # --- JSON log ---
        json_path = LOGS_DIR / f"{base}.json"
        payload = {
            "task": self.task_name,
            "started_at": self.started_at,
            "outcome": self.outcome,
            "total_ticks": self.total_ticks,
            "ticks": [t.__dict__ for t in self.ticks],
        }
        json_path.write_text(json.dumps(payload, indent=2))

        # --- Plain text summary ---
        txt_path = LOGS_DIR / f"{base}.txt"
        txt_path.write_text(self._build_summary())

        return json_path

    def _build_summary(self) -> str:
        lines = [
            "=" * 60,
            "EPISODE SUMMARY",
            "=" * 60,
            f"Task:        {self.task_name}",
            f"Started:     {self.started_at}",
            f"Outcome:     {self.outcome}",
            f"Total ticks: {self.total_ticks}",
            "",
            "TICK LOG",
            "-" * 60,
        ]
        for t in self.ticks:
            lines += [
                f"[Tick {t.tick}]",
                f"  Position:  {t.agent_position} facing {t.agent_facing}",
                f"  Inventory: {t.inventory}",
                f"  Action:    {t.parsed_action}",
                f"  Result:    {t.action_result}",
                f"  Memory:    {t.memory_notes if t.memory_notes else 'none'}",
            ]
        return "\n".join(lines)