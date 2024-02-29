from typing import List

from src.api.myapi.metadata_model import MetadataFromSearch, MetadataToChangeRequest, MetadataId3Input
from src.api.myapi.music_db_models import SongWithRelations, Artist, ArtistBase
from src.database.musicDB.db_models import Song


def map_search_db_data(db_result: List[Song]) -> List[MetadataFromSearch]:
    mapped_output_data: List[MetadataFromSearch] = []

    for song in db_result:
        artists = [Artist(artist_name=artist.artist.ARTIST_NAME) for artist in (song.artist or [])]
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


def input_mapping_from_change_metadata(metadata_to_change: MetadataToChangeRequest) -> MetadataId3Input:
    """
    Change metadata model for input model of id3 service
    """
    if metadata_to_change.artists:
        artist_names = [artist.name for artist in metadata_to_change.artists]
        artist_str = ';'.join(artist_names)
    else:
        artist_str = None

    return MetadataId3Input(genre=metadata_to_change.genre, album=metadata_to_change.album,
                            title=metadata_to_change.title, artists=artist_str, date=metadata_to_change.date)


def map_song_with_rel_to_model(song_obj):
    """
    Converts SQLAlchemy song object to SongWithRelations model.
    """

    artists = [ArtistBase(artist_name=artist.artist.ARTIST_NAME) for artist in (song_obj.artist or [])]

    album_name = song_obj.album.ALBUM_NAME if song_obj.album else None
    genre_name = song_obj.genre.GENRE_NAME if song_obj.genre else None
    return SongWithRelations(
        song_id=song_obj.SONG_ID,
        title=song_obj.TITLE,
        duration=song_obj.DURATION,
        release_date=song_obj.RELEASE_DATE.year if song_obj.RELEASE_DATE else None,
        album=album_name,
        genre=genre_name,
        artist=artists,
        file_id=song_obj.file.FILE_ID
    )

