from typing import Optional
from pydantic import BaseModel


class CreateAd(BaseModel):
    title: str
    text: str
    owner: str


class UpdateAd(BaseModel):
    title: Optional[str]
    text: Optional[str]
    owner: Optional[str]
