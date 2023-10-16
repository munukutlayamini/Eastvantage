from fastapi import APIRouter
from typing import List
from fastapi import APIRouter, Depends,status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.schema import AddressCreate,AddressDisplay
from db import db_address
import logging


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler = logging.FileHandler("Adderss_log.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


router_address = APIRouter(
    prefix='/address',
    tags=["Post"]
)

#creating new address
@router_address.post('',response_model=AddressDisplay)
def create_address(request: AddressCreate , db:Session=Depends(get_db)):
    try:
        if not request:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Parameter image_type_url can only tale 'absolute', 'relative'.")
        return db_address.create_address(db, request)
    except Exception as e:
        logger.error(f"Error create address: {e}")

#deleting address by id
@router_address.delete('/delete/{id}')
def delete_address(id:int, db:Session =Depends(get_db)):
    try:
        return db_address.delete(db, id)
    except Exception as e:
        logger.error(f"Error delete address: {e}")

#get all the addresses
@router_address.get('/all', response_model=List[AddressDisplay])
def all_address(db:Session= Depends(get_db)):
    try:
        return db_address.get_all(db)
    except Exception as e:
        logger.error(f"Error get address: {e}")

#get address by id
@router_address.get('/{id}', response_model =AddressDisplay)
def address_id(id:int,db:Session= Depends(get_db)):
    try:
        return db_address.get_id(db, id)
    except Exception as e:
        logger.error(f"Error get by id address: {e}")

#update the address by id
@router_address.put('/{id}')
def update_address(id:int, request:AddressCreate,db:Session= Depends(get_db)):
    try:
        return db_address.update_address(id, request, db)
    except Exception as e:
        logger.error(f"Error updating address: {e}")


@router_address.get('/{disance}/{logitude}/{latitude}')
def get_address_by_distance(distance:int,longitude:float,latitude:float, db:Session= Depends(get_db)):
    try:
        return db_address.find_addresses_within_radius(distance,latitude,longitude,db)
    except Exception as e:
        logger.error(f"Error getting by address: {e}")