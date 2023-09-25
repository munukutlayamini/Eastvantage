from sqlalchemy import create_engine,Column, Integer, String
from pydantic import BaseModel
from src.db.databse import Base


# Pydantic model for creating an address
class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str


# Define the Address model
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)


