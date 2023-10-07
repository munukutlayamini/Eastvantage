from sqlalchemy.orm.session import Session
from db.schema import AddressCreate,AddressDisplay
from db.models import Address
from fastapi import HTTPException, status
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

#creating new address
def create_address(db:Session, request:AddressCreate ):
    try:
        new_address =Address(
            street = request.street,
            city= request.city,
            state=request.state,
            postal_code=request.postal_code
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
    try:
        logger.info("successfully get by id")
        return db.query(Address).filter(Address.id == id).first()
    except Exception as e:
        logger.error(f"Error updating address: {e}")

#update the address by id
def update_address(id:int, request:AddressCreate, db:Session):
    address = db.query(Address).filter(Address.id == id)
    try:
        if not address.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =f"Blog with the id {id} is not available")
        address.update({"street":request.street, "city":request.city,"state":request.state,"postal_code":request.postal_code}, synchronize_session=False)
        db.commit()
        logger.info("successfully updated")
        return {"Message": "Updated Sucessfuly", "data": request}
    except Exception as e:
        logger.error(f"Error updating address: {e}")

#delete the address based on id
def delete(db: Session, id:int):
    post = db.query(Address).filter(Address.id == id).first()
    try:
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post with the id {id}")
            
        db.delete(post)
        db.commit()
        logger.info("successfully deleted")
        return{
            "message": "Deleted Succesfully" 
        }
    except Exception as e:
        logger.error(f"Error updating address: {e}")

