import dataclasses
from typing import List, Dict
from .alert import Alert

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

