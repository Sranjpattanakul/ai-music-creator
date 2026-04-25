from dataclasses import dataclass


@dataclass
class GenerationRequest:
    title: str
    description: str
    mood: str
    occasion: str
    singer_tone: str
    requested_duration: str = '3:00'
