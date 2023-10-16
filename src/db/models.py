from db.database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    door_no = Column(String)
    street = Column(String, index=True)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    
