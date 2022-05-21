import dataclasses
from typing import Dict

@dataclasses.dataclass
class Alert:
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    startsAt: str
    endsAt: str
    generatorURL: str
