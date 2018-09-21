import flask
import logging
import os
import traceback
import logging.config

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flasgger import Swagger
from werkzeug.exceptions import NotFound
from jinja2.exceptions import TemplateNotFound

from apis.hello import Hello

# Logging configs
logging.config.fileConfig('configs/logging.conf')

CONFIG_ENVVAR = 'FLASK_CONF'

app = Flask(__name__)
app.config.from_pyfile('configs/app.default.py')
if CONFIG_ENVVAR in os.environ.keys():
    app.config.from_envvar(CONFIG_ENVVAR, silent=True)
app.config.from_pyfile('configs/secret.py')

# Modifiers
CORS(app)
Swagger(app)

api = Api(app)
api.add_resource(Hello, '/hello')


@app.after_request
def after_request(response):
    """ Logging after every request. """
    logger = logging.getLogger('app.requests')
    logger.info('%s\t%s\t%s\t%s\t%s',
                flask.request.remote_addr,
                flask.request.method,
                flask.request.scheme,
                flask.request.full_path,
                response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every exception. """
    if isinstance(e, NotFound) or isinstance(e, TemplateNotFound):
        return 'Resource Not Found', 404

    logger = logging.getLogger('app.errors')
    tb = traceback.format_exc()
    logger.error('%s\t%s\t%s\t%s\n%s',
                 flask.request.remote_addr,
                 flask.request.method,
                 flask.request.scheme,
                 flask.request.full_path,
                 tb)
    return "Internal Server Error", 500


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'])
    print()
