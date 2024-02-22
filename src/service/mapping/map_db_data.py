from typing import List

from src.api.myapi.metadata_model import MetadataFromSearch, Artist
from src.database.musicDB.db_models import Song


def map_search_db_data(db_result: List[Song]) -> List[MetadataFromSearch]:
    mapped_output_data: List[MetadataFromSearch] = []

    for song in db_result:
        artists = [Artist(name=artist.artist.ARTIST_NAME) for artist in (song.artist or [])]
        album_name = song.album.ALBUM_NAME if song.album else None
        genre_name = song.genre.GENRE_NAME if song.genre else None
        release_date = str(song.RELEASE_DATE) if song.RELEASE_DATE else None
        duration = song.DURATION if song.DURATION else None

        metadata = MetadataFromSearch(
            title=song.TITLE,
            artists=artists,
            album=album_name,
            genre=genre_name,
            date=release_date,
            duration=duration,
            file_id=song.FILE_ID
        )
        mapped_output_data.append(metadata)

    return mapped_output_data
