from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    email: str = Field(None, max_length=30, min_length=8)
    password: str = Field(None, max_length=60, min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "example@abc.com",
                "password": "60 characters encrypted string"
            }
        }