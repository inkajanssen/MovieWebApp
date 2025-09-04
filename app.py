from flask import Flask
from flask.cli import load_dotenv
import os

from data import db, User, Movies, UsersFavoriteMovie

#Initialize Flask app
app = Flask(__name__)
#Secret key for flash
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
#Define base dir for app and URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir,
                                                    'data/library.sqlite')}"
# Initialize database with Flask
db.init_app(app)

if __name__ == "__main__":
    # Done once to create database, comment out after
    # with app.app_context():
        #db.create_all()

    app.run(host="0.0.0.0", port=5000)
