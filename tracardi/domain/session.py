from datetime import datetime
from typing import Optional, Any
from uuid import uuid4

from .entity import Entity
from .metadata import Metadata
from .time import Time
from .value_object.operation import Operation
from .value_object.storage_info import StorageInfo


class Session(Entity):
    metadata: Optional[Metadata]
    operation: Operation = Operation()
    profile: Optional[Entity] = None
    context: Optional[dict] = {}
    properties: Optional[dict] = {}

    def __init__(self, **data: Any):
        data['metadata'] = Metadata(
            time=Time(
                insert=datetime.utcnow()
            ))
        super().__init__(**data)

    def replace(self, session):
        self.metadata = session.metadata
        self.profile = session.profile
        self.context = session.context
        self.id = session.id
        self.properties = session.properties
        self.operation = session.operation

    @staticmethod
    def storage_info() -> StorageInfo:
        return StorageInfo(
            'session',
            Session
        )

    @staticmethod
    def new() -> 'Session':
        return Session(id=str(uuid4()))
