from pydantic import SecretStr, Field
from src.schemas.base import BaseSchema

class User(BaseSchema):
    login: str = Field(..., validation_alias="username")
    password: SecretStr