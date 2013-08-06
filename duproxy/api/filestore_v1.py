# -*- coding: utf-8 -*-
"""
    duproxy.api
    ~~~~~~~~~~~~~

    duproxy api package
"""
import os

from flask import Blueprint, request, current_app
from flask import Response

from ..services import filestores
from ..duerror import DUProxyError
from . import route

v1_fs = Blueprint('filestores', __name__, url_prefix='/v1/filestores')


@v1_fs.before_request
def before_request():
    if current_app.config.get('DISABLE', False):
        return 'Disabled', 404


@route(v1_fs, '/', methods=['GET'])
def list():
    """List all filestores"""
    return filestores.all()


@route(v1_fs, '/', methods=['POST'])
def create():
    """Creates a new product. Returns the new file object instance."""
    if request.json.get('md5', None) is None:
        raise DUProxyError('MD5 is required')
    if request.json.get('g_id', None) is None:
        raise DUProxyError('g_id is required')
    if len(request.json.get('md5')) != 32:
        raise DUProxyError('Invalid MD5')

    return filestores.create(**request.json)


@route(v1_fs, '/stream', methods=['POST'])
def upload():
    """Accept a stream file upload"""
    import hashlib
    import shutil
    g_id = request.args.get('g_id', None)
    if g_id is None:
        raise DUProxyError('g_id is required')
    if not request.files or request.files.get('file', None) is None:
        raise DUProxyError('No file specified')
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                             g_id)
    m = hashlib.md5()
    with open(file_path, 'wb') as f:
        while True:
            data = request.files['file'].stream.read(1048576)
            if not data:
                break
            m.update(data)
            f.write(data)
    md5 = m.hexdigest()
    new_file_path = file_path + md5
    shutil.move(file_path, new_file_path)

    return filestores.create(g_id=g_id,
                             md5=md5,
                             local_path=new_file_path), 201


@route(v1_fs, '/<id_md5>')
def show(id_md5):
    """Returns a user instance."""
    return filestores.get_or_404(id_md5)


@route(v1_fs, '/<id_md5>', methods=['PUT'])
def update(id_md5):
    from ..task import update_filestore
    """Returns a user instance."""
    import shutil
    md5 = request.json.get('md5', None)
    if md5 is None:
        raise DUProxyError('MD5 is required')
    g_id = request.json.get('g_id', None)
    if g_id is None:
        raise DUProxyError('g_id is required')
    update_filestore.delay(g_id, md5)
    return "", 200
#    filestore = filestores.get_or_404(id_md5)
#    new_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
#                                 g_id + md5)
#    try:
#        shutil.move(filestore.local_path, new_file_path)
#    except Exception as e:
#        raise DUProxyError(repr(e))
#    filestore.local_path = new_file_path
#    filestore.g_id = g_id
#    return filestores.update(filestore)


@route(v1_fs, '/<id_md5>', methods=['DELETE'])
def delete(id_md5):
    """Deletes a product. Returns a 204 response."""
    filestores.delete(filestores.get_or_404(id_md5))
    return None, 204


@v1_fs.route('/stream/<id_md5>')
def download_file(id_md5):
    import os
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                             id_md5)
    if not os.path.isfile(file_path):
        raise DUProxyError('Invalid file path')

    def generate():
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024 * 1024)
                if not data:
                    break
                yield data
    return Response(generate())
