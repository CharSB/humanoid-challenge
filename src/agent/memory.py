from dataclasses import dataclass, field

@dataclass
class Memory:
    notes: list[str]
    
    def add(self, note: str) -> None:
        self.notes.append(note)
        
    def as_text(self) -> str:
        if not self.notes:
            return "No notes yet."
        return "\n".join(f"- {note}" for note in self.notes)