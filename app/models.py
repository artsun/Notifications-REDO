import re
from typing import Literal, Optional

from methods import send_email, send_post, send_sms
from pydantic import AnyHttpUrl, BaseModel, EmailStr, validator


class NotificationModel(BaseModel):
    """Basic notification object. Name and Type should be valid."""

    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    url: Optional[AnyHttpUrl]
    type: Literal["email", "post", "sms"]

    class Config:
        anystr_strip_whitespace = True

    @validator("name")
    def name_validation(cls, value: str):
        """Empty str is not allowed."""

        if not value:
            raise ValueError("Name is Empty.")

        return value

    def notify(self):
        raise NotImplementedError()


class SMSNotificationModel(NotificationModel):
    phone: str

    @validator("phone")
    def phone_validation(cls, value: str):
        """Check if phone number contains capital letters."""

        regex = r"[A-Z]"
        if value and re.search(regex, value):
            raise ValueError("Phone Number is Invalid.")

        return value

    def notify(self):
        return send_sms(self.phone, {"name": self.name})


class EmailNotificationModel(NotificationModel):
    email: EmailStr

    def notify(self):
        return send_email(self.email, {"name": self.name})


class PostNotificationModel(NotificationModel):
    url: AnyHttpUrl

    def notify(self):
        return send_post(self.url, {"name": self.name})
