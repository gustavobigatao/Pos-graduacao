from dagster import ConfigurableResource, IAttachDifferentObjectToOpContext
from sqlalchemy.orm import Session

from src.models.database import SessionLocal


class DatabaseResource(ConfigurableResource, IAttachDifferentObjectToOpContext):
    def get_session(self) -> Session:
        return SessionLocal()

    def attach_to_object(self, context):
        return self.get_session()
