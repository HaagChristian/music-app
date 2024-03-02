"""This module contains the CRUD operations for the database."""

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.api.middleware.file_operations import create_and_return_file
from src.api.myapi.metadata_model import MetadataResponse, DBMetadata
from src.api.myapi.music_db_models import ConversionResponse
from src.database.music_db.db_models import Album, File, Genre, Song, Artist, SongArtist, ConvertedFile
from src.settings.error_messages import DB_NO_RESULT_FOUND


def add_file_and_metadata(db: Session, file, metadata: MetadataResponse, file_name: str):
    album = None
    if metadata.album:
        album = Album(ALBUM_NAME=metadata.album)

    file_data = File(FILE_DATA=file, FILE_TYPE='mp3', FILE_NAME=file_name)

    genre = None
    if metadata.genre:
        genre = db.query(Genre).filter(Genre.GENRE_NAME == metadata.genre).first()
        if not genre:
            genre = Genre(GENRE_NAME=metadata.genre)

    song = Song(
        DURATION=metadata.duration,
        TITLE=metadata.title,
        RELEASE_DATE=metadata.date,
        file=file_data,
        album=album,
        genre=genre
    )

    if metadata.artists:
        for artist_name in metadata.artists:
            artist = db.query(Artist).filter(Artist.ARTIST_NAME == artist_name.name).first()
            if not artist:  # artist does not exist in the database
                artist = Artist(ARTIST_NAME=artist_name.name)
                db.add(artist)
                db.flush()
            song_artist = SongArtist(song=song, artist=artist)
            db.add(song_artist)
            db.flush()

    db.add(song)
    db.flush()


def get_song_by_title(db: Session, metadata: MetadataResponse):
    return db.query(Song).filter(Song.TITLE == metadata.title).first()


def get_file_by_song_id(db: Session, song_id: int):
    return db.query(File).join(File.song).filter(Song.SONG_ID == song_id).first()


def get_file_by_id(db: Session, file_id: int):
    return db.query(File).filter(File.FILE_ID == file_id).first()


def is_converted_file_already_in_db(db: Session, file_name: str, file_type: str):
    return db.query(ConvertedFile).filter(
        and_(ConvertedFile.FILE_NAME == file_name, ConvertedFile.FILE_TYPE == file_type)).first()


def handle_conversion_response(response: ConversionResponse, original_file_id: int, file_name: str, db: Session):
    existing_file = is_converted_file_already_in_db(db, file_name, response.file_type)
    if existing_file:
        return create_and_return_file(existing_file)
    else:
        converted_file = ConvertedFile(
            ORIGINAL_FILE_ID=original_file_id,
            FILE_TYPE=response.file_type,
            FILE_DATA=response.file_data,
            FILE_NAME=file_name
        )
        db.add(converted_file)
        db.flush()
        return create_and_return_file(converted_file)


def update_file_and_metadata(db: Session, file, metadata: DBMetadata):
    if metadata.title:
        db.query(Song).filter(Song.SONG_ID == metadata.song_id).update({Song.TITLE: metadata.title})

    if metadata.genre:
        genre_res = db.query(Genre).filter(Genre.GENRE_NAME == metadata.genre).first()
        if not genre_res:  # genre does not exist in the database
            genre = Genre(GENRE_NAME=metadata.genre)
            db.add(genre)
            db.flush()
            db.query(Song).filter(Song.SONG_ID == metadata.song_id).update({Song.GENRE_ID: genre.GENRE_ID})
        else:
            db.query(Song).filter(Song.SONG_ID == metadata.song_id).update({Song.GENRE_ID: genre_res.GENRE_ID})

    if metadata.album:
        album_id = db.query(Song).filter(Song.SONG_ID == metadata.song_id).first().ALBUM_ID
        db.query(Album).filter(Album.ALBUM_ID == album_id).update({Album.ALBUM_NAME: metadata.album})

    if metadata.artists:
        # get all artists for the song
        artist_res = db.query(Artist). \
            join(SongArtist, Artist.ARTIST_ID == SongArtist.ARTIST_ID). \
            join(Song, Song.SONG_ID == SongArtist.SONG_ID). \
            filter(Song.SONG_ID == metadata.song_id).all()

        if not artist_res:  # song has no artists in the database
            for artist in metadata.artists:
                if_artist_not_in_db_add_to_db(db=db, artist_name=artist.name, song_id=metadata.song_id)
        else:
            for artist in metadata.artists:
                if artist.name not in [a.ARTIST_NAME for a in artist_res]:  # artist does not belong to the song
                    if_artist_not_in_db_add_to_db(db=db, artist_name=artist.name, song_id=metadata.song_id)

            for song_artist in artist_res:
                if song_artist.ARTIST_NAME not in [a.name for a in metadata.artists]:
                    # artist is attached to the song in the database, but was removed with the metadata change
                    # --> remove artist from song
                    db.query(SongArtist).filter(and_(SongArtist.SONG_ID == metadata.song_id,
                                                     SongArtist.ARTIST_ID == song_artist.ARTIST_ID)).delete()

    if metadata.date:
        db.query(Song).filter(Song.SONG_ID == metadata.song_id).update({Song.RELEASE_DATE: metadata.date})

    # update file data
    file_id = db.query(Song).filter(Song.SONG_ID == metadata.song_id).first().FILE_ID
    db.query(File).filter(File.FILE_ID == file_id).update({File.FILE_DATA: file})

    db.flush()


def is_artist_in_db(db: Session, artist_name: str):
    return db.query(Artist).filter(Artist.ARTIST_NAME == artist_name).first()


def if_artist_not_in_db_add_to_db(db: Session, artist_name: str, song_id: int):
    artist_in_db = is_artist_in_db(db, artist_name)
    if not artist_in_db:  # artist does not exist in the database
        artist = Artist(ARTIST_NAME=artist_name)
        db.add(artist)
        db.flush()
        song_artist = SongArtist(SONG_ID=song_id, ARTIST_ID=artist.ARTIST_ID)
        db.add(song_artist)
    else:
        song_artist = SongArtist(SONG_ID=song_id, ARTIST_ID=artist_in_db.ARTIST_ID)
        db.add(song_artist)
    db.flush()


def delete_song_and_file_by_song_id(db: Session, song_id: int):
    """
    delete a song with file
    """

    # get file_id
    song = db.query(Song).filter(Song.SONG_ID == song_id).first()
    if not song:
        raise NoResultFound(DB_NO_RESULT_FOUND)

    file_id = song.FILE_ID

    # delete referencing entries in `converted_file`
    db.query(ConvertedFile).filter(ConvertedFile.ORIGINAL_FILE_ID == file_id).delete(synchronize_session='fetch')

    # delete referencing entries in `song_artist`
    db.query(SongArtist).filter(SongArtist.SONG_ID == song_id).delete(synchronize_session='fetch')

    # delete song
    db.query(Song).filter(Song.SONG_ID == song_id).delete(synchronize_session='fetch')

    # delete file
    if db.query(Song).filter(Song.FILE_ID == file_id).count() == 0:
        db.query(File).filter(File.FILE_ID == file_id).delete(synchronize_session='fetch')

    db.commit()
    return True
