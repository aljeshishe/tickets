from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.ddl import DropConstraint
from sqlalchemy import Column, String, Integer, ForeignKey, Sequence, func, Table, DateTime, MetaData
from sqlalchemy.orm import relationship, backref, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


__author__ = 'alexey.grachev'
Base = declarative_base()


class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)

    depart_date_time = Column(DateTime())
    arrive_date_time = Column(DateTime())

    depart_code = Column(String(5))
    arrive_code = Column(String(5))
    duration = Column(Integer)
    stop_count = Column(Integer)
    price = Column(Integer)

SERVER_CONNECT_STRING = 'mysql+pymysql://root:root@localhost'
DB_CONNECT_STRING = 'mysql+pymysql://root:root@localhost/lux'
engine = create_engine(DB_CONNECT_STRING, echo=False)
Session = sessionmaker(bind=engine)
# Session = scoped_session(sessionmaker(bind=engine))


def get_or_create(session, model, defaults={}, **kwargs):
    query = session.query(model).filter_by(**kwargs)
    instance = query.first()
    if instance:
        return instance, False
    else:
        session.begin(nested=True)
        try:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            params.update(defaults)
            instance = model(**params)
            session.add(instance)
            session.commit()
            return instance, True
        except IntegrityError:
            import traceback
            traceback.print_exc()
            session.rollback()
            instance = query.one()
            return instance, False


if __name__ == '__main__':
    Base.metadata.bind = engine
    Base.metadata.create_all()
    session = Session()
    try:
        # msk, _ = get_or_create(session, City, defaults={'short_name': 'msk', 'name': 'Moscow'}, short_name='msk', name='Moscow')
        t = Ticket(depart_date_time=datetime.now(), arrive_date_time=datetime.now(), depart_code='LED', arrive_code='MOW',
                   duration=10, stop_count=1, price=1)
        session.add(t)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
