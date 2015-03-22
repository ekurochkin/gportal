# coding: utf8
import web
from random import choise
import dbbackend as _db
from flask.ext.script import Manager


app = web.app.create_app()
manager = Manager(app)


@manager.command
def run():
    """Run application"""
    app.run()

users = {
        "appointment": ["It", "App", "Developer", "QA Enginer"],
        "l_name": ["l_name_1"],
        "name": ["Marina", "Sofia", "Alexander", "Roman", "Sergey"],
        "m_name": "m_name_1",
        "duration": [],
        "location": ["Russian Federation"],
        "views": [1, 2, 10, 300, 500]
    }


@manager.command
def fill_db():
	pass


if __name__ == '__main__':
    manager.run()
