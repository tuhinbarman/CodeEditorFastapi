from pydantic import BaseModel,Field
from typing import Optional


class RoomRequest(BaseModel):

    username : str = Field(max_length=255)
    no_of_users_allowed : int
    code :Optional[str] = None 

class AutoCompleteRequest(BaseModel):

    room_id : int
    code :str
