from __future__ import annotations
import yaml
from pathlib import Path

from src.environment.world import World
from src.environment.tasks import task_from_yaml
from src.llm.client import client_from_config
from src.agent.harness import AgentHarness

WORLD_CONFIG  = Path("configs/world.yaml")
AGENT_CONFIG  = Path("configs/agent.yaml")


def run_episode(
    world_config: Path = WORLD_CONFIG,
    agent_config: Path = AGENT_CONFIG,
) -> bool:
    with open(world_config) as f:
        world_cfg = yaml.safe_load(f)

    with open(agent_config) as f:
        agent_cfg = yaml.safe_load(f)

    world  = World.from_yaml(world_config)
    task   = task_from_yaml(world_cfg["task"])
    client = client_from_config(agent_cfg)

    harness = AgentHarness(
        world=world,
        task=task,
        client=client,
        max_ticks=agent_cfg.get("max_ticks", 100),
    )

    return harness.run()


if __name__ == "__main__":
    run_episode()