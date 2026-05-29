from .base import LLMClient

class OpenAIClient(LLMClient):
    
    def choose_action(self, observation):
        return super().choose_action(observation)