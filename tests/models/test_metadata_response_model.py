from datetime import datetime

from src.api.myapi.metadata_model import MetadataResponse
from src.settings.error_messages import INVALID_YEAR


def test_metadata_response_with_valid_date():
    response = MetadataResponse(title="Sample Title", date=2000)
    assert response.date == 2000
    assert response.title == "Sample Title"


def test_metadata_response_with_impossible_year():
    try:
        MetadataResponse(title="Sample Title", date=999)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert INVALID_YEAR in str(e)

    try:
        MetadataResponse(title="Sample Title", date=datetime.now().year + 1)
    except ValueError as e:
        pass
        assert INVALID_YEAR in str(e)


def test_metadata_response_with_invalid_year():
    try:
        MetadataResponse(title="Sample Title", date="invalid")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert INVALID_YEAR in str(e)


def test_metadata_response_with_no_date():
    response = MetadataResponse(title="Sample Title")
    assert response.date is None
