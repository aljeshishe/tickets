# -*- coding: utf-8 -*-
import re
import sys
from grachev import args
from alembic.config import main

import model


@args.command
def alembic(*args):
    new_args = ['-c', 'alembic/alembic.ini']
    new_args.extend(args)
    sys.exit(main(argv=new_args))


@args.command
def create():
    from sqlalchemy import create_engine
    engine = create_engine(model.SQLALCHEMY_SERVER_URI, echo=True)
    engine.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET=UTF8MB4" % model.SQLALCHEMY_DATABASE_NAME)


@args.command
def drop():
    from sqlalchemy import create_engine
    engine = create_engine(model.SQLALCHEMY_SERVER_URI, echo=True)
    engine.execute("DROP DATABASE IF EXISTS %s" % model.SQLALCHEMY_DATABASE_NAME)



if __name__ == '__main__':
    args = args.Arguments(globals())
    args.run(sys.argv)
