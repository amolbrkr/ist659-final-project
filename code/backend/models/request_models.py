from pydantic import BaseModel


class PlayerCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str

