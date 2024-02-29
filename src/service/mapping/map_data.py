import base64

from src.api.middleware.custom_exceptions.missing_title_from_metadata_error import MissingTitleFromMetadataError
from src.api.myapi.metadata_model import MetadataResponse, Artist
from src.api.myapi.music_db_models import ConversionResponse
from src.settings.error_messages import MISSING_TITLE_FROM_METADATA


def map_data_from_request_call(res) -> MetadataResponse:
    # map the data to the response model so that the response is independent of the underlying service
    # input data from title is List of str and needs to be converted to List of Artist objects

    res_from_request = res.json()

    if res_from_request.get('title', None) is None:
        raise MissingTitleFromMetadataError(MISSING_TITLE_FROM_METADATA)

    list_of_artists = res_from_request.get('artists', None)
    if list_of_artists:
        artists_objects = [Artist(name=artist) for artist in list_of_artists]
        res_from_request['artists'] = artists_objects

    return MetadataResponse(**res_from_request)


def map_converted_data_from_request_call(res) -> ConversionResponse:
    data = res.json()
    file_type = data['file_type']
    file_data = data['file_data']
    content_as_bytes = base64.b64decode(file_data)
    return ConversionResponse(file_type=file_type, file_data=content_as_bytes)
