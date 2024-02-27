from typing import Optional, Any

from pydantic import BaseModel, model_validator

from src.settings.error_messages import MISSING_PARAMETER, MISSING_SEARCH_CRITERIA


class SearchCriteria(BaseModel):
    title: Optional[str] = None
    genre_name: Optional[str] = None
    artist_name: Optional[str] = None
    album_name: Optional[str] = None

    @model_validator(mode='before')
    def is_empty(self):
        """
        Checks whether all metadata fields are None
        At least one metadata field should be passed
        """
        if set(self.keys()) == {''}:
            raise ValueError(MISSING_PARAMETER)
        return self


    '''
    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, data: Any) -> Any:
        if set(self.dict().values()) == {None}:  # or {''} # if all fields are None
            raise ValueError(MISSING_SEARCH_CRITERIA)

        if isinstance(data, dict):
            fields = ['title', 'genre_name', 'artist_name', 'album_name']
            if not any(data.get(field) for field in fields):
                raise ValueError(MISSING_SEARCH_CRITERIA)
        return data


 
    @model_validator(mode='before')
    def check_at_least_one_field(self, values):
        if not any(value for value in values.values() if value is not None):
            raise ValueError(MISSING_SEARCH_CRITERIA)
        return values
    '''
