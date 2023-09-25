import logging
from fastapi import FastAPI, HTTPException
from src.models.address import Address,AddressCreate
from src.db.databse import SessionLocal


# Create a FastAPI app
app = FastAPI()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Address
@app.post("/addresses/", response_model=Address)
def create_address(address: AddressCreate):
    """
    Creating address 
    """
    db = SessionLocal()
    try:
        db_address = Address(**address.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    except Exception as e:
        logger.error(f"Error creating address: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Read Address
@app.get("/addresses/{address_id}", response_model=Address)
def read_address(address_id: int):
    """
    Reading address
    """
    db = SessionLocal()
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
        if address is None:
            raise HTTPException(status_code=404, detail="Address not found")
        return address
    except Exception as e:
        logger.error(f"Error reading address: {e}")
        raise
    finally:
        db.close()

# Update Address
@app.put("/addresses/{address_id}", response_model=Address)
def update_address(address_id: int, address: AddressCreate):
    """
    Updating address
    """
    db = SessionLocal()
    try:
        db_address = db.query(Address).filter(Address.id == address_id).first()
        if db_address is None:
            raise HTTPException(status_code=404, detail="Address not found")

        for key, value in address.dict().items():
            setattr(db_address, key, value)

        db.commit()
        db.refresh(db_address)
        return db_address
    except Exception as e:
        logger.error(f"Error updating address: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Delete Address
@app.delete("/addresses/{address_id}", response_model=Address)
def delete_address(address_id: int):
    """
    Deleting address
    """
    db = SessionLocal()
    try:
        db_address = db.query(Address).filter(Address.id == address_id).first()
        if db_address is None:
            raise HTTPException(status_code=404, detail="Address not found")

        db.delete(db_address)
        db.commit()
        return db_address
    except Exception as e:
        logger.error(f"Error deleting address: {e}")
        db.rollback()
        raise
    finally:
        db.close()
