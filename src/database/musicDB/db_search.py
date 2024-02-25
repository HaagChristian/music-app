from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from src.database.musicDB.db_models import Song, Artist, Album, Genre


"""Search for songs in the database based on various criteria."""
# simple search returns only song objects
'''
def search_song_by_title(db: Session, title: str):
    return db.query(Song).filter(Song.TITLE.like(f"%{title}%")).all()


def search_songs_by_genre(db: Session, genre_name: str):
    return db.query(Song).join(Genre).filter(Genre.GENRE_NAME.like(f'%{genre_name}%')).all()


def search_songs_by_artist(db: Session, artist_name: str):
    return db.query(Song).join(Song.artist).join(Artist).filter(Artist.ARTIST_NAME.like(f'%{artist_name}%')).all()


def search_songs_by_album(db: Session, album_name: str):
    return db.query(Song).join(Album).filter(Album.ALBUM_NAME.like(f'%{album_name}%')).all()


def search_songs_combined(db: Session, title: str = None, genre_name: str = None, artist_name: str = None,
                          album_name: str = None):
    query = db.query(Song)

    if title:
        query = query.filter(Song.TITLE.like(f'%{title}%'))
    if genre_name:
        query = query.join(Song.genre).filter(Genre.GENRE_NAME.like(f'%{genre_name}%'))
    if artist_name:
        query = query.join(Song.artist).join(Artist).filter(Artist.ARTIST_NAME.like(f'%{artist_name}%'))
    if album_name:
        query = query.join(Song.album).filter(Album.ALBUM_NAME.like(f'%{album_name}%'))

    return query.all()
'''
# TODO: decide if we want to use the combined search or the simple search
"""Search for songs in the database based on various criteria."""
# combined search returns song objects with joined artist, album and genre
def search_song_by_title(db: Session, title: str):
    return db.query(Song).filter(Song.TITLE.like(f"%{title}%")) \
        .options(
            joinedload(Song.album),
            joinedload(Song.genre),
            joinedload(Song.artists)
        ).all()

def search_songs_by_genre(db: Session, genre_name: str):
    return db.query(Song).join(Genre).filter(Genre.GENRE_NAME.like(f'%{genre_name}%')) \
        .options(
            joinedload(Song.album),
            joinedload(Song.artists)
        ).all()

def search_songs_by_artist(db: Session, artist_name: str):
    return db.query(Song).join(Song.artists).join(Artist).filter(Artist.ARTIST_NAME.like(f'%{artist_name}%')) \
        .options(
            joinedload(Song.album),
            joinedload(Song.genre)
        ).all()

def search_songs_by_album(db: Session, album_name: str):
    return db.query(Song).join(Album).filter(Album.ALBUM_NAME.like(f'%{album_name}%')) \
        .options(
            joinedload(Song.genre),
            joinedload(Song.artists)
        ).all()

def search_songs_combined(db: Session, title: str = None, genre_name: str = None, artist_name: str = None,
                          album_name: str = None):
    query = db.query(Song)

    if title:
        query = query.filter(Song.TITLE.like(f'%{title}%'))
    if genre_name:
        query = query.join(Song.genre).filter(Genre.GENRE_NAME.like(f'%{genre_name}%'))
    if artist_name:
        query = query.join(Song.artists).join(Artist).filter(Artist.ARTIST_NAME.like(f'%{artist_name}%'))
    if album_name:
        query = query.join(Song.album).filter(Album.ALBUM_NAME.like(f'%{album_name}%'))

    return query.options(
            joinedload(Song.album),
            joinedload(Song.genre),
            joinedload(Song.artists)
        ).all()


"""Combined search for title and artist."""

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