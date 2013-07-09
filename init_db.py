from duproxy import application
from duproxy import api
from duproxy.core import db
from duproxy.models import FileStore
from flask.ext.sqlalchemy import SQLAlchemy
app = api.create_app()
db.init_app(app)
with app.test_request_context():
    db.create_all()

