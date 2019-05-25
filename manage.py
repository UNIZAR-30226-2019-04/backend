import os
import unittest
import threading

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import blueprint
from app.main import create_app, db, socketio
from app.main.model import blacklist, deseados,mensaje,pertenece,producto,reporteProducto, reporteUsuario,seguir, seguir, valoracion, categoria
from app.main.service.user_service import recomendar



app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

threading.Timer(7200, recomendar).start()


@manager.command
def run():
    socketio.run(app,host='127.0.0.1',port='5000')
    # app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()

