from sqlalchemy.orm import Session

from src.api.myapi.metadata_model import MetadataResponse
from src.database.musicDB.db_models import Album, File, Genre, Song, Artist, SongArtist


def add_file_and_metadata(db: Session, file, metadata: MetadataResponse):
    album = Album(ALBUM_NAME=metadata.album)
    file = File(FILE_DATA=file, FILE_TYPE='mp3')
    genre = Genre(GENRE_NAME=metadata.genre)
    song = Song(
        DURATION=metadata.duration,
        TITLE=metadata.title,
        RELEASE_DATE=metadata.date,
        file=file,
        album=album,
        genre=genre
    )

    for artist_name in metadata.artists:
        artist = Artist(ARTIST_NAME=artist_name)
        song_artist = SongArtist(song=song, artist=artist)
        song.artist.append(song_artist)

    db.add(song)
    db.flush()
