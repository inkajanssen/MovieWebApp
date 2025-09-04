from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, ForeignKey

db = SQLAlchemy()

# Class for the User
class User(db.Model):
    """
    Class for a user with:
        A unique identifier (id)
        A name (name)
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return f"Username: {self.name}"

    def __repr__(self):
        return f"ID: {self.id}, name: {self.name}"

    favorite_movies = db.relationship("Movies",
                                      secondary= "favorite_movies",
                                      backref = "users",
                                      lazy= "dynamic")


# Class for Movies
class Movies(db.Model):
    """
    Class for Movies with:
        A unique identifier (id)
        The movie’s name (name)
        The movie’s director (director)
        The year of release (year)
        The url of the poster (poster_url)
    """
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    poster_url = db.Column(db.Text, nullable=False)

    def __str__(self):
        return (f"Movie:{self.name}, Director:{self.director or None}, "
                f"Released: {self.release_date or None}")

    def __repr__(self):
        return (f"ID: {self.id}, Movie:{self.name}, Director:{self.director or None},"
                f" Released: {self.release_date or None}, poster_url: {self.poster_url}")


# Class for joined Table between User and Movie
class UsersFavoriteMovie(db.Model):
    """
    A Join Table between User and Movie
    to establish which User likes which Movies
    user_id Foreign Key from User
    movie_id Foreign Key from Movies
    """
    __tablename__ = "favorite_movies"
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = db.Column(db.Integer, ForeignKey('movies.id'), primary_key=True)

    def __repr__(self):
        return f"User: {self.user_id}, Movie: {self.movie_id}"
