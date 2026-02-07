FILE llm_token_budgeting/domain/models.py
```python
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum, auto


class TokenSource(Enum):
    """Enumeration for token source types."""
    PROMPT = auto()
    COMPLETION = auto()
    SYSTEM = auto()


@dataclass(frozen=True)
class TokenBudget:
    """
    Represents the token budget allocated and consumed within an LLM session.

    Attributes:
        total_tokens: The maximum total tokens allowed in the session.
        prompt_tokens: Number of tokens consumed by the prompt.
        completion_tokens: Number of tokens consumed by the completion/generated response.
        system_tokens: Tokens reserved for system instructions or metadata.
    """
    total_tokens: int
    prompt_tokens: int = 0
    completion_tokens: int = 0
    system_tokens: int = 0

    def remaining_tokens(self) -> int:
        """Calculate remaining tokens available."""
        consumed = self.prompt_tokens + self.completion_tokens + self.system_tokens
        return max(self.total_tokens - consumed, 0)

    def allocate_tokens(self, count: int, source: TokenSource) -> 'TokenBudget':
        """
        Return a new TokenBudget with tokens allocated for the given source.

        Args:
            count: Number of tokens to allocate.
            source: The TokenSource indicating the token type.

        Returns:
            A new TokenBudget instance with updated token counts.

        Raises:
            ValueError: If allocation exceeds total_tokens.
        """
        new_prompt = self.prompt_tokens
        new_completion = self.completion_tokens
        new_system = self.system_tokens

        if source == TokenSource.PROMPT:
            new_prompt += count
        elif source == TokenSource.COMPLETION:
            new_completion += count
        elif source == TokenSource.SYSTEM:
            new_system += count
        else:
            raise ValueError("Invalid token source")

        if new_prompt + new_completion + new_system > self.total_tokens:
            raise ValueError("Token allocation exceeds total budget")

        return TokenBudget(
            total_tokens=self.total_tokens,
            prompt_tokens=new_prompt,
            completion_tokens=new_completion,
            system_tokens=new_system,
        )
```
