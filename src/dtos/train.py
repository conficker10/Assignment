from pydantic import BaseModel
from typing import Optional

class Train(BaseModel):
    trainNo: int
    scheduleTime: str
    day: list
    platform: int

class TrainUpdate(BaseModel):
    arrivalTime: str

class TrainUpdateSchedule(BaseModel):
    scheduleTime: Optional[str]
    day: Optional[list]