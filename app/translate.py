import json
import requests 
from flask import current_app
from flask_babel import _

def translate(text, source_language, dest_language):
    """
    Uses a LibreTranslate mirror to perform translations.

    The LIBRETRANSLATE_MIRROR configuration option must be set.
    The LIBRETRANSLATE_API_KEY is applicable if using a mirror requiring a key.

    If source_language is not specified, it will be filled with 'auto', because
    the LibreTranslate engine can automatically detect the source language.

    See https://github.com/LibreTranslate/LibreTranslate#mirrors
    """
    if 'LIBRETRANSLATE_MIRROR' not in current_app.config or \
        not current_app.config['LIBRETRANSLATE_MIRROR']:
        current_app.logger.error( \
            'No LibreTranslate mirror is set! Check README.md')
        return _('Error: failed to contact the external translation service.')

    if source_language is None or not source_language:
        source_language = 'auto'

    requestDict = {}
    requestDict['q'] = text
    requestDict['source'] = source_language
    requestDict['target'] = dest_language

    if 'LIBRETRANSLATE_API_KEY' in current_app.config and \
        current_app.config['LIBRETRANSLATE_API_KEY']:
        requestDict['api_key'] = current_app.config['LIBRETRANSLATE_API_KEY']

    r = requests.post( \
        'https://' + current_app.config['LIBRETRANSLATE_MIRROR'] + '/translate',
        json=requestDict)

    if r.status_code == 403:
        current_app.logger.error( \
        'The LibreTranslate mirror wants an API key.  ' \
        + 'Either purchase an API key and set it in .flaskenv, or use a ' \
        + 'different LibreTranslate mirror.')
    if r.status_code == 400:
        current_app.logger.error('The text to translate had confused the ' \
        + 'LibreTranslate service.')
    if r.status_code != 200:
        current_app.logger.error( \
        'Error ' + str(r.status_code) + ' when utilizing ' \
        + 'the LibreTranslation service.')
        return _('Error: failed to contact the external translation service.')

    return r.json()['translatedText']

