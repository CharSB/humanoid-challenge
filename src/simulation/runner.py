from __future__ import annotations
import yaml
import argparse
from pathlib import Path

from src.environment.world import World
from src.environment.tasks import task_from_yaml
from src.llm.client import client_from_config
from src.agent.harness import AgentHarness

WORLD_CONFIG = Path("configs/world.yaml")
AGENT_CONFIG = Path("configs/agent.yaml")


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--world",
        type=Path,
        default=WORLD_CONFIG,
        help="Path to world config yaml"
    )
    parser.add_argument(
        "--agent",
        type=Path,
        default=AGENT_CONFIG,
        help="Path to agent config yaml"
    )
    args = parser.parse_args()
    run_episode(world_config=args.world, agent_config=args.agent)