from flask_migrate import MigrateCommand
from application import app, manage
from flask_script import Server

from libs.models import *  # 把模型对象都导入 否则MigrateCommand无法加载
import www

manage.add_command('runserver', Server(port=app.config['SERVERPORT'], use_debugger=True, use_reloader=True))
manage.add_command('db', MigrateCommand)


def main():
    manage.run()


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
