from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, Field, model_validator, field_validator

from src.settings.error_messages import MISSING_PARAMETER, INVALID_YEAR, IMPOSSIBLE_YEAR


class Artist(BaseModel):
    name: str


class DBMetadata(BaseModel):
    artists: Optional[List[Artist]] = None
    genre: Optional[str] = None
    album: Optional[str] = None
    title: Optional[str] = None
    date: Optional[Union[int]] = Field(None, description='Date is only provided as year')
    song_id: int

    @field_validator('date', mode='before')
    def parse_year(cls, value):
        if value is not None:
            try:
                year = int(value)
                if year < 1000 or year > datetime.now().year:
                    raise ValueError(IMPOSSIBLE_YEAR)
                return year
            except ValueError:
                raise ValueError(INVALID_YEAR)
        return None


# Input models

class MetadataToChangeRequest(BaseModel):
    artists: Optional[List[Artist]] = None
    genre: Optional[str] = None
    album: Optional[str] = None
    title: Optional[str] = None
    date: Optional[Union[int]] = Field(None, description='Date is only provided as year')
    # Union is required because the date can be None
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

    @field_validator('date', mode='before')
    def parse_year(cls, value):
        if value is None:
            return None
        try:
            year = int(value)
            if year < 1000 or year > datetime.now().year:
                raise ValueError(IMPOSSIBLE_YEAR)
            return year
        except ValueError:
            raise ValueError(INVALID_YEAR)


class MetadataId3Input(BaseModel):
    artists: Optional[str] = Field(None, description='As string separated by ;')
    genre: Optional[str] = None
    album: Optional[str] = None
    title: Optional[str] = None
    date: Optional[Union[int]] = Field(None, description='Date is only provided as year')


# Output models

class MetadataResponse(BaseModel):
    """ Response model for metadata with date validation """

    title: str
    artists: Optional[List[Artist]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[Union[int]] = Field(None, description='Date is only provided as year')
    duration: Optional[float] = None
    failed_tags: Optional[List[str]] = Field(None,
                                             description='List of metadata keys which are not in the '
                                                         'metadata of the file')

    @field_validator('date', mode='before')
    def parse_year(cls, value):
        if value is not None:
            try:
                year = int(value)
                if year < 1000 or year > datetime.now().year:
                    raise ValueError(IMPOSSIBLE_YEAR)
                return year
            except ValueError:
                raise ValueError(INVALID_YEAR)
        return None


class MetadataFromSearch(BaseModel):
    title: Optional[str] = None
    artists: Optional[List[Artist]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[float] = None
    file_id: int
