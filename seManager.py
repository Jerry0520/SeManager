#-*- coding:uft-8 -*-
from support import create_app, db
from flask_script import Manager


app = create_app('config')
manager = Manager(app)


if __name__ == '__main__':
    Manager.run()

