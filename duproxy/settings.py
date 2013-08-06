# -*- coding: utf-8 -*-
"""
    duproxy.settings
    ~~~~~~~~~~~~~~~

    duproxy settings module
"""

DEBUG = True
SECRET_KEY = 'random me'

SQLALCHEMY_DATABASE_URI = 'sqlite:///abc.db'
UPLOAD_FOLDER = 'stream'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
