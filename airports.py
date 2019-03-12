from sqlalchemy import Column, String, Integer, Float

from model import Base


class Airport(Base):
    __tablename__ = 'airport'
    code = Column(String(10), primary_key=True)
    city_name = Column(String(50))
    country_code = Column(String(5))
    country = Column(String(50))
    latitude = Column(Float())
    longitude = Column(Float())


class Route(Base):
    __tablename__ = 'route'
    depart = Column(String(10), primary_key=True)
    arrive = Column(String(10), primary_key=True)
    carrier = Column(String(10), primary_key=True)
    carrier_name = Column(String(100))

