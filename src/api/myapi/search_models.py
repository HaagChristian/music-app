from pydantic import BaseModel, model_validator
from typing import Optional, Any
from src.settings.error_messages import MISSING_SEARCH_CRITERIA


class SearchCriteria(BaseModel):
    title: Optional[str] = None
    genre_name: Optional[str] = None
    artist_name: Optional[str] = None
    album_name: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, data: Any) -> Any:
        if isinstance(data, dict):
            fields = ['title', 'genre_name', 'artist_name', 'album_name']
            if not any(data.get(field) for field in fields):
                raise ValueError(MISSING_SEARCH_CRITERIA)
        return data


    '''
    @model_validator(mode='before')
    def check_at_least_one_field(self, values):
        if not any(value for value in values.values() if value is not None):
            raise ValueError(MISSING_SEARCH_CRITERIA)
        return values
    '''
