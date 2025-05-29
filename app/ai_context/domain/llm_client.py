from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class LLMClient(ABC):
    @abstractmethod
    def get_client(self) -> Any:
        """Get the LLM client."""
        pass
