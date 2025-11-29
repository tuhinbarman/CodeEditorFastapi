from pydantic import BaseModel,Field
from typing import Optional


class RoomRequest(BaseModel):

    username : str = Field(max_length=255)
    no_of_users_allowed : int = Field(max_digits=2)
    code :Optional[str] = None 