from flask import Flask
from flask_migrate import Migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('config/base_settings.py')
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__)
manage = Manager(app)
migrate = Migrate(app, db)
