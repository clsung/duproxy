# -*- coding: utf-8 -*-
"""
    tests.settings
    ~~~~~~~~~~~~

    Test settings
"""
DEBUG = False
TESTING = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_POOL_SIZE = None
SQLALCHEMY_POOL_TIMEOUT = None
SQLALCHEMY_POOL_RECYCLE = None
UPLOAD_FOLDER = 'stream_test'

CELERY_ALWAYS_EAGER = True
