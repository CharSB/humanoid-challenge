# humanoid-challenge

<details>
<summary>Challenge Brief</summary>

## Challenge Description
https://thehumanoid.ai/

Intern Challenge: LLM Agent in a Virtual World

Build a system that places an LLM agent into a virtual world where it can perceive its environment, take actions, and accomplish goals.

The core challenge isn't the world itself — it's the harness: the interface between an intelligent agent and an environment it can act in.

**At a Minimum, Your System Should:**
- Create a virtual environment the agent can exist in
- Define an observation format that represents the agent's current state and surroundings
- Define an action space the agent can use to interact with the world
- Wire up an LLM to observe state, reason, and choose actions in a loop
- Demonstrate the agent completing at least one goal-directed task

**What to Submit:**
- A working codebase
- Clear instructions on how to run your system
- Example inputs and outputs
- (Optional) A short note explaining your design choices

**What We Care About:**
- Quality of the agent harness
- Whether the agent can actually accomplish tasks
- Thoughtfulness about observation representation
- Creativity in the world, tasks, or agent capabilities
- Simplicity and usability

</details>

## Overview

I created a 2D grid-based world for an LLM agent to navigate, explore, and comple goals. The agent is able to "perceive" its environment through a field-of-view cone, limiting it to only reason about what is infront of it. The agent is fed a prompt containing its: task, agent's state, memory, what it can see (ASCII grid), adjacent cells, available actions, rules of the game, and response type. The agent is then able to reason about all of this information and output a structured response from the avialable actions. I also chose to make the program relatively model agnostic. As I do not have any API keys I chose to create a manual mode as well, where I copy and paste prompts and responses between the program and an LLM. 

```
=== LLM Agent World ===
Task: Collect the red key and open the red door.

Tick:      4
Agent:     (3, 2) facing east
Inventory: [key_red]

Agent View            |  Full Map
-----------------------------------
? ? ? ? ? ? ? ? ? ?  |  . . . . . R . . . .
? ? ? ? ? ? ? ? ? ?  |  . . . . . R . . . .
? ? ? > . R ? ? ? ?  |  . . . > . R . r . .
? ? ? . . . ? ? ? ?  |  . . . . . R . . . .
? ? ? . . D ? ? ? ?  |  . . . . . D . . . .
? ? ? ? ? ? ? ? ? ?  |  . k . . . R . . . .
```

## Features

- **2D grid world** with configurable size, objects, and agent start position
- **FOV cone** — the agent can only see within a configurable angle and range; cells not currently visible are show as `?`
- **Side-by-side terminal rendering** — agent's fog-of-war view on the left, full dev map on the right
- **Object types**: short rocks (block movement), tall rocks (block movement and vision), keys, and doors (colour-paired)
- **Agent memory** — the LLM can write notes to its own memory, persisted across ticks
- **Swappable LLM clients** — Anthropic, OpenAI, or Manual (copy-paste) mode
- **Structured JSON actions** with optional memory notes
- **Episode logging** — every run produces a JSON log and plain text summary in `logs/episodes/`
- **61 unit tests** across world mechanics, action parsing, and task evaluation

## Project Structure
```
humanoid-challenge/
├── main.py                 # Main file used to run program
├── .env                    # Used to configure API keys
├── configs/
│   ├── world.yaml          # Active world config
│   ├── test_world.yaml     # Testing world config
│   └── agent.yaml          # LLM provider, model, max ticks
├── src/
│   ├── environment/        # Grid, world state, objects, tasks
│   ├── agent/              # Observe-think-act loop, prompt, parser, memory
│   ├── llm/                # LLM client wrapper, prompts, schemas
│   ├── simulation/         # Episode runner, task evaluator
│   └── utils/              # Episode logger
├── examples/
│   ├── navigate_maze/      # Pure navigation, no keys or doors
│   └── key_and_door/       # Find key, unlock door, reach goal
├── tests/                  # pytest unit tests
└── logs/episodes/          # JSON + plain text episode logs
```

---

## Setup

**Requirements:** Python 3.12+
```bash
# Clone and enter the project
git clone <your-repo-url>
cd humanoid-challenge

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**API Keys:** Create a `.env` file at the project root
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```
Note this is not necessary if you intended to use the program in `manual`

## How to Run
### Manual mode (no API key needed)

Set `provider: manual` in `configs/agent/yaml`. The system will print the prompt each tick and wait for your response.
```bash
python -m src.main
```
Each tick you'll see the prompt to send to an LLM, then pasts the JSON response:
```json
{"action": "move", "direction": "south", "steps": 3}
```

### API mode

Set your provider in `configs/agent.yaml`:
```yaml
provider: anthropic        # or openai
model: claude-sonnet-4-20250514
max_ticks: 100
temperature: 0.3
```
Then run:
```bash
python -m src.main
```

### Run an example

Either:
```bash
python -m src.simulation.runner --world examples/navigate_maze/config.yaml
```
Or:
```bash
python -m src.simulation.runner --world examples/key_and_door/config.yaml
```

### Run Tests

```bash
pytest tests/ -v
```

## Configuration
### `configs/world.yaml`

Controls the world layout:
```yaml
grid:
  width: 10
  height: 10

agent:
  start_x: 0
  start_y: 0
  start_facing: south   # north | south | east | west

fov:
  max_range: 5          # How many cells the agent can see
  max_angle: 135        # Field of view cone in degrees

objects:
  - type: short_rock    # Blocks movement only
    x: 3
    y: 2
  - type: tall_rock     # Blocks movement and vision
    x: 5
    y: 4
  - type: key
    colour: red
    x: 1
    y: 5
  - type: door
    colour: red         # Matched to key by colour
    x: 6
    y: 5

task:
  type: reach_goal      # reach_goal | collect_key | open_door | collect_and_open
  x: 9
  y: 9
```
### `configs/agent.yaml`

Controls the LLM:
```yaml
provider: manual        # manual | anthropic | openai
model: claude-sonnet-4-20250514
max_ticks: 100
temperature: 0.3
```

## Examples
### Example 1: Navigate a Maze

The agent starts at `(0,0)` and must navigate a 12x12 maze with dead ends and no keys or doors to reach `(11,11)`. Because of the agents limited FOV, they cannot see the goal and must explore systematically. 

```bash
python -m src.simulation.runner --world examples/navigate_maze/config.yaml
```

World Layout: 
```
^ . R . . . R . . . . .
R . R . R . R . R R R R
. . R . R . . . . . . R
. R R R R R R R R R . R
. . . . . R . . . R . R
R R R . R R . R . R . R
. . R . R . . R . R . .
. R R . R . R R . R R R
. . . . . . R . . . . R
R R R R . R R . R R . R
. . . R . R . . R . . R
R R . R . R . R R R . G
```

### Example 2: Key and Door

The agent starts at `(0,0)` in a world divided by a locked red door at `(5,4)`. The red key is hidden on the left side at `(2,6)`. The agent must explore to find the key, pick it up, navigate to the door, face it, unlock it, then reach `(9,9)`.

```bash
python -m src.simulation.runner --world examples/key_and_door/config.yaml
```

World Layout:
```
. . . . . R . . . .
. . . . . R . . . .
. . R . . R . r . .
. . R . . R . . . .
. . R R . D . . . .
. . . . . R . r . .
. r k r . R . . . .
. . . . . R . . . .
. . . . . R . . R .
. . . . . R . . R G
```

## Action Space

The agent responds with a single JSON object each tick:

| Action | JSON | Notes |
|--------|------|----|
| Move 1 cell | `{"action": "move", "direction": "north"}` | Also turns agent to face that direction |
| Move multiple cells | `{"action": "move", "direction": "east", "steps": 4}` | Stops early if blocked |
| Pick up item | `{"action": "pick_up"}` | Must be standing on top of the item |
| Unlock faced door | `{"action": "use_key"}` | Must be facing door from adjacent cell
| Any action + memory | `{"action": "move", "direction": "south", "steps": 2, "memory_note": "red door at (5,4)"}` | LLM writes its own notes for future use |

## Episode Logs

Every run (including interrupted ones) saves two files to `logs/episodes/`:

- `2026-05-30_14-32-01_reachgoal.json` — full tick-by-tick log with observations, responses, and world state
- `2026-05-30_14-32-01_reachgoal.txt` — plain text summary

---

## Design Choices
What information does the agent get each tick, and why those three things (grid, adjacency, memory)?
What did you try that didn't work well in the prompt?
Why give the agent a memory it writes itself rather than tracking state automatically?

### Observation Representation

The agent receives three different sets of information each tick:

1. ASCII grid. This provides a spatial overview of everything currently visible, giving the agent a map it can reason from. Seeing what objects are of interest within its FOV or what pathways are blocked.
2. Adjacent cell descriptions. An explicit natural language description of the agent's four neighbouring cells. This allows the LLM to make immediate decisions without parsing the ASCII map.
3. Memory notes. This is a free-text list the agent can write itself, allowing it to record points of interest (doors, keys, etc.) and recall them after moving away

The three sets of information work together to give spatial context, immediate actionable information, and retain information between ticks.

### Action Space

The actions are kept minimal and discrete: move, pick up, and use key. I also allowed the agent to input more than one move in the same direction at a time, in order to reduce "wasted" ticks moving in long lines. I also did not include a "turn" action as the agent can do this by using a movement command, even if the path is blocked the agent will still turn the inputted direction. 

### Field of View

A 16-direction raycasting cone gives more natural visibility than 4-directional rays, as it allows the agent to see diagonally. The agent can also only see in the, configurable, cone in front of it, simulating a more realistic FOV. Vision is blocked by tall rocks and locked doors, forcing the agent to navigate around obstacles. The agent may also take not of objects seen over small rocks, as they provide sight, but block the agent's movement.

### LLM Interface

The client is a simple abstract base class with a single `complete(prompt) -> str` method. Swapping providers is a simple change in `agent.yaml`, also allowing for dev to swap models quickly and easily. The manual client (copy-paste) was essential for developmnent, allowing inspecting of exactly what the LLM sees and also craft responses to test edge cases without spending API credits. 

---

## What Worked...

- Dynamic prompt warnings, such as doors without keys or standing on objects, significantly reduced the agent getting stuck
- Explicit multi-step movement instruction in the prompt stopped the agent from moving one cell at a time
- Keeping memory as a free-text note rather than structured data gave the LLM flexibility to record in a way which was useful to it
- Adding a manual client. Without I would be unable to keep testing the programme when I did not have API credits.

## and What Didn't

- 
- The agent ocassionally gets stuck in mazes. Without the ability to path plan, the agent may continously get stuck in dead ends or repeat the same moves. Prompting the LLM to also create its own copy of a "map" or dead end paths may stop this from occurring.
- Memory is permanent. A long episode accumulates lots of stale notes, having it be a fixed amount of notes may force the agent to prioritise certain information of others, creating more interesting behaviour while exploring larger maps.
- There is a very limited palette of objects to create the world with. Introducing more objects, like traps, teleporters, or coins, would allow for more interesting behaviour and create a more fun interaction between us and the LLM.  
- `observation.py` does all the prompt building. As I realised more information should be sent to the LLM it kept on growing. INstead a seperate `prompt_builder.py` may be better suited to handle prompts. 
- The match/case pattern is both in `harness.py` and `parser.py`. Adding a new action type would mean updating both. Instead the execution logic should be within the action classes themselves. 
