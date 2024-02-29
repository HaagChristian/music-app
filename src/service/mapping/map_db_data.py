from src.api.myapi.metadata_model import MetadataToChangeRequest, MetadataId3Input
from src.api.myapi.music_db_models import SongWithRelations, ArtistBase


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
    artists = []
    if song_obj.artist:
        for artist in song_obj.artist:
            artists.append(ArtistBase(name=artist.artist.ARTIST_NAME, id=artist.artist.ARTIST_ID))
    else:
        artists = []

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
