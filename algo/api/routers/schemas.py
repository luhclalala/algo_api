from pydantic import BaseModel
from typing import Optional, Literal
from pyprojroot import here
import sys
sys.path.append(str(here()))

class QuestionRequest(BaseModel):
    query: str

class TaskResponse(BaseModel):
    task_id: str

class PollResponse(BaseModel):
    task_id: str
    status: Literal["processing", "completed", "failed"]
    result: Optional[str] = None
