from src.environment.objects import WorldObject

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

    def render(self, agent_symbol: str, agent_x: int, agent_y: int) -> str:
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == agent_x and y == agent_y:
                    row.append(agent_symbol)
                elif self._cells[y][x] is not None:
                    row.append(self._cells[y][x].symbol)
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)
    