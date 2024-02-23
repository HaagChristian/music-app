from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from src.api.myapi.metadata_model import MetadataResponse, DBMetadata
from src.database.musicDB.db_models import Album, File, Genre, Song, Artist, SongArtist


def add_file_and_metadata(db: Session, file, metadata: MetadataResponse, file_name: str):
    album = Album(ALBUM_NAME=metadata.album)
    file = File(FILE_DATA=file, FILE_TYPE='mp3', FILE_NAME=file_name)

    genre_res = db.query(Genre).filter(Genre.GENRE_NAME == metadata.genre).first()
    if not genre_res:
        genre = Genre(GENRE_NAME=metadata.genre)
        song = Song(
            DURATION=metadata.duration,
            TITLE=metadata.title,
            RELEASE_DATE=metadata.date,
            file=file,
            album=album,
            genre=genre
        )
    else:
        song = Song(
            DURATION=metadata.duration,
            TITLE=metadata.title,
            RELEASE_DATE=metadata.date,
            file=file,
            album=album,
            GENRE_ID=genre_res.GENRE_ID
        )

    for artist_name in metadata.artists:
        artist_res = db.query(Artist).filter(Artist.ARTIST_NAME == artist_name.name).first()
        if not artist_res:
            artist = Artist(ARTIST_NAME=artist_name.name)
            song_artist = SongArtist(song=song, artist=artist)
            song.artist.append(song_artist)

    db.add(song)
    db.flush()


def search_for_title_and_artist(db: Session, title: str, artist: str):
    if title and artist:
        return db.query(Song).join(Song.artist).join(Song.album).filter(
            and_(
                Song.TITLE.like(title),
                Artist.ARTIST_NAME == artist
            )
        ).options(
            joinedload(Song.artist),
            joinedload(Song.album),
            joinedload(Song.genre)) \
            .all()
    elif title and not artist:
        return db.query(Song).join(Song.artist).join(Song.album).filter(Song.TITLE.like(title)).options(
            joinedload(Song.artist),
            joinedload(Song.album),
            joinedload(Song.genre)).all()
    else:
        # only artist
        return db.query(Song).join(Song.artist).join(Song.album).filter(Artist.ARTIST_NAME == artist).options(
            joinedload(Song.artist),
            joinedload(Song.album),
            joinedload(Song.genre)).all()


def get_file_by_id(db: Session, file_id: int):
    return db.query(File).filter(File.FILE_ID == file_id). \
        options(
        joinedload(File.song).joinedload(Song.album),
        joinedload(File.song).joinedload(Song.artist),
        joinedload(File.song).joinedload(Song.genre)
    ).first()


def update_file_and_metadata(db: Session, file, metadata: DBMetadata):
    if metadata.title:
        db.query(Song).filter(Song.FILE_ID == metadata.file_id).update({Song.TITLE: metadata.title})
    if metadata.genre:
        genre_res = db.query(Genre).filter(Genre.GENRE_NAME == metadata.genre).first()
        if not genre_res:
            genre = Genre(GENRE_NAME=metadata.genre)
            db.add(genre)
            db.flush()
            db.query(Song).filter(Song.FILE_ID == metadata.file_id).update({Song.GENRE_ID: genre.GENRE_ID})
        else:
            db.query(Song).filter(Song.FILE_ID == metadata.file_id).update({Song.GENRE_ID: genre_res.GENRE_ID})
    if metadata.album:
        # album_res = db.query(Album).filter(
        #     and_(Album.ALBUM_NAME == metadata.album, Song.FILE_ID == metadata.file_id)).first()
        # if not album_res:
        #     album = Album(ALBUM_NAME=metadata.album)
        #     db.add(album)
        #     db.flush()
        #
        #     db.query(Song).filter(Song.FILE_ID == metadata.file_id).update({Song.ALBUM_ID: album.ALBUM_ID})
        # else:
        song = db.query(Song).filter(Song.FILE_ID == metadata.file_id).first()
        db.query(Album).filter(Album.ALBUM_ID == Song.album.ALBUM_ID).update({Album.ALBUM_NAME: metadata.album})
    if metadata.artists:
        artist_names = metadata.artists.split(';')

    db.flush()
