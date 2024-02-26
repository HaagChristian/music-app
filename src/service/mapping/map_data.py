from src.api.middleware.custom_exceptions.MissingTitleFromMetadataError import MissingTitleFromMetadataError
from src.api.myapi.metadata_model import MetadataResponse, Artist
from src.settings.error_messages import MISSING_TITLE_FROM_METADATA


def map_data_from_request_call(res) -> MetadataResponse:
    # map the data to the response model so that the response is independent of the underlying service
    list_of_artists = res.json().get('artists', [])
    artists_objects = [Artist(name=artist) for artist in list_of_artists]

    res_from_request = res.json()
    res_from_request['artists'] = artists_objects

    if res_from_request.get('title', None) is None:
        raise MissingTitleFromMetadataError(MISSING_TITLE_FROM_METADATA)

    return MetadataResponse(**res_from_request)
