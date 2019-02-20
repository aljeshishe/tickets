# -*- coding: utf-8 -*-
import sys
import log_config
from grachev import args
from alembic.config import main
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

log_config.configure()
SQLALCHEMY_DATABASE_NAME = 'tickets'
SQLALCHEMY_SERVER_URI = 'mysql+pymysql://root:root@localhost:33306'
SQLALCHEMY_DATABASE_URI = '%s/%s?charset=utf8mb4' % (SQLALCHEMY_SERVER_URI, SQLALCHEMY_DATABASE_NAME)
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False, pool_size=30, max_overflow=150)
Session = scoped_session(sessionmaker(bind=engine))


@args.command
def alembic(*args):
    new_args = ['-c', 'alembic/alembic.ini']
    new_args.extend(args)
    sys.exit(main(argv=new_args))


@args.command
def create():
    engine = create_engine(SQLALCHEMY_SERVER_URI, echo=True)
    engine.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET=UTF8MB4" % SQLALCHEMY_DATABASE_NAME)


@args.command
def drop():
    engine = create_engine(SQLALCHEMY_SERVER_URI, echo=True)
    engine.execute("DROP DATABASE IF EXISTS %s" % SQLALCHEMY_DATABASE_NAME)



if __name__ == '__main__':
    args = args.Arguments(globals())
    args.run(sys.argv)
