# -*- coding: utf-8 -*-
"""
duproxy.tasks
~~~~~~~~~~~~~~

duproxy tasks module for Celery
"""
import os
import hashlib
import shutil

from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from flask import current_app

from duproxy import api
from .core import db
from .application import create_celery_app
from .services import filestores

logger = get_task_logger(__name__)

celery = create_celery_app(current_app or api.create_app('local_settings'))


if __name__ == '__main__':
    celery.start()


@celery.task()
def upload_filestore(g_id, md5, new_file_path):
    return filestores.create(g_id=g_id,
                             md5=md5,
                             local_path=new_file_path).to_dict


@celery.task(ignore_result=True)
def update_filestore(dir_path, id_md5, g_id, md5):
    filestore = filestores.get(id_md5)
    if filestore is None:
        logger.error("No such filestore {0}".format(id_md5))
        return
    new_file_path = os.path.join(dir_path,
                                 g_id + md5)
    try:
        shutil.move(filestore.local_path, new_file_path)
    except Exception as e:
        logger.exception(e)
        return
    filestore.local_path = new_file_path
    filestore.g_id = g_id
    return filestores.update(filestore)


@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()
