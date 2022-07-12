from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import ValidationError

from models import NotificationModel


class AbstractHandler(ABC):
    """"""

    _next_handler: AbstractHandler = None

    def set_next(self, handler: AbstractHandler) -> AbstractHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, notification: Any) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(notification)
        return None


class NotificationHandler(AbstractHandler):
    def __init__(self, model):
        self.model = model

    def _get_instance(self, notification: NotificationModel):

        try:
            return self.model(**notification.dict())
        except ValidationError as er:
            return None

    def handle(self, notification: NotificationModel) -> Optional[str]:
        instance: NotificationModel = self._get_instance(notification)
        if instance is not None:
            instance.notify()
        return super().handle(notification)
