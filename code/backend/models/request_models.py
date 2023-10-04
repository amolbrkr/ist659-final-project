from pydantic import BaseModel


class LobbyCreate(BaseModel):
    lobby_name: str


class PlayerCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str

