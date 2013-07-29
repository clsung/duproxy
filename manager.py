#!/usr/bin/env python
from flask.ext.script import Manager

from duproxy import api
from duproxy.core import db

app = api.create_app()
manager = Manager(app)


@manager.command
def init_db():
    db.create_all()


if __name__ == "__main__":
    manager.run()
