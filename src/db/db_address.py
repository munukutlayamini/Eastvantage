from sqlalchemy.orm.session import Session
from db.schema import AddressCreate,AddressDisplay
from db.models import Address
from fastapi import HTTPException, status
import logging
from math import radians, sin, cos, sqrt, atan2


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

#creating new address
def create_address(db:Session, request:AddressCreate ):
    try:
        new_address =Address(
            door_no = request.door_no,
            street = request.street,
            city= request.city,
            state=request.state,
            postal_code=request.postal_code,
            latitude = request.latitude,
            longitude=request.longitude
            
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        logger.info("successfully created")
        return new_address
    except Exception as e:
        logger.error(f"Error updating address: {e}")

#get all addresses
def get_all(db:Session):
    try:
        logger.info("get all")
        return db.query(Address).all()
    except Exception as e:
        logger.error(f"Error updating address: {e}")

#get address by using id
def get_id(db:Session, id:int):
    logger.info("successfully get by id")
    return db.query(Address).filter(Address.id == id).first()

#update the address by id
def update_adres(id:int, request:AddressCreate, db:Session):
    db_address = db.query(Address).filter(Address.id == id).first()
    if db_address is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =f"Address with the id {id} is not available")
    for key, value in request.dict().items():
        setattr(db_address, key, value) if value else None
    db.commit()
    db.refresh(db_address)
    logger.info("successfully updated")
    return db_address


#delete the address based on id
def delete_address(db: Session, id:int):
    address = db.query(Address).filter(Address.id == id).first()
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No address with the id {id}")
        
    db.delete(address)
    db.commit()
    logger.info("successfully deleted")
    return address

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    try:
        earth_radius = 6371
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c
        return distance
    except Exception as e:
        logger.error(e)

#get addresses in given distance
def find_addresses_within_radius(radius_km:int, target_lat:float, target_lon:float,db:Session):
    addresses = [adres for adres in db.query(Address).all()]
    addresses_within_radius = []
    for address in addresses:
        distance = haversine_distance(target_lat, target_lon, address.latitude, address.longitude)
        if distance <= radius_km:
            addresses_within_radius.append(address)
    if len(addresses_within_radius)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No address with in distance")
    return addresses_within_radius