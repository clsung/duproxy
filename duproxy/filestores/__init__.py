# -*- coding: utf-8 -*-
"""
    duproxy.filestore
    ~~~~~~~~~~~~~~~

    duproxy filestore package
"""

from ..core import Service
from ..duerror import DUProxyError
from .model import FileStore


class FileStoreService(Service):
    __model__ = FileStore

    def add_file(self, filestore, fileobject):
        if fileobject in filestore.products:
            raise DUProxyError(u'File exists')
        filestore.fileobjects.append(fileobject)
        return self.save(filestore)

    def remove_file(self, filestore, fileobject):
        if fileobject in filestore.fileobjects:
            raise DUProxyError(u'Invalid file')
        filestore.fileobjects.remove(fileobject)
        return self.save(filestore)
