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


def _build_temp_file(n):
    import os
    import tempfile
    import shutil
    from flask import current_app
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    with open(temp_path, 'wb') as f:
        f.write(randstr(100))
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                             n.g_id + n.md5)
    try:
        shutil.move(temp_path, file_path)
    except Exception as e:
        raise DUProxyError(repr(e))
    return file_path


class FileStoreFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = FileStore
    FACTORY_SESSION = db.session

    g_id = Sequence(lambda n: '{0}-{1}'.format(n, randstr(10)))
    md5 = LazyAttribute(lambda n: randstr(40))
    local_path = LazyAttribute(
        lambda n: _build_temp_file(n)
                              )
