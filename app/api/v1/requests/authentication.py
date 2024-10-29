from pydantic import BaseModel, Field


class RequestAuthentication(BaseModel):
    username: str = Field(..., title="Username", description="Username")
    password: str = Field(..., title="Password", description="Password")
    grant_type: str = Field(None, title="Grant Type", description="Grant Type")
    scope: str | None = Field(None, title="Scope", description="Scope")

class RequestRefreshToken(BaseModel):
    refresh_token: str = Field(..., title="Refresh Token", description="Refresh Token")
    grant_type: str = Field(None, title="Grant Type", description="Grant Type")
    scope: str | None = Field(None, title="Scope", description="Scope")