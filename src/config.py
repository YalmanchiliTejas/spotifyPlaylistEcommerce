import os
basedir = os.path.abspath(os.path.dirname(__file__)) # directory file is stored in

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'temp_secret_key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # set to False to disable a feature of Flask-SQLAlchemy that sends a signal to the application every time a change is about to be made in the database (not needed)
