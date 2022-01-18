import dataclasses
from typing import List, Dict


@dataclasses.dataclass
class Alert:
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    startsAt: str
    endsAt: str
    generatorURL: str


@dataclasses.dataclass
class Webhook:
    receiver: str
    status: str
    alerts: List[Alert]
    groupLabels: Dict[str, str]
    commonLabels: Dict[str, str]
    commonAnnotations: Dict[str, str]
    externalURL: str
    version: str

