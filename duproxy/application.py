# -*- coding: utf-8 -*-
"""
    duproxy.app
    ~~~~~~~~~~~

    duproxy application module
"""
import os

from celery import Celery
from flask import Blueprint
from flask import Flask

from .core import db


def create_app(package_name, package_path, settings_override=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the Overholt platform.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('duproxy.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    try:
        app.config.from_object(settings_override)
    except ImportError:
        pass

    db.init_app(app)

    register_blueprints(app, package_name, package_path)

    return app

def create_celery_app(app=None, settings_override=None):
    app = app or create_app('duproxy', os.path.dirname(__file__),
                            settings_override)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application
    found in all modules for the specified package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    import pkgutil
    import importlib

    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv
