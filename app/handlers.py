from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Optional

from config import logging
from logdecorator import log_on_error
from models import NotificationModel
from pydantic import ValidationError


class AbstractHandler(ABC):
    """Base class for chain of handlers to find responsible one."""

    _next_handler: AbstractHandler = None

    def set_next(self, handler: AbstractHandler) -> AbstractHandler:
        """Set next responsible handler in a Chain."""

        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, notification: Any) -> Any:
        """If current handler is not appropriate then go to hext."""
        if self._next_handler:
            return self._next_handler.handle(notification)
        return None


class NotificationHandler(AbstractHandler):
    """Use models to validate the notification object."""

    def __init__(self, model):
        self.model: ClassVar[NotificationModel] = model

    @log_on_error(
        logging.ERROR,
        "{notification!s} {e!r}",
        on_exceptions=ValidationError,
        reraise=True,
    )
    def _get_instance(self, notification: dict):
        return self.model(**notification)

    def handle(self, notification: dict) -> Optional[NotificationModel]:
        """Get Notification model instance or go to next handler."""

        try:
            return self._get_instance(notification)
        except ValidationError:
            return super().handle(notification)
