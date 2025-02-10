"""
prompt_optimizer.py

En enkel promptoptimizer som exempelvis kan trimma prompts om de blir för långa.
Här kan du lägga till mer avancerad logik vid behov.
"""

from typing import Dict, Any

class PromptOptimizer:
    def __init__(self, max_tokens: int = 60000):
        self.max_tokens = max_tokens

    def optimize(self, prompt: str) -> str:
        # Enkel uppskattning: 4 tecken per token
        token_estimate = len(prompt) // 4
        if token_estimate > self.max_tokens:
            # Trunkera prompten så att den ryms inom max_tokens
            prompt = prompt[: self.max_tokens * 4]
        return prompt

# Skapa en singleton-instans
prompt_optimizer = PromptOptimizer()
