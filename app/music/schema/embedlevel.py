from dataclasses import dataclass

@dataclass(frozen=True)
class LevelsSchema:
    color: int
    emoji: str

@dataclass(frozen=True)
class EmbedLevelsData:
    notice: LevelsSchema
    warning: LevelsSchema
    error: LevelsSchema

@dataclass(frozen=True)
class DefaultsData:
    title: str
    description: str
    footer: str
    icon_url: str