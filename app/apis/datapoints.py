from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import DatapointCreate, DatapointUpdate, DatapointInDB

router = APIRouter(prefix="/api/datapoints")


@router.post("/", response_model=DatapointInDB, status_code=201)
async def create_datapoint(datapoint: DatapointCreate, db: Session = Depends(get_db)):
    """Create a new datapoint associated with an object"""
    # Validate object exists
    # object_exists = await conn.fetchval(
    #     "SELECT EXISTS(SELECT 1 FROM objects WHERE id = $1)",
    #     datapoint.object_FK
    # )
    # if not object_exists:
    #     raise HTTPException(status_code=400, detail="Referenced object does not exist")
    #
    # # Create datapoint
    # now = datetime.now()
    # query = """
    # INSERT INTO datapoints (object_FK, value, unit, timestamp, created_at, updated_at)
    # VALUES ($1, $2, $3, $4, $5, $6)
    # RETURNING datapoint_id, object_FK, value, unit, timestamp, created_at, updated_at
    # """
    # row = await conn.fetchrow(
    #     query,
    #     datapoint.object_FK,
    #     datapoint.value,
    #     datapoint.unit,
    #     now,
    #     now,
    #     now
    # )
    #
    # return dict(row)


@router.get("/{datapoint_id}", response_model=DatapointInDB)
async def get_datapoint(
        datapoint_id: int = Path(..., title="The ID of the datapoint to retrieve"),
        db: Session = Depends(get_db)
):
    """Get a specific datapoint by ID"""
    # query = """
    # SELECT datapoint_id, object_FK, value, unit, timestamp, created_at, updated_at
    # FROM datapoints
    # WHERE datapoint_id = $1
    # """
    # row = await conn.fetchrow(query, datapoint_id)
    #
    # if not row:
    #     raise HTTPException(status_code=404, detail="Datapoint not found")
    #
    # return dict(row)


@router.get("/object/{object_id}", response_model=List[DatapointInDB])
async def get_object_datapoints(
        object_id: int = Path(..., title="The ID of the object"),
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """Get all datapoints for a specific object"""
    # Verify object exists
    # object_exists = await conn.fetchval(
    #     "SELECT EXISTS(SELECT 1 FROM objects WHERE id = $1)",
    #     object_id
    # )
    # if not object_exists:
    #     raise HTTPException(status_code=404, detail="Object not found")
    #
    # query = """
    # SELECT datapoint_id, object_FK, value, unit, timestamp, created_at, updated_at
    # FROM datapoints
    # WHERE object_FK = $1
    # ORDER BY timestamp DESC
    # LIMIT $2 OFFSET $3
    # """
    # rows = await conn.fetch(query, object_id, limit, offset)
    #
    # return [dict(row) for row in rows]


@router.put("/{datapoint_id}", response_model=DatapointInDB)
async def update_datapoint(
        datapoint_id: int = Path(..., title="The ID of the datapoint to update"),
        datapoint_data: DatapointUpdate = None,
        db: Session = Depends(get_db)
):
    """Update an existing datapoint"""
    # # Verify datapoint exists
    # exists = await conn.fetchval(
    #     "SELECT EXISTS(SELECT 1 FROM datapoints WHERE datapoint_id = $1)",
    #     datapoint_id
    # )
    # if not exists:
    #     raise HTTPException(status_code=404, detail="Datapoint not found")
    #
    # # Update datapoint
    # query = "UPDATE datapoints SET updated_at = $1"
    # params = [datetime.now()]
    #
    # if datapoint_data.value is not None:
    #     params.append(datapoint_data.value)
    #     query += f", value = ${len(params)}"
    #
    # if datapoint_data.unit is not None:
    #     params.append(datapoint_data.unit)
    #     query += f", unit = ${len(params)}"
    #
    # query += " WHERE datapoint_id = $" + str(len(params) + 1)
    # params.append(datapoint_id)
    #
    # query += " RETURNING datapoint_id, object_FK, value, unit, timestamp, created_at, updated_at"
    #
    # row = await conn.fetchrow(query, *params)
    # return dict(row)


@router.delete("/{datapoint_id}", status_code=204)
async def delete_datapoint(
        datapoint_id: int = Path(..., title="The ID of the datapoint to delete"),
        db: Session = Depends(get_db)
):
    """Delete a datapoint"""
    # # Verify datapoint exists
    # exists = await conn.fetchval(
    #     "SELECT EXISTS(SELECT 1 FROM datapoints WHERE datapoint_id = $1)",
    #     datapoint_id
    # )
    # if not exists:
    #     raise HTTPException(status_code=404, detail="Datapoint not found")
    #
    # # Delete datapoint
    # await conn.execute("DELETE FROM datapoints WHERE datapoint_id = $1", datapoint_id)
    # return None


@router.get("/history/{object_id}", response_model=List[DatapointInDB])
async def get_datapoint_history(
        object_id: int = Path(..., title="The ID of the object"),
        from_time: Optional[str] = Query(None, title="Start time (ISO format)"),
        to_time: Optional[str] = Query(None, title="End time (ISO format)"),
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """Get historical datapoints for an object with time range filtering"""

    # object_exists = await conn.fetchval(
    #     "SELECT EXISTS(SELECT 1 FROM objects WHERE id = $1)",
    #     object_id
    # )
    # if not object_exists:
    #     raise HTTPException(status_code=404, detail="Object not found")
    #
    # query = """
    # SELECT datapoint_id, object_FK, value, unit, timestamp, created_at, updated_at
    # FROM datapoints
    # WHERE object_FK = $1
    # """
    # params = [object_id]
    #
    # # Add time range filtering if provided
    # if from_time:
    #     try:
    #         from_datetime = datetime.fromisoformat(from_time)
    #         query += f" AND timestamp >= ${len(params) + 1}"
    #         params.append(from_datetime)
    #     except ValueError:
    #         raise HTTPException(status_code=400,
    #                             detail="Invalid from_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
    #
    # if to_time:
    #     try:
    #         to_datetime = datetime.fromisoformat(to_time)
    #         query += f" AND timestamp <= ${len(params) + 1}"
    #         params.append(to_datetime)
    #     except ValueError:
    #         raise HTTPException(status_code=400, detail="Invalid to_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
    #
    # # Add ordering and pagination
    # query += f" ORDER BY timestamp DESC LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}"
    # params.extend([limit, offset])
    #
    # rows = await conn.fetch(query, *params)
    #
    # return [dict(row) for row in rows]
