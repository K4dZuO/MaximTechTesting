from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional

class SearchQuery(BaseModel):
    q: str
    isHighlight: Optional[bool] = None
    title: Optional[bool] = None
    tags: Optional[bool] = None
    departmentId: Optional[int] = None
    isOnView: Optional[bool] = None
    artistOrCulture: Optional[bool] = None
    medium: Optional[str] = None
    hasImages: Optional[bool] = None
    geoLocation: Optional[str] = None
    dateBegin: Optional[int] = None
    dateEnd: Optional[int] = None

    @field_validator('isHighlight', mode='before')
    def check_isHighlight(cls, v):
        if isinstance(v, str):
            raise ValueError('isHighlight must be a boolean')
        return v
