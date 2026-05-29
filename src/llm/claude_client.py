from .base import LLMClient

class ClaudeClient(LLMClient):
    
    def choose_action(self, observation):
        return super().choose_action(observation)