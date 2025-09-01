from pydantic import BaseModel, Field
from typing import Optional

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    year: Optional[str] = None
    description: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None

class MovieOut(MovieBase):
    id: int
    class Config:
        from_attributes = True
