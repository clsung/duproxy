# -*- coding: utf-8 -*-
"""
    duproxy.filestore.model
    ~~~~~~~~~~~~~~~

    Filestore Model
"""
from ..core import db
from ..helper import JsonSerializer


class FileStore(JsonSerializer, db.Model):
    __tablename__ = 'filestores'

    __json_hidden__ = ['local_path']

    id = db.Column(db.Integer, primary_key=True)
    g_id = db.Column(db.String(160))
    md5 = db.Column(db.String(40))
    local_path = db.Column(db.String())
