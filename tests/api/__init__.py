# -*- coding: utf-8 -*-
"""
    tests.api
    ~~~~~~~~~

    api tests package
"""

from duproxy.api import create_app

from .. import DUProxyTestCase, settings


class DUProxyApiTestCase(DUProxyTestCase):

    def _create_app(self):
        return create_app(settings)

    def setUp(self):
        super(DUProxyApiTestCase, self).setUp()
        pass
