from pydantic import BaseModel

# Pydantic model for creating an address
class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str

    class Config():
        orm_mode =True

class AddressDisplay(BaseModel):
    id: int
    street: str
    city: str
    state: str
    postal_code: str


    class Config():
        orm_mode =True