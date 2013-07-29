# -*- coding: utf-8 -*-
"""
    duproxy.api
    ~~~~~~~~~~~~~

    duproxy api package
"""

import os

from functools import wraps

from flask import jsonify

from ..duerror import DUProxyError
from ..helper import JSONEncoder

from .. import application


def create_app(settings_override=None):
    """Returns the DUProxy API application instance"""

    app = application.create_app(__name__,
                                 __path__,
                                 settings_override)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Register custom error handlers
    app.errorhandler(DUProxyError)(on_duproxy_error)
    app.errorhandler(404)(on_404)
    app.errorhandler(405)(on_405)
    if os.path.exists(os.path.join(app.instance_path, 'disable')):
        app.config['DISABLE'] = True

    return app


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            status_code = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                status_code = rv[1]
                rv = rv[0]
            return jsonify(dict(data=rv)), status_code
        return f

    return decorator


def on_duproxy_error(e):
    return jsonify(dict(error=e.message)), 400


def on_404(e):
    return jsonify(dict(error='Not Found')), 404


def on_405(e):
    return jsonify(dict(error='Method Not Allowed')), 405
