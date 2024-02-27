from typing import List

from src.api.myapi.metadata_model import MetadataFromSearch, Artist, MetadataToChangeRequest, MetadataId3Input
from src.api.myapi.music_db_models import SongWithRelationsAndFile, Album, Genre, File, SongWithRelations, SimpleSong
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

def map_album_to_model(album_obj):
    if album_obj:
        return Album(
            album_id=album_obj.ALBUM_ID,
            album_name=album_obj.ALBUM_NAME
        )
    return None

def map_genre_to_model(genre_obj):
    return Genre(
        genre_id=genre_obj.GENRE_ID,
        genre_name=genre_obj.GENRE_NAME
    ) if genre_obj else None

def map_file_to_model(file_obj):
    return File(
        file_id=file_obj.FILE_ID,
        file_data=file_obj.FILE_DATA,
        file_type=file_obj.FILE_TYPE,
        file_name=file_obj.FILE_NAME
        ) if file_obj else None

def map_artist_to_model(artist_obj):
    return Artist(
        artist_id=artist_obj.ARTIST_ID,
        artist_name=artist_obj.ARTIST_NAME
    ) if artist_obj else None


def map_simple_song_to_model(song_obj):
    return SimpleSong(
        song_id=song_obj.SONG_ID,
        title=song_obj.TITLE,
        duration=song_obj.DURATION,
        release_date=str(song_obj.RELEASE_DATE) if song_obj.RELEASE_DATE else None
    ) if song_obj else None


def map_song_with_rel_to_model(song_obj):
    """Converts SQLAlchemy song object to SongWithRelations model."""
    album_model = Album(
        album_id=song_obj.album.ALBUM_ID,
        album_name=song_obj.album.ALBUM_NAME
    ) if song_obj.album else None

    genre_model = Genre(
        genre_id=song_obj.genre.GENRE_ID,
        genre_name=song_obj.genre.GENRE_NAME
    ) if song_obj.genre else None

    artists_model = [Artist(
        artist_id=artist.ARTIST_ID,
        artist_name=artist.ARTIST_NAME
    ) for artist in song_obj.artist]

    return SongWithRelations(
        song_id=song_obj.SONG_ID,
        title=song_obj.TITLE,
        duration=song_obj.DURATION,
        release_date=str(song_obj.RELEASE_DATE) if song_obj.RELEASE_DATE else None,
        album=album_model,
        genre=genre_model,
        artist=artists_model
    )


def map_song_with_rel_and_file_to_model(song_obj):
    """Converts SQLAlchemy song object to SongWithRelationsAndFile."""

    file_model = File(
        file_id=song_obj.file.FILE_ID,
        file_data=song_obj.file.FILE_DATA,
        file_type=song_obj.file.FILE_TYPE,
        file_name=song_obj.file.FILE_NAME
    ) if song_obj.file else None

    song_with_rel = map_song_with_rel_to_model(song_obj)
    return SongWithRelationsAndFile(**song_with_rel.dict(), file=file_model)

