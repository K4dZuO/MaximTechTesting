from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union
from datetime import datetime


from . import Constituent, Measurement, Tag


class MetObject(BaseModel):
    objectID: int
    isHighlight: bool
    accessionNumber: str
    accessionYear: Optional[str]
    isPublicDomain: bool
    primaryImage: Optional[Union[HttpUrl, str]]
    primaryImageSmall: Optional[Union[HttpUrl, str]]
    additionalImages: List[Union[HttpUrl, str]]
    constituents: Optional[List[Constituent]]
    department: Optional[str]
    objectName: Optional[str]
    title: Optional[str]
    culture: Optional[str]
    period: Optional[str]
    dynasty: Optional[str]
    reign: Optional[str]
    portfolio: Optional[str]
    artistRole: Optional[str]
    artistPrefix: Optional[str]
    artistDisplayName: Optional[str]
    artistDisplayBio: Optional[str]
    artistSuffix: Optional[str]
    artistAlphaSort: Optional[str]
    artistNationality: Optional[str]
    artistBeginDate: Optional[str]
    artistEndDate: Optional[str]
    artistGender: Optional[str]
    artistWikidata_URL: Optional[Union[HttpUrl, str]]
    artistULAN_URL: Optional[Union[HttpUrl, str]]
    objectDate: Optional[str]
    objectBeginDate: Optional[Union[int, str]]
    objectEndDate: Optional[Union[int, str]]
    medium: Optional[str]
    dimensions: Optional[str]
    measurements: Optional[List[Measurement]]
    creditLine: Optional[str]
    geographyType: Optional[str]
    city: Optional[str]
    state: Optional[str]
    county: Optional[str]
    country: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    locale: Optional[str]
    locus: Optional[str]
    excavation: Optional[str]
    river: Optional[str]
    classification: Optional[str]
    rightsAndReproduction: Optional[str]
    linkResource: Optional[Union[HttpUrl, str]]
    metadataDate: Optional[datetime]
    repository: Optional[str]
    objectURL: Optional[Union[HttpUrl, str]]
    tags: Optional[List[Tag]]
    objectWikidata_URL: Optional[Union[HttpUrl, str]]
    isTimelineWork: Optional[bool]
    GalleryNumber: Optional[str]