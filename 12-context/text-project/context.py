from pydantic import BaseModel
from typing import Optional, List, Dict

class UserSessionContext(BaseModel):
    name: str = "TestUser"
    uid: int = 0

    