"""This module contains the CRUD operations for the database."""

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from src.api.myapi.metadata_model import MetadataResponse, DBMetadata
from src.database.musicDB.db_models import Album, File, Genre, Song, Artist, SongArtist, ConvertedFile


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
            if not artist:
                # Wenn der Künstler nicht gefunden wird, erstellen Sie einen neuen Künstler
                artist = Artist(ARTIST_NAME=artist_name.name)
                db.add(artist)
                db.flush()  # Fügen Sie den neuen Künstler zur Datenbank hinzu
            song_artist = SongArtist(song=song, artist=artist)
            song.artist.append(song_artist)

    db.add(song)  # Fügen Sie den Song zur Datenbank hinzu
    db.flush()


def add_converted_file(db: Session, original_file_id: int, file_data: bytes, file_type: str) -> ConvertedFile:
    converted_file = ConvertedFile(
        ORIGINAL_FILE_ID=original_file_id,
        FILE_DATA=file_data,
        FILE_TYPE=file_type
    )
    db.add(converted_file)
    db.commit()
    db.refresh(converted_file)
    return converted_file


def get_file_by_song_id(db: Session, song_id: int):
    return db.query(File).join(File.song).filter(Song.SONG_ID == song_id).first()


def get_song_and_file_by_song_id(db: Session, song_id: int):
    return db.query(Song).filter(Song.SONG_ID == song_id). \
        options(
        joinedload(Song.file),
        joinedload(Song.album),
        joinedload(Song.genre),
        joinedload(Song.artists)
    ).first()


def get_file_by_id(db: Session, file_id: int):
    return db.query(File).filter(File.FILE_ID == file_id).first()


def get_file_by_song_id(db: Session, song_id: int):
    return db.query(File).join(Song).filter(Song.SONG_ID == song_id).first()


def get_song_by_id(db: Session, song_id: int):
    return db.query(Song).filter(Song.SONG_ID == song_id).first()


def update_file_and_metadata(db: Session, file, metadata: DBMetadata):
    if metadata.title:
        db.query(Song).filter(Song.SONG_ID == metadata.song_id).update({Song.TITLE: metadata.title})
    if metadata.genre:
        genre_res = db.query(Genre).filter(Genre.GENRE_NAME == metadata.genre).first()
        if not genre_res:
            # genre does not exist in the database
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
            filter(Song.SONG_ID == metadata.song_id). \
            all()

        if not artist_res:  # song has no artists
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


"""Delete a song and its file from the database by song id."""


def delete_song_and_file_by_id(db: Session, song_id: int):
    song = db.query(Song).filter(Song.SONG_ID == song_id).first()
    if not song:
        return False

    file_id = song.FILE_ID

    if file_id:
        db.query(File).filter(File.FILE_ID == file_id).delete()

    db.query(Song).filter(Song.SONG_ID == song_id).delete()

    db.commit()

    return True
