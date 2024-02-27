from src.api.myapi.metadata_model import Artist, MetadataToChangeRequest, MetadataId3Input
from src.service.mapping.map_db_data import input_mapping_from_change_metadata


def test_input_mapping_from_change_metadata_with_artists():
    artists = [Artist(name="Artist 1"), Artist(name="Artist 2")]
    metadata_to_change = MetadataToChangeRequest(artists=artists, genre="Genre", album="Album", title="Title",
                                                 date=2000, song_id=123)

    mapped_input: MetadataId3Input = input_mapping_from_change_metadata(metadata_to_change)

    assert mapped_input.artists == "Artist 1;Artist 2"
    assert mapped_input.genre == "Genre"
    assert mapped_input.album == "Album"
    assert mapped_input.title == "Title"
    assert mapped_input.date == 2000


def test_input_mapping_from_change_metadata_with_one_artist():
    artists = [Artist(name="Artist 1")]
    metadata_to_change = MetadataToChangeRequest(artists=artists, genre="Genre", album="Album", title="Title",
                                                 date=2000, song_id=123)

    mapped_input: MetadataId3Input = input_mapping_from_change_metadata(metadata_to_change)

    assert mapped_input.artists == "Artist 1"
    assert mapped_input.genre == "Genre"
    assert mapped_input.album == "Album"
    assert mapped_input.title == "Title"
    assert mapped_input.date == 2000


def test_input_mapping_from_change_metadata_without_artists():
    metadata_to_change = MetadataToChangeRequest(genre="Genre", album="Album", title="Title", date=2000, song_id=123)

    mapped_input: MetadataId3Input = input_mapping_from_change_metadata(metadata_to_change)

    assert mapped_input.artists is None
    assert mapped_input.genre == "Genre"
    assert mapped_input.album == "Album"
    assert mapped_input.title == "Title"
    assert mapped_input.date == 2000


def test_input_mapping_from_change_metadata_with_empty_artists():
    metadata_to_change = MetadataToChangeRequest(artists=[], genre="Genre", album="Album", title="Title", date=2000,
                                                 song_id=123)

    mapped_input: MetadataId3Input = input_mapping_from_change_metadata(metadata_to_change)

    assert mapped_input.artists is None
    assert mapped_input.genre == "Genre"
    assert mapped_input.album == "Album"
    assert mapped_input.title == "Title"
    assert mapped_input.date == 2000


def test_input_mapping_from_change_metadata_with_none_values():
    metadata_to_change = MetadataToChangeRequest(artists=None, genre=None, album=None, title=None, date=None,
                                                 song_id=123)

    mapped_input: MetadataId3Input = input_mapping_from_change_metadata(metadata_to_change)

    assert mapped_input.artists is None
    assert mapped_input.genre is None
    assert mapped_input.album is None
    assert mapped_input.title is None
    assert mapped_input.date is None
