from src.api.myapi.metadata_model import MetadataToChangeRequest, Artist
from src.settings.error_messages import MISSING_PARAMETER


def test_is_empty_with_all_fields_none():
    try:
        MetadataToChangeRequest()
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_is_empty_with_some_fields_not_none():
    metadata = MetadataToChangeRequest(genre="Genre", song_id=123)

    assert metadata.song_id == 123
    assert metadata.title is None
    assert metadata.album is None
    assert metadata.genre == "Genre"
    assert metadata.date is None
    assert metadata.artists is None


def test_is_empty_with_only_song_id():
    try:
        MetadataToChangeRequest(song_id=123)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert MISSING_PARAMETER in str(e)


def test_is_empty_with_only_artists():
    artists = [Artist(name="Artist 1"), Artist(name="Artist 2")]
    metadata = MetadataToChangeRequest(artists=artists, song_id=123)

    assert metadata.song_id == 123
    assert metadata.title is None
    assert metadata.album is None
    assert metadata.genre is None
    assert metadata.date is None
    assert metadata.artists == artists
