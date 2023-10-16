from pydantic import BaseModel

# Pydantic model for creating an address
class AddressCreate(BaseModel):
    door_no: str
    street: str
    city: str
    state: str
    postal_code: str
    latitude: float
    longitude: float

    class Config():
        orm_mode =True


class AddressDisplay(BaseModel):
    id: int
    door_no: str
    street: str
    city: str
    state: str
    postal_code: str
    latitude: float
    longitude: float
    
    class Config():
        orm_mode =True
