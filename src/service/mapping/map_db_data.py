from typing import List

from src.api.myapi.metadata_model import MetadataFromSearch, Artist, MetadataToChange, MetadataId3Input
from src.api.myapi.music_db_models import FileDetailModel, SongDetailModel
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

    data_for_id3 = MetadataId3Input(genre=metadata_to_change.genre, album=metadata_to_change.album,
                                    title=metadata_to_change.title, artists=artist_str)

    return data_for_id3


def file_obj_to_model(file_obj):
    """converts SQLAlchemy file object to dictionary for the pydantic model."""
    file_detail_data = {
        "file_id": file_obj.FILE_ID,
        "file_type": file_obj.FILE_TYPE,
        "file_name": file_obj.FILE_NAME,
        "song": {
            "song_id": file_obj.song.SONG_ID,
            "song_title": file_obj.song.TITLE,
            "duration": file_obj.song.DURATION,
            "file_path": file_obj.song.file.FILE_NAME,
            "bit_rate": file_obj.song.BIT_RATE,
            "sample_rate": file_obj.song.SAMPLE_RATE,
            "release_date": file_obj.song.RELEASE_DATE.strftime("%Y-%m-%d") if file_obj.song.RELEASE_DATE else None,
            "album": {
                "album_id": file_obj.song.album.ALBUM_ID,
                "album_name": file_obj.song.album.ALBUM_NAME,
                "artist_id": file_obj.song.album.artist_id,
            },
            "genre": {
                "genre_id": file_obj.song.genre.GENRE_ID,
                "genre_name": file_obj.song.genre.GENRE_NAME,
            },
            "artists": [
                {"artist_id": artist.ARTIST_ID, "artist_name": artist.ARTIST_NAME} for artist in file_obj.song.artist
            ]
        }
    }
    return FileDetailModel(**file_detail_data)



def song_obj_to_model(song_obj):
    """converts SQLAlchemy song object to dictionary for the pydantic model."""
    artists_list = [{"artist_id": artist.artist_id, "artist_name": artist.artist_name} for artist in song_obj.artists]

    file_model = {
        "file_id": song_obj.file.FILE_ID,
        "file_type": song_obj.file.FILE_TYPE,
        "file_name": song_obj.file.FILE_NAME,
    }

    song_detail_data = {
        "song_id": song_obj.SONG_ID,
        "song_title": song_obj.TITLE,
        "duration": song_obj.DURATION,
        "file_path": song_obj.file.FILE_NAME,
        "bit_rate": song_obj.BIT_RATE,
        "sample_rate": song_obj.SAMPLE_RATE,
        "release_date": song_obj.RELEASE_DATE.strftime("%Y-%m-%d") if song_obj.RELEASE_DATE else None,
        "album": {
            "album_id": song_obj.album.ALBUM_ID,
            "album_name": song_obj.album.ALBUM_NAME,
            "artist_id": song_obj.album.artist_id,
        },
        "genre": {
            "genre_id": song_obj.genre.GENRE_ID,
            "genre_name": song_obj.genre.GENRE_NAME,
        },
        "artists": artists_list,
        "file": file_model,
    }

    return SongDetailModel(**song_detail_data)
