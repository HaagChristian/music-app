from unittest.mock import MagicMock, patch

from src.database.musicDB.db_models import Song, Artist, Album, Genre
from src.database.musicDB.db_search import fetch_all_search_criteria

# data for testing
mock_titles = [('Song 1',), ('Song 2/Song 3',)]
mock_artist_names = [('Artist 1',), ('Artist 2/Artist 3',)]
mock_album_names = [('Album 1',), ('Album 2/Album 3',)]
mock_genre_names = [('Genre 1',), ('Genre 2/Genre 3',)]


@patch('src.database.musicDB.db_search.Song')
def test_fetch_all_search_criteria_title(mock_song):
    mock_session = MagicMock()
    mock_session.query(Song).distinct().all.return_value = mock_titles

    criteria_dict = fetch_all_search_criteria(mock_session)

    assert 'title' in criteria_dict
    assert criteria_dict['title'] == ['Song 1', 'Song 2', 'Song 3']


@patch('src.database.musicDB.db_search.Artist')
def test_fetch_all_search_criteria_interpret(mock_artist):
    mock_session = MagicMock()
    mock_session.query(Artist).distinct().all.return_value = mock_artist_names

    criteria_dict = fetch_all_search_criteria(mock_session)

    assert 'artist_name' in criteria_dict
    assert criteria_dict['artist_name'] == ['Artist 1', 'Artist 2', 'Artist 3']


@patch('src.database.musicDB.db_search.Genre')
def test_fetch_all_search_criteria_genre(mock_genre):
    mock_session = MagicMock()
    mock_session.query(Genre).distinct().all.return_value = mock_genre_names

    criteria_dict = fetch_all_search_criteria(mock_session)

    assert 'genre_name' in criteria_dict
    assert criteria_dict['genre_name'] == ['Genre 1', 'Genre 2', 'Genre 3']


@patch('src.database.musicDB.db_search.Album')
def test_fetch_all_search_criteria_album(mock_album):
    mock_session = MagicMock()
    mock_session.query(Album).distinct().all.return_value = mock_album_names

    criteria_dict = fetch_all_search_criteria(mock_session)

    assert 'genre_name' in criteria_dict
    assert criteria_dict['genre_name'] == ['Album 1', 'Album 2', 'Album 3']
