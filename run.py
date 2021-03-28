import logging
import os
import sys

from app import create_app, db
from app.models.user import User
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = create_app(db_uri='sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'production.db'))


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'user': User}


def run_tornado():
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%d.%m.%Y %H:%M:%S')
    access_logger = logging.getLogger('tornado.access')
    access_logger.setLevel(logging.INFO)
    access_handler = logging.StreamHandler(stream=sys.stdout)
    access_handler.setFormatter(formatter)
    access_logger.addHandler(access_handler)
    application_logger = logging.getLogger('tornado.application')
    application_logger.setLevel(logging.INFO)
    application_handler = logging.StreamHandler(stream=sys.stdout)
    application_handler.setFormatter(formatter)
    application_logger.addHandler(application_handler)
    general_logger = logging.getLogger('tornado.general')
    general_logger.setLevel(logging.INFO)
    general_handler = logging.StreamHandler(stream=sys.stdout)
    general_handler.setFormatter(formatter)
    general_logger.addHandler(general_handler)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()


if __name__ == '__main__':
    app.logger.info("Running using Tornado HTTP server.")
    run_tornado()
