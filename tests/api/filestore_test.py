# -*- coding: utf-8 -*-
"""
    tests.api.filestore_tests
    ~~~~~~~~~~~~~~~~~~~~~~~

    api filestore tests module
"""

try: from cStringIO import StringIO
except: from StringIO import StringIO

from ..factories import FileStoreFactory
from . import DUProxyApiTestCase
from .. import db


class FileStoreApiTestCase(DUProxyApiTestCase):

    def _create_fixtures(self):
        super(FileStoreApiTestCase, self)._create_fixtures()
        self.filestore = FileStoreFactory()
        db.session.commit()
        pass

    def test_get_filestores(self):
        r = self.jget('/v1/filestores')
        self.assertOkJson(r)

    def test_get_filestore(self):
        r = self.jget('/v1/filestores/{0}'.format(self.filestore.id))
        self.assertOkJson(r)

    def test_create_filestore(self):
        r = self.jpost('/v1/filestores', data={
            'g_id': 'New filestore', 'md5': 'asdf' * 8
        })
        self.assertOkJson(r)

    def test_upload_with_invalid_file(self):
        r = self.post_with_file(
            '/v1/filestores/stream?g_id={0}&md5={1}'.format(
                self.filestore.g_id, self.filestore.md5
            ),
            data={
                'file': (StringIO('Foo bar baz' * 1024 * 1024), "N/A"),
            })
        self.assertStatusCode(r, 400)

    def test_upload_with_file(self):
        import hashlib
        m = hashlib.md5('Foo bar baz' * 1024 * 1024)
        r = self.post_with_file(
            '/v1/filestores/stream?g_id={0}&md5={1}'.format(
                self.filestore.g_id, m.hexdigest()
            ),
            data={
                'file': (StringIO('Foo bar baz' * 1024 * 1024), "N/A"),
            }
        )
        self.assertStatusCode(r, 201)

        r = self.get(
            '/v1/filestores/stream/{0}{1}'.format(
                self.filestore.g_id, m.hexdigest()
            )
        )
        self.assertEquals('Foo bar baz' * 1024 * 1024, r.data)

    def test_create_invalid_filestore(self):
        r = self.jpost('/v1/filestores', data={
            'g_id': 'New filestore', 'md5': 'axsd' * 4
        })
        self.assertBadJson(r)

    def test_update_filestore(self):
        r = self.jput('/v1/filestores/{0}'.format(self.filestore.id), data={
            'g_id': 'Old filestore'
        })
        self.assertOkJson(r)

    def test_delete_filestore(self):
        r = self.jdelete('/v1/filestores/{0}'.format(self.filestore.id))
        self.assertStatusCode(r, 204)
