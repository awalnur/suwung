from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(..., title="Access Token", description="Access Token")
    token_type: str = Field('Bearer', title="Token Type", description="Token Type")
    expires_in: int = Field(..., title="Expires In", description="Expires In")
    refresh_token: str = Field(..., title="Refresh Token", description="Refresh Token")