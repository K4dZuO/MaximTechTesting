from pydantic import BaseModel
from typing import Optional


class Measurement(BaseModel):
    elementName: Optional[str]
    elementDescription: Optional[str]
    elementMeasurements: dict