from __future__ import annotations
import os
import json
from abc import ABC, abstractmethod

from dotenv import load_dotenv

load_dotenv()


class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Send a prompt and return the raw response string."""
        
class AnthropicClient(LLMClient):
    def __init__(self, model: str, temperature: float = 0.3):
        import anthropic
        self.model = model
        self.temperature = temperature
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def complete(self, prompt: str) -> str:
        from src.llm.prompts import SYSTEM_PROMPT
        message = self.client.messages.create(
            model=self.model,
            max_tokens=256,
            temperature=self.temperature,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    
class OpenAIClient(LLMClient):
    def __init__(self, model: str, temperature: float = 0.3):
        import openai
        self.model = model
        self.temperature = temperature
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def complete(self, prompt: str) -> str:
        from src.llm.prompts import SYSTEM_PROMPT
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

class ManualClient(LLMClient):
    def complete(self, prompt: str) -> str:
        print("\n" + "="*60)
        print("PROMPT TO SEND TO LLM:")
        print("="*60)
        print(prompt)
        print("="*60)
        print("Paste the LLM response below, then press Enter twice:")
        print("="*60 + "\n")

        lines = []
        while True:
            line = input()
            if line == "" and lines:
                break
            lines.append(line)

        return "\n".join(lines).strip()

PROVIDERS: dict[str, type[LLMClient]] = {
    "anthropic": AnthropicClient,
    "openai": OpenAIClient,
    "manual": ManualClient,

}

def client_from_config(cfg: dict) -> LLMClient:
    provider = cfg.get("provider", "anthropic").lower()
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: '{provider}'. Choose from {list(PROVIDERS)}")
    if provider == "manual":
        return ManualClient()
    return PROVIDERS[provider](
        model=cfg["model"],
        temperature=cfg.get("temperature", 0.3)
    )