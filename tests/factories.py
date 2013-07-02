# -*- coding: utf-8 -*-
"""
    tests.factories
    ~~~~~~~~~~~~

    for factory_boy
"""
from factory import Sequence, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory

from duproxy.core import db
from duproxy.models import FileStore
from .helper import randstr


class FileStoreFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = FileStore
    FACTORY_SESSION = db.session

    g_id = Sequence(lambda n: '{0}-{1}'.format(randstr(10), n))
    md5 = LazyAttribute(lambda n: "asdfg" * 8)
