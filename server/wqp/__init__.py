import logging
import json
import os
import sys

from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFProtect
from requests import Session
from whitenoise import WhiteNoise


__version__ = '6.7.0dev'


def _create_log_handler(log_dir=None, log_name=__name__):
    """
    Create a handler object. The logs will be streamed
    to stdout if a logfile is not specified using a StreamHandler.
    If a logfile is specified, a handler will be created so logs
    will be written to the file.

    :param str log_dir: optional path of a directory where logs can be written to
    :return: a handler
    :rtype: logging.Handler

    """
    if log_dir is not None:
        log_file = '{}.log'.format(log_name)
        log_path = os.path.join(log_dir, log_file)
        log_handler = logging.FileHandler(log_path)
    else:
        log_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - {%(pathname)s:L%(lineno)d} - %(message)s')
    log_handler.setFormatter(formatter)
    return log_handler


app = Flask(__name__.split()[0], instance_relative_config='NO_INSTANCE_CONFIG' not in os.environ)

# Loads configuration information from config.py and instance/config.py
app.config.from_object('config')
if 'NO_INSTANCE_CONFIG' not in os.environ:
    app.config.from_pyfile('config.py')

if app.config.get('LOGGING_ENABLED'):
    log_directory = app.config.get('LOGGING_DIRECTORY')
    loglevel = app.config.get('LOGGING_LEVEL')
    handler = _create_log_handler(log_directory)
    # Do not set logging level in the handler.
    # Otherwise, if Flask's DEBUG is set to False,
    # all logging will be disabled.
    # Instead, set the level in the logger object.
    app.logger.setLevel(loglevel)
    app.logger.addHandler(handler)

csrf = CSRFProtect(app)


@app.before_request
def log_before():
    url = request.path
    method = request.method
    app.logger.debug('Request of type %s made to %s', method, url)


@app.after_request
def log_after(response):
    resp_status = response.status
    resp_headers = response.headers
    app.logger.debug('Response: %s, %s', resp_status, resp_headers)
    return response


session = Session()
session.verify = app.config['VERIFY_CERT']


# Load static assets manifest file, which maps source file names to the
# corresponding versioned/hashed file name.
_manifest_path = app.config.get('ASSET_MANIFEST_PATH')
if _manifest_path:
    with open(_manifest_path, 'r') as f:
        app.config['ASSET_MANIFEST'] = json.loads(f.read())


from .portal_ui_blueprint.views import portal_ui  # pylint: disable=C0413
from .wqx.views import wqx  # pylint: disable=C0413
from . import filters  # pylint: disable=C0413

app.register_blueprint(portal_ui, url_prefix='/')
app.register_blueprint(wqx, url_prefix='/portal/schemas')

if os.getenv('CONTAINER_RUN'):
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='/assets', prefix=app.config.get('STATIC_ROOT'))
else:
    app.wsgi_app = \
        WhiteNoise(app.wsgi_app,
                   root=os.path.join(os.path.dirname(app.config.get('PROJECT_HOME')), 'assets', 'dist', ''),
                   autorefresh=True,
                   prefix=app.config.get('STATIC_ROOT'))


