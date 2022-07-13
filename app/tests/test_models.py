from unittest import TestCase

from pydantic import ValidationError
from pydantic_factories import Ignore

from .factories import (
    EmailNotificationFactory,
    NotificationFactory,
    PostNotificationFactory,
    SMSNotificationFactory,
)


class ModelCreationTestCase(TestCase):
    """Control constrains in models."""

    def test_notification_instance_incorrect(self):
        """Notification model."""

        # should contain name
        with self.assertRaises(ValidationError):
            NotificationFactory.build(name=Ignore())

        # should contain type
        with self.assertRaises(ValidationError):
            NotificationFactory.build(type=Ignore())

    def test_email_notification_instance_incorrect(self):
        """Email Notification model."""

        # should contain email
        with self.assertRaises(ValidationError):
            EmailNotificationFactory.build(email=Ignore())

    def test_post_notification_instance_incorrect(self):
        """Post Notification model."""

        # should contain url
        with self.assertRaises(ValidationError):
            PostNotificationFactory.build(url=Ignore())

    def test_sms_notification_instance_incorrect(self):
        """SMS Notification model."""

        # should contain phone
        with self.assertRaises(ValidationError):
            SMSNotificationFactory.build(phone=Ignore())
