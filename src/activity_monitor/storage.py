import abc
import uuid
from . import models
from pydantic import ValidationError
from sqlalchemy import Column, String, DateTime, JSON, Uuid
from .database import Base
from typing import Any


class BaseStorageService(abc.ABC):
    """
    Abstract base class for storage services.
    """

    @abc.abstractmethod
    def store_event(self, event: models.EventModel) -> None:
        """
        Store an activity event.

        Args:
            event (models.EventModel): The event to be stored.
        """
        raise NotImplementedError


class ConsoleStorageService(BaseStorageService):
    """
    A simple storage service that logs events to the console.
    """

    def store_event(self, event: models.EventModel) -> None:
        """
        Stores the event by printing it's details to the console.
        """
        print("=" * 30)
        print(f"Storing event: {event}")
        print(f"  - Event Type: {event.event_type}")
        print(f"  - Session ID: {event.session_id}")
        print(f"  - Timestamp: {event.timestamp}")
        print(f"  - Payload: {event.payload}")
        print("=" * 30)


class PostgreSQLStorageService(BaseStorageService):
    """
    A storage service that saves events to a PostgreSQL database.
    """

    def __init__(self, db_session: object):
        """
        Initialize the PostgreSQL storage service.
        """
        self.db_session = db_session

    def store_event(self, event: models.EventModel) -> None:
        """
        Stores the event in the PostgreSQL database.
        """
        try:
            db_event = SqlAlchemyEventModelTable(
                session_id=event.session_id,
                website_id=event.website_id,
                url=event.url,
                timestamp=event.timestamp,
                event_type=event.event_type,
                payload=event.payload.model_dump(),
            )
            self.db_session.add(db_event)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Failed to store event: {e}")