from pydantic import BaseModel


class TestToken(BaseModel):
    token: str