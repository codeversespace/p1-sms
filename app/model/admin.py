from datetime import date
from random import randint

from pydantic import BaseModel, Field, EmailStr


def get_random_digits(length: str = 10):
    return ''.join(["{}".format(randint(0, 9)) for num in range(0, length)])


class AdminSchema(BaseModel):
    email: str = Field(None, max_length=30)
    phone: str = Field(None, max_length=10, min_length=10)
    password: str = Field(None, max_length=60, min_length=8)
    createdOn: date
    accountStatus: str = Field(None, max_length=98)
    role: str = Field(None, max_length=10)

    class Config:
        schema_extra = {
            "example": {
                "email": f"example@{get_random_digits(3)}.com",
                "phone": get_random_digits(10),
                "password": "admin123",
                "createdOn": "2022-09-09",
                "accountStatus": "active",
                "role": "admin"
            }
        }


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }
