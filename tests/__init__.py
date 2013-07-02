# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~

    tests package
"""

from unittest import TestCase
from flask import Request
from werkzeug.datastructures import MultiDict

import json

from duproxy.core import db

from .helper import TestingFileStorage


class DUProxyTestCase(TestCase):

    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        pass

    def setUp(self):
        super(DUProxyTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self._create_fixtures()

    def tearDown(self):
        super(DUProxyTestCase, self).tearDown()
        db.drop_all()
        self.app_context.pop()

    def _json_data(self, kwargs, csrf_enabled=True):
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/json'
        return kwargs

    def _request(self, method, *args, **kwargs):
        kwargs.setdefault('content_type', 'text/html')
        kwargs.setdefault('follow_redirects', True)
        return method(*args, **kwargs)

    def _jrequest(self, *args, **kwargs):
        return self._request(*args, **kwargs)

    def post_with_file(self, *args, **kwargs):
        class TestingRequest(Request):
            """A testing request to use that will return a
            TestingFileStorage to test the uploading."""
            @property
            def files(self):
                d = MultiDict()
                d['file'] = TestingFileStorage(
                    stream=kwargs['data']['file'][0],
                    filename=kwargs['data']['file'][1])
                return d
#            def _get_file_stream(*args, **kwargs):
#                return TestingFile()

        self.new_app = self._create_app()
        self.new_app.request_class = TestingRequest
        test_client = self.new_app.test_client()
        return self._request(test_client.post, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request(self.client.get, *args, **kwargs)

    def jget(self, *args, **kwargs):
        return self._jrequest(self.client.get, *args, **kwargs)

    def jpost(self, *args, **kwargs):
        return self._jrequest(self.client.post, *args,
                              **self._json_data(kwargs))

    def jput(self, *args, **kwargs):
        return self._jrequest(self.client.put, *args,
                              **self._json_data(kwargs))

    def jdelete(self, *args, **kwargs):
        return self._jrequest(self.client.delete, *args, **kwargs)

    def assertStatusCode(self, response, status_code):
        """Assert the status code of a Flask test client response

        :param response: The test client response object
        :param status_code: The expected status code
        """
        self.assertEquals(status_code, response.status_code)
        return response

    def assertOk(self, response):
        """Test that response status code is 200

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 200)

    def assertBadRequest(self, response):
        """Test that response status code is 400

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 400)

    def assertForbidden(self, response):
        """Test that response status code is 403

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 403)

    def assertNotFound(self, response):
        """Test that response status code is 404

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 404)

    def assertContentType(self, response, content_type):
        """Assert the content-type of a Flask test client response

        :param response: The test client response object
        :param content_type: The expected content type
        """
        self.assertEquals(content_type, response.headers['Content-Type'])
        return response

    def assertJson(self, response):
        """Test that content returned is in JSON format

        :param response: The test client response object
        """
        return self.assertContentType(response, 'application/json')

    def assertOkJson(self, response):
        """Assert the response status code is 200 and a JSON response

        :param response: The test client response object
        """
        return self.assertOk(self.assertJson(response))

    def assertBadJson(self, response):
        """Assert the response status code is 400 and a JSON response

        :param response: The test client response object
        """
        return self.assertBadRequest(self.assertJson(response))
