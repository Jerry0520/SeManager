# -*- coding: utf-8 -*-

from support import create_app, db
from flask_script import Manager,Shell
from flask_migrate import Migrate, MigrateCommand
from support.models.users import User, Role, roles_users
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, roles_users=roles_users)

@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
