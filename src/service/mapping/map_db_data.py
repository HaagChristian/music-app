from typing import List

from src.api.myapi.metadata_model import MetadataFromSearch, Artist, MetadataToChange, MetadataId3Input
from src.api.myapi.music_db_models import FileDetailModel, SongWithRelationsAndFile, Album, Genre, File, \
    SongWithRelations
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


def input_mapping_from_change_metadata(metadata_to_change: MetadataToChange) -> MetadataId3Input:
    """
    Change metadata model for input model of id3 service
    """
    if metadata_to_change.artists:
        artist_names = [artist.name for artist in metadata_to_change.artists]
        artist_str = ';'.join(artist_names)
    else:
        artist_str = None
    date_string = metadata_to_change.date.strftime("%Y-%m-%d") if metadata_to_change.date else None
    data_for_id3 = MetadataId3Input(genre=metadata_to_change.genre, album=metadata_to_change.album,
                                    title=metadata_to_change.title, artists=artist_str, date=date_string)

    return data_for_id3


def file_obj_to_model(file_obj):
    """Converts SQLAlchemy file object to FileDetailModel."""
    song = file_obj.song
    album = song.album if song.album else None
    genre = song.genre if song.genre else None
    artists = [Artist(artist_id=artist.ARTIST_ID, artist_name=artist.ARTIST_NAME) for artist in song.artists]

    song_model = SongWithRelations(
        song_id=song.SONG_ID,
        song_title=song.TITLE,
        duration=song.DURATION,
        file_path=file_obj.FILE_NAME,
        bit_rate=song.BIT_RATE,
        sample_rate=song.SAMPLE_RATE,
        release_date=song.RELEASE_DATE.strftime("%Y-%m-%d") if song.RELEASE_DATE else None,
        album=Album(album_id=album.ALBUM_ID, album_name=album.ALBUM_NAME) if album else None,
        genre=Genre(genre_id=genre.GENRE_ID, genre_name=genre.GENRE_NAME) if genre else None,
        artists=artists
    )

    file_model = File(
        file_id=file_obj.FILE_ID,
        file_type=file_obj.FILE_TYPE,
        file_name=file_obj.FILE_NAME
    )

    return FileDetailModel(song=song_model, **file_model.dict())


def song_obj_to_model(song_obj):
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
    ) for artist in song_obj.artists]

    return SongWithRelations(
        song_id=song_obj.SONG_ID,
        title=song_obj.TITLE,
        duration=song_obj.DURATION,
        release_date=song_obj.RELEASE_DATE.strftime("%Y-%m-%d") if song_obj.RELEASE_DATE else None,
        album=album_model,
        genre=genre_model,
        artists=artists_model
    )


def song_and_file_obj_to_model(song_obj):
    """Converts SQLAlchemy song object to SongWithRelationsAndFile."""
    album = song_obj.album if song_obj.album else None
    genre = song_obj.genre if song_obj.genre else None
    artists = [Artist(artist_id=artist.ARTIST_ID, artist_name=artist.ARTIST_NAME) for artist in song_obj.artists]
    file_obj = song_obj.file if song_obj.file else None

    file_model = File(
        file_id=file_obj.FILE_ID,
        file_type=file_obj.FILE_TYPE,
        file_name=file_obj.FILE_NAME
    ) if file_obj else None

    return SongWithRelationsAndFile(
        song_id=song_obj.SONG_ID,
        song_title=song_obj.TITLE,
        duration=song_obj.DURATION,
        release_date=song_obj.RELEASE_DATE.strftime("%Y-%m-%d") if song_obj.RELEASE_DATE else None,
        album=Album(album_id=album.ALBUM_ID, album_name=album.ALBUM_NAME) if album else None,
        genre=Genre(genre_id=genre.GENRE_ID, genre_name=genre.GENRE_NAME) if genre else None,
        artists=artists,
        file=file_model
    )

