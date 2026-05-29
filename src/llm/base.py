from abc import ABC, abstractmethod

class LLMClient(ABC):
    
    @abstractmethod
    def choose_action(self, observation: str) -> str:
        pass
    
    