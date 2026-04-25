from abc import ABC, abstractmethod
from .generation_request import GenerationRequest
from .generation_result import GenerationResult


class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        """Submit a song generation request and return a result with a task_id."""

    @abstractmethod
    def get_status(self, task_id: str) -> GenerationResult:
        """Poll the status of a previously submitted generation task."""
