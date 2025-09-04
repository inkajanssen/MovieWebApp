from flask import Flask
from flask.cli import load_dotenv
import os

from data import db, User, Movies, UsersFavoriteMovie
from data import DataManager

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

@app.route('/', method=['GET'])
def home():
    """
    TODO
    The home page of the application.
    Shows a list of all registered users and a form for adding new users.
    """
    return "Welcome to MoviWeb App!"


@app.route('/users', method=['GET', 'POST'])
def list_users():
    """
    TODO
    When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database,
    then redirects back to /
    """
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def favorite_movies_of_user(user_id):
    """
    TODO
    When you click on a user name,
    the app retrieves that user’s list of favorite movies and displays it.
    """
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_favorite(user_id):
    """
    TODO
    Add a new movie to a user’s list of favorite movies.
    """
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def change_movie_title(user_id, movie_id):
    """
    Modify the title of a specific movie in a user’s list
    """
    pass


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
