from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, model_validator, field_validator

from src.settings.error_messages import MISSING_PARAMETER


class Artist(BaseModel):
    name: str


class MetadataResponse(BaseModel):
    title: str
    artists: Optional[List[Artist]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[float] = None
    failed_tags: Optional[List[str]] = Field(None,
                                             description='List of metadata keys which are not in the metadata of the file')


class MetadataFromSearch(BaseModel):
    title: Optional[str] = None
    artists: Optional[List[Artist]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[float] = None
    file_id: int


class MetadataToChange(BaseModel):
    artists: Optional[List[Artist]] = None
    genre: Optional[str] = None
    album: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = Field(None, description='Date in format YYYY-MM-DD')
    song_id: int

    @model_validator(mode='before')
    def is_empty(self):
        """
        Checks whether all metadata fields are None
        At least one metadata field should be passed
        """
        if set(self.keys()) == {'song_id'}:
            raise ValueError(MISSING_PARAMETER)
        return self

    @field_validator('date')
    def map_date(cls, value):
        if value:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        return value


class MetadataId3Input(BaseModel):
    artists: Optional[str] = Field(None, description='As string separated by ;')
    genre: Optional[str] = None
    album: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = Field(None, description='Date in format YYYY-MM-DD')


class DBMetadata(BaseModel):
    artists: Optional[List[Artist]] = None
    genre: Optional[str] = None
    album: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    song_id: int

    @field_validator('date')
    def map_date(cls, value):
        if value:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        return value
