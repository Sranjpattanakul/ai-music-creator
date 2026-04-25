from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GenerationResult:
    task_id: str
    status: str
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[str] = None
    raw_data: Optional[dict] = field(default_factory=dict)
