import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime


from data import db, User, Movies, UsersFavoriteMovie
from data import DataManager
from api import get_info_from_api


#Initialize Flask app
app = Flask(__name__)
#Secret key for flash
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
#Define base dir for app and URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir,
                                                    'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database with Flask
db.init_app(app)
#Create an object of Datamanager
data_manager = DataManager()


@app.route('/', methods=['GET'])
def home():
    """
    The home page of the application.
    Shows a list of all registered users and a form for adding new users.
    """
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """
    When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database,
    then redirects back to /
    """
    user = request.form.get('create_user')
    message = data_manager.create_user(user)
    flash(message)

    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def favorite_movies_of_user(user_id):
    """
    When you click on a user name,
    the app retrieves that user’s list of favorite movies and displays it.
    """
    user = db.session.get(User, user_id)
    favorite_movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=favorite_movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_favorite(user_id):
    """
    Add a new movie to a user’s list of favorite movies.
    """
    movie_title = request.form.get('add_movie')
    movie_info = get_info_from_api(movie_title)

    if movie_info.get("Response") == "False":
        message = "Your movie could not be found. Please try again"
        flash(message)
        return redirect(url_for('favorite_movies_of_user', user_id=user_id))

    title = movie_info.get('Title')
    poster = movie_info.get('Poster')
    release_date = datetime.strptime(movie_info.get('Released'), '%d %b %Y')
    director = movie_info.get('Director')

    movie = data_manager.create_movie(title, poster, director, release_date)
    data_manager.add_movie_to_user(user_id, movie)

    return redirect(url_for('favorite_movies_of_user', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def change_movie_title(user_id, movie_id):
    """
    Modify the title of a specific movie in a user’s list
    """
    new_title = request.form.get("change_title")
    message = data_manager.update_movie(movie_id, new_title)
    flash(message)

    return redirect(url_for('favorite_movies_of_user', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def remove_movie_from_users_list(user_id, movie_id):
    """
    Remove a specific movie from a user’s favorite movie list.
    """
    pass


if __name__ == "__main__":
    # Done once to create database, comment out after
    #with app.app_context():
        #db.create_all()

    app.run(host="0.0.0.0", port=5000)
