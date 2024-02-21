from sqlalchemy.orm import Session

from src.database.musicDB.db_model_album import Album
from src.database.musicDB.db_model_artist import Artist
from src.database.musicDB.db_model_file import File
from src.database.musicDB.db_model_genre import Genre
from src.database.musicDB.db_model_song import Song


def add_file_and_metadata(db: Session, file, metadata):
    artist = Artist(ARTIST_NAME=metadata.artist)
    album = Album(ALBUM_NAME=metadata.album)
    file = File(FILE_DATA=file, FILE_TYPE='mp3')
    genre = Genre(GENRE_NAME=metadata.genre)
    song = Song(
        DURATION=metadata.duration,  # TODO Add
        TITLE=metadata.title,
        RELEASE_DATE=metadata.date,
        file=file,
        album=album,
        genre=genre,
        artist=artist
    )

    db.add(song)
    db.flush()
