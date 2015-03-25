# ! /usr/bin/python
# coding: utf8
import web
from random import choice
import dbbackend as _db
from flask.ext.script import Manager
from helper import *


app = web.app
manager = Manager(app)


@manager.command
def run():
    """Run application"""
    app.run()


USERS = {
        "appointment": ["It", "App", "Developer", "QA Enginer"],
        "l_name": ["Low", "High", "Medium"],
        "name": ["Marina", "Sofia", "Alexander", "Roman", "Sergey"],
        "m_name": "Alexandovich",
        "start_time": ["2014-01-01", "2010-11-01"],
        "location": ["Russian Federation"],
        "views": [1, 2, 10, 300, 500],
        "avatar": ["/static/img/pl.jpg"],
        "nickname": ["bla", "lala"],
        "reputation": [102, 21922, 2112],
        "tags": [["python"], ["nodejs"], ["html"], ["flask"]]
    }


@manager.command
def filldb():
    db = _db.User(app.config["USER_COLLECT"])
    
    for x in xrange(100):
        item = dict((k, choice(v)) for k, v in USERS.items())
        item["permalink"] = random_string(12)
        db.insert(item)

if __name__ == '__main__':
    manager.run()
