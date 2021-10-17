from dataclasses import dataclass

@dataclass(frozen=True)
class EmbedLevelSchema:
    color: int
    emoji: str