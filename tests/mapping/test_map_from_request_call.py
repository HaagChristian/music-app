from src.api.middleware.custom_exceptions.MissingTitleFromMetadataError import MissingTitleFromMetadataError
from src.api.myapi.metadata_model import MetadataResponse, Artist
from src.service.mapping.map_data import map_data_from_request_call
from src.settings.error_messages import MISSING_TITLE_FROM_METADATA


class MockResponse:
    # required to mock the response object because the function map_data_from_request_call uses
    # the response.json() method
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


# Mock data
sample_response_data = {
    "title": "Sample Title",
    "artists": ["Artist 1", "Artist 2"]
}


def test_map_data_with_valid_data():
    res = map_data_from_request_call(MockResponse(sample_response_data))
    expected_response = MetadataResponse(title="Sample Title",
                                         artists=[Artist(name="Artist 1"), Artist(name="Artist 2")])
    assert res == expected_response


def test_map_data_with_valid_data_and_one_artist():
    sample_response_data_copy = sample_response_data.copy()
    sample_response_data_copy['artists'] = ["Artist 1"]

    res = map_data_from_request_call(MockResponse(sample_response_data_copy))
    expected_response = MetadataResponse(title="Sample Title",
                                         artists=[Artist(name="Artist 1")])
    assert res == expected_response


def test_map_data_with_missing_title():
    sample_response_data_copy = sample_response_data.copy()
    sample_response_data_copy.pop('title')
    try:
        map_data_from_request_call(MockResponse(sample_response_data_copy))
        assert False, "Expected MissingTitleFromMetadataError"
    except MissingTitleFromMetadataError as e:
        assert type(e) == MissingTitleFromMetadataError
        assert e.args[0] == MISSING_TITLE_FROM_METADATA


def test_map_data_from_request_call_with_no_artists():
    sample_response_data_copy = sample_response_data.copy()
    sample_response_data_copy.pop('artists')

    # Check if the artists are set to an empty list in the mapped response
    mapped_response = map_data_from_request_call(MockResponse(sample_response_data_copy))
    expected_response = MetadataResponse(title='Sample Title', artists=None, album=None, genre=None, date=None,
                                         duration=None,
                                         failed_tags=None)
    assert mapped_response == expected_response
