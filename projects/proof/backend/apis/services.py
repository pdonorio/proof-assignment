# -*- coding: utf-8 -*-

import sys
import contextlib


class Devnull(object):

    def write(self, _):
        pass

    def flush(self):
        pass


@contextlib.contextmanager
def nooutput():
    """
    Thanks Alex: https://stackoverflow.com/a/1810086
    """
    savestderr = sys.stderr
    savestdout = sys.stdout
    sys.stdout = Devnull()
    sys.stderr = Devnull()
    try:
        yield
    finally:
        sys.stdout = savestdout
        sys.stderr = savestderr


def mongo():
    service = 'mongo'
    with nooutput():
        from restapi.services.detect import detector
        from proof.models.mongo import MongoClient, APP_DB
        extension = detector.services_classes.get(service)
        odm = extension().get_instance()
        link = MongoClient(odm.connection.conn_string)
    print("Connected to service: %s" % service)
    return link, odm, APP_DB


def postgres():
    service = 'sqlalchemy'
    with nooutput():
        from restapi.services.detect import detector
        # NOTE: need to fake the flask app for Flask-Sqlalchemy to work
        from flask import Flask

        app = Flask(__name__)
        # from proof.models.mongo import MongoClient, APP_DB
        extension = detector.services_classes.get(service)
        APP_DB = extension.variables.get('db')
        orm = extension(app=app).get_instance()
        with app.app_context():
            orm.init_app(app)
            orm.create_all()
        # link = MongoClient(odm.connection.conn_string)

    print("Connected to service: %s" % service)
    return app, orm, APP_DB
