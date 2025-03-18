from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sql_alchemy_models import Object, Datapoint, ObjectDatapoint
from app.models.pydantic_models import DatapointCreate, DatapointUpdate, DatapointResponse

router = APIRouter(prefix="/api/datapoints")


# GET endpoint to retrieve a datapoint by ID
@router.get("/{id}") #, response_model=DatapointResponse)
async def get_datapoint(id: int, db: Session = Depends(get_db)):
    try:
        # Fetch the datapoint
        datapoint = db.query(Datapoint).filter(Datapoint.id == id).first()
        if not datapoint:
            raise HTTPException(status_code=404, detail=f"Datapoint with id {id} not found")

        # Get associated object ID
        association = db.query(ObjectDatapoint).filter(
            ObjectDatapoint.datapoint_FK == datapoint.id
        ).first()
        object_id = association.object_FK if association else None

        # Prepare response
        return DatapointResponse(
            id=datapoint.id,
            name=datapoint.name,
            value=datapoint.value,
            unit=datapoint.unit,
            created_at=datapoint.created_at,
            updated_at=datapoint.updated_at,
            is_fresh=datapoint.is_fresh,
            type=datapoint.type,
            object_id=object_id
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving datapoint: {str(e)}")

# PUT endpoint to update a datapoint (partial update)
@router.put("/{id}", response_model=DatapointResponse)
async def update_datapoint(
        id: int,
        datapoint_data: DatapointUpdate,
        db: Session = Depends(get_db)
):
    try:
        # Fetch existing datapoint
        datapoint = db.query(Datapoint).filter(Datapoint.id == id).first()
        if not datapoint:
            raise HTTPException(status_code=404, detail=f"Datapoint with id {id} not found")

        # Check if at least one field is provided
        if not any([datapoint_data.name, datapoint_data.value, datapoint_data.unit,
                    datapoint_data.is_fresh is not None, datapoint_data.type]):
            raise HTTPException(status_code=400, detail="At least one field must be provided for update")

        # Update only fields that are not None in the request
        if datapoint_data.name is not None:
            datapoint.name = datapoint_data.name
        if datapoint_data.value is not None:
            datapoint.value = datapoint_data.value
        if datapoint_data.unit is not None:
            datapoint.unit = datapoint_data.unit
        if datapoint_data.is_fresh is not None:
            datapoint.is_fresh = datapoint_data.is_fresh
        if datapoint_data.type is not None:
            datapoint.type = datapoint_data.type

        db.commit()
        db.refresh(datapoint)

        # Get associated object ID for response
        association = db.query(ObjectDatapoint).filter(
            ObjectDatapoint.datapoint_FK == datapoint.id
        ).first()
        object_id = association.object_FK if association else None

        return DatapointResponse(
            id=datapoint.id,
            name=datapoint.name,
            value=datapoint.value,
            unit=datapoint.unit,
            created_at=datapoint.created_at,
            updated_at=datapoint.updated_at,
            is_fresh=datapoint.is_fresh,
            type=datapoint.type,
            object_id=object_id
        )

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating datapoint: {str(e)}")


@router.delete("/{id}", status_code=204)
async def delete_datapoint(id: int, db: Session = Depends(get_db)):
    try:
        # Fetch existing datapoint
        datapoint = db.query(Datapoint).filter(Datapoint.id == id).first()
        if not datapoint:
            raise HTTPException(status_code=404, detail=f"Datapoint with id {id} not found")

        # Delete the datapoint (cascades to ObjectDatapoint due to ON DELETE CASCADE)
        db.delete(datapoint)
        db.commit()

        return None  # 204 No Content

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting datapoint: {str(e)}")
