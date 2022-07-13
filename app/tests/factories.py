from faker import Faker
from models import (
    EmailNotificationModel,
    NotificationModel,
    PostNotificationModel,
    SMSNotificationModel,
)
from pydantic_factories import ModelFactory

Fk = Faker()


class NotificationFactory(ModelFactory):
    __model__ = NotificationModel

    name = Fk.name


class SMSNotificationFactory(ModelFactory):
    __model__ = SMSNotificationModel

    phone = Fk.phone_number


class EmailNotificationFactory(ModelFactory):
    __model__ = EmailNotificationModel


class PostNotificationFactory(ModelFactory):
    __model__ = PostNotificationModel
