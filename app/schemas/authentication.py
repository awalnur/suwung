from pydantic import BaseModel


class RequestAuthentication(BaseModel):
    username: str
    password: str