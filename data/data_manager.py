from .models import db, User, Movies, UsersFavoriteMovie

class DataManager:
    """
    Class to interact with a SQLite database.
    Implements all the basic CRUD methods.
    """

    def create_user(self, name):
        """
        Add a new user to your database.
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

        return "User sucessfully added to the database."


    def get_users(self):
        """
        Return a list of all users in your database.
        """
        users = User.query.order_by(User.name).all()
        if users:
            return users
        return []


    def get_movies(self, user_id):
        """
        Return a list of all movies of a specific user.
        """
        user = User.query.get(user_id)
        if user:
            return user.favorite_movies.all()
        return []


    def create_movie(self, name, poster_url, director=None, release_date=None):
        """
        Checks if a movie already exists
        If not:
        Adds a movie to the database
        """
        movie = Movies.query.filter_by(name=name).first()

        if movie is None:
            new_movie = Movies(name=name, poster_url=poster_url,
                           director=director, release_date=release_date)
            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        else:
            return movie


    def add_movie_to_user(self, user_id, movie):
        """
        Add a new movie to a user’s favorites.
        """
        user = db.session.get(User, user_id)
        new_movie = Movies.query.filter_by(name=movie.name).first()

        user.favorite_movies.append(new_movie)
        db.session.commit()

        return "Movie sucessfully added to the favorites."


    def update_movie(self, movie_id, new_title):
        """
        Update the details of a specific movie in the database.
        """
        movie_to_update = Movies.query.filter_by(id = movie_id).first()
        movie_to_update.name = new_title
        db.session.commit()

        return "Movie successfully updated"


    def delete_movie(self, user_id, movie_id):
        """
        Delete the movie from the user’s list of favorites.
        """
        user = User.query.get(user_id)
        movie_to_remove = Movies.query.get(movie_id)

        user.favorite_movies.remove(movie_to_remove)
        db.session.commit()

        return "Movie sucessfully removed from favorites"