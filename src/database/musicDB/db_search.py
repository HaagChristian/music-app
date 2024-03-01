from sqlalchemy.orm import Session, joinedload

from src.database.musicDB.db_models import Song, Artist, Album, Genre, SongArtist


def fetch_all_search_criteria(db: Session):
    criteria_dict = {}

    titles = db.query(Song.TITLE).distinct().all()
    titles_list = [item for title in titles for item in title[0].split("/")]
    if titles_list:
        criteria_dict["title"] = titles_list

    artists = db.query(Artist.ARTIST_NAME).distinct().all()
    artists_list = [item for artist in artists for item in artist[0].split("/")]
    if artists_list:
        criteria_dict["interpret"] = artists_list

    albums = db.query(Album.ALBUM_NAME).distinct().all()
    albums_list = [item for album in albums for item in album[0].split("/")]
    if albums_list:
        criteria_dict["album"] = albums_list

    genres = db.query(Genre.GENRE_NAME).distinct().all()
    genres_list = [item for genre in genres for item in genre[0].split("/")]
    if genres_list:
        criteria_dict["genre"] = genres_list

    return criteria_dict


def search_songs_combined(db: Session, title: str = None, genre_name: str = None, artist_name: str = None,
                          album_name: str = None):
    query = db.query(Song)

    if title:
        query = query.filter(Song.TITLE.like(f'%{title}%'))
    if genre_name:
        query = query.join(Song.genre).filter(Genre.GENRE_NAME.like(f'%{genre_name}%'))
    if artist_name:
        query = query.join(SongArtist).join(Artist).filter(Artist.ARTIST_NAME.like(f'%{artist_name}%'))
    if album_name:
        query = query.join(Song.album).filter(Album.ALBUM_NAME.like(f'%{album_name}%'))

    return query.options(
        joinedload(Song.album),
        joinedload(Song.genre),
        joinedload(Song.artist)
    ).all()
