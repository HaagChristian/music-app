from unittest.mock import MagicMock

from src.service.mapping.map_db_data import map_song_with_rel_to_model


mock_artist_1 = MagicMock(ARTIST_NAME="Markus Nowak", ARTIST_ID=1)
mock_song_artist_1 = MagicMock(artist=mock_artist_1)
mock_artist_2 = MagicMock(ARTIST_NAME="Another Artist", ARTIST_ID=2)
mock_song_artist_2 = MagicMock(artist=mock_artist_2)
mock_album = MagicMock(ALBUM_NAME="Markus Nowak", ALBUM_ID=1)
mock_genre = MagicMock(GENRE_NAME="Pop", GENRE_ID=1)

# song mocks
song_mock1 = MagicMock(
    FILE_ID=1,
    DURATION=291.2914375,
    TITLE="Ich war noch niemals in New York",
    SONG_ID=1,
    RELEASE_DATE=2021,
    artist=[mock_song_artist_1],
    album=mock_album,
    genre=mock_genre,
    file=MagicMock(FILE_ID=1)
)

song_mock2 = MagicMock(
    FILE_ID=2,
    DURATION=291.2914375,
    TITLE="Another Song",
    SONG_ID=2,
    RELEASE_DATE=2021,
    artist=[mock_song_artist_1, mock_song_artist_2],
    album=mock_album,
    genre=mock_genre,
    file=MagicMock(FILE_ID=2)
)

song_mock3 = MagicMock(
    FILE_ID=3,
    DURATION=None,
    TITLE=None,
    SONG_ID=3,
    RELEASE_DATE=None,
    artist=[],
    album=None,
    genre=None,
    file=MagicMock(FILE_ID=3)
)


def test_map_song_with_rel_one_artist_to_model():
    model = map_song_with_rel_to_model(song_mock1)
    assert model.song_id == 1
    assert model.title == "Ich war noch niemals in New York"
    assert model.duration == 291.2914375
    assert model.release_date == 2021
    assert model.album == "Markus Nowak"
    assert model.genre == "Pop"
    assert model.artists[0].name == "Markus Nowak"
    assert model.artists[0].artist_id == 1
    assert model.file_id == 1


def test_map_song_with_rel_two_artists_to_model():
    model = map_song_with_rel_to_model(song_mock2)
    assert model.song_id == 2
    assert model.title == "Another Song"
    assert model.duration == 291.2914375
    assert model.release_date == 2021
    assert model.album == "Markus Nowak"
    assert model.genre == "Pop"
    assert model.artists[0].name == "Markus Nowak"
    assert model.artists[0].artist_id == 1
    assert model.artists[1].name == "Another Artist"
    assert model.artists[1].artist_id == 2
    assert model.file_id == 2


def test_map_song_with_rel_none_types_to_model():
    model = map_song_with_rel_to_model(song_mock3)
    assert model.song_id == 3
    assert model.title == None
    assert model.duration == None
    assert model.release_date == None
    assert model.album == None
    assert model.genre == None
    assert model.artists == []
    assert model.file_id == 3

