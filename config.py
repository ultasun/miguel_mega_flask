import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # CSRF protection key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'good-luck-guessing-it'

    # database options
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # application options (or "knobs")
    POSTS_PER_PAGE = 3

    # email logging options
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # automatic language feature options
    LANGUAGES = ['en', 'es']

    # LibreTranslate options
    # https://github.com/LibreTranslate/LibreTranslate#mirrors
    LIBRETRANSLATE_MIRROR = os.environ.get('LIBRETRANSLATE_MIRROR')
    # Not all LibreTranslate mirrors require an API key
    LIBRETRANSLATE_API_KEY = os.environ.get('LIBRETRANSLATE_API_KEY')

