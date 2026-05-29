import math

from src.environment.objects import WorldObject

# 16 compass directions as unit vectors
_DIRECTIONS_16: list[tuple[float, float]] = [
    (0, -1),           # N
    (0.5, -1),         # NNE  (normalised below)
    (1, -1),           # NE
    (1, -0.5),         # ENE
    (1, 0),            # E
    (1, 0.5),          # ESE
    (1, 1),            # SE
    (0.5, 1),          # SSE
    (0, 1),            # S
    (-0.5, 1),         # SSW
    (-1, 1),           # SW
    (-1, 0.5),         # WSW
    (-1, 0),           # W
    (-1, -0.5),        # WNW
    (-1, -1),          # NW
    (-0.5, -1),        # NNW
]

FACING_VECTORS = {
    "north": (0, -1),
    "east": (1, 0),
    "south": (0, 1),
    "west": (-1, 0),
}

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._cells: list[list[WorldObject | None]] = [
            [None] * width for _ in range(height)
        ]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get(self, x: int, y: int) -> WorldObject | None:
        if not self.in_bounds(x, y):
            raise ValueError(f"Position ({x}, {y}) is out of bounds.")
        return self._cells[y][x]
    
    def place(self, obj: WorldObject, x: int, y: int) -> None:
        if not self.in_bounds(x, y):
            raise ValueError(f"Position ({x}, {y}) is out of bounds.")
        if self._cells[y][x] is not None:
            raise ValueError(f"Cell ({x}, {y}) is already occupied by {self._cells[y][x].name}.")
        self._cells[y][x] = obj

    def remove(self, x: int, y: int) -> WorldObject | None:
        if not self.in_bounds(x, y):
            raise ValueError(f"Position ({x}, {y}) is out of bounds.")
        obj = self._cells[y][x]
        self._cells[y][x] = None
        return obj

    def compute_visible_cells(
        self, agent_x: int, agent_y: int, facing: str, max_range: int, max_angle: int
    ) -> set[tuple[int,int]]:
        """
        Cast rays in directions from the agent's position. Return the set of (x, y) cells the agent can see. Vision is blocked by cells whose objects block_vision. The blocking cell itself is visible (agent sees the blocker).
        """
        
        visible: set[tuple[int, int]] = {(agent_x, agent_y)}

        face_dx,face_dy = FACING_VECTORS[facing]
        
        half_angle = max_angle / 2
        cos_threshold = math.cos(math.radians(half_angle))
        
        
        for dx, dy in _DIRECTIONS_16:
            
            # normalise ray direction
            length = math.sqrt(dx * dx + dy * dy)
            step_x = dx / length
            step_y = dy / length

            dot = (
                step_x * face_dx + 
                step_y * face_dy
            )
            
            if dot < cos_threshold:
                continue
            
            for dist in range(1, max_range + 1):
                cx = int(round(agent_x + step_x * dist))
                cy = int(round(agent_y + step_y * dist))

                if not self.in_bounds(cx, cy):
                    break

                visible.add((cx, cy))

                obj = self._cells[cy][cx]
                if obj is not None and obj.blocks_vision:
                    break

        return visible

    def render(
        self, 
        agent_symbol: str, 
        agent_x: int, 
        agent_y: int,
        visible_cells: set[tuple[int, int]]| None = None
    ) -> str:
        
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == agent_x and y == agent_y:
                    row.append(agent_symbol)
                elif visible_cells is not None and (x, y) not in visible_cells:
                    row.append("?")
                elif self._cells[y][x] is not None:
                    row.append(self._cells[y][x].symbol)
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)
    