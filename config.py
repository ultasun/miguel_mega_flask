import os
from dotenv import load_dotenv 

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # CSRF protection key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'good-luck-guessing-it'

    # database options
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # application options (or "knobs")
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE') or 33)

    # email logging options
    # TODO the usage of MAIL_USE_TLS is confusing, see README.md.
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # who to send error emails to
    ADMINS = os.environ.get('ADMINS')
    if ADMINS:
        ADMINS = ADMINS.split(',')
    else:
        ADMINS = ['nobody@nowhere.com']

    # system content language options
    # TODO this should be automatically detected based on the directories which
    # are found in app/translations plus 'en'. 
    LANGUAGES = os.environ.get('LANGUAGES')
    if LANGUAGES:
        LANGUAGES = LANGUAGES.split(',')
    else:
        LANGUAGES = ['en', 'es']

    # user content language options
    # LibreTranslate options
    # https://github.com/LibreTranslate/LibreTranslate#mirrors
    LIBRETRANSLATE_MIRROR = os.environ.get('LIBRETRANSLATE_MIRROR') or \
        "lt.vern.cc"
    # Not all LibreTranslate mirrors require an API key
    LIBRETRANSLATE_API_KEY = os.environ.get('LIBRETRANSLATE_API_KEY')

