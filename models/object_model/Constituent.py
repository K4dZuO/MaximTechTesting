from pydantic import BaseModel, HttpUrl
from typing import Optional, Union


class Constituent(BaseModel):
    constituentID: int
    role: str
    name: str
    constituentULAN_URL: Optional[Union[HttpUrl, str]]
    constituentWikidata_URL: Optional[Union[HttpUrl, str]]
    gender: Optional[str]