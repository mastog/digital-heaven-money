import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()# Load environment variables

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE_URL'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FILE_UPLOAD_DIR = os.path.join(os.path.dirname(basedir),"public", 'uploaded_Pic')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}