import json

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, text, case
from typing import List, Dict, Optional
from datetime import datetime

from app.database import get_db
from app.models.sql_alchemy_models import Object, Datapoint, ObjectDatapoint
from app.models.pydantic_models import (
    ObjectBase,
    ObjectCreate, ObjectUpdate, ObjectInDB,
    DatapointResponse, DatapointCreate
)

from app.utils import build_tree, build_subtree_with_datapoints, update_object_association, resolve_relative_path

router = APIRouter(prefix="/api/object")


@router.get("/tree")
def get_objects(
        db: Session = Depends(get_db)
):
    """
    Get objects with optional filtering by parent_id or type.
    If parent_id is not provided, returns top-level objects.
    """
    _query_all_objects = """SELECT
        id,
        name,
        type,
        parent_id
    FROM public."object"
    ORDER BY
        CASE WHEN parent_id IS NULL THEN 0 ELSE 1 END,
        parent_id,
        id;
    """
    objects_result = db.execute(text(_query_all_objects))
    objects = [dict(row) for row in objects_result.mappings()]
    hierarchy = build_tree(objects)

    return hierarchy


@router.get("/{object_id}")
def get_object(
        object_id: int = Path(..., title="The ID of the object to retrieve"),
        include_children: bool = False,
        include_datapoints: bool = True,
        db: Session = Depends(get_db)
):
    """
    Get a specific object by ID with optional inclusion of children and datapoints.
    """
    _object = db.query(Object).filter(Object.id == object_id).first()

    if not _object:
        raise HTTPException(status_code=404, detail="Object not found")

    result = {
        "id": _object.id,
        "name": _object.name,
        "type": _object.type,
        "location_details": _object.location_details,
        "parent_object_id": _object.parent_id,
        "created_at": _object.created_at,
        "updated_at": _object.updated_at
    }

    # Include children if requested
    if include_children:
        children = db.query(Object).filter(Object.parent_id == object_id).all()
        result["children"] = children

    # Include datapoints if requested
    if include_datapoints:
        _datapoint_query = f"""select d.id, d.name, d.value, d.unit, d.type from "object" o
                    join object_datapoint od on o.id = od."object_FK"
                    join datapoint d ON d.id = od."datapoint_FK"
                    where o.id = {object_id}"""

        _datapoint_result = db.execute(text(_datapoint_query))
        _columns = _datapoint_result.keys()
        _rows = _datapoint_result.fetchall()
        result["datapoints"] =  [dict(zip(_columns, row)) for row in _rows]

    return result


@router.put("/{object_id}") # , response_model=ObjectInDB)
def update_object(
        object_id: int = Path(..., title="The ID of the object to update"),
        object_data: ObjectUpdate = None,
        db: Session = Depends(get_db)
):
    """Update an existing object"""
    _object = db.query(Object).filter(Object.id == object_id).first()
    if not _object:
        raise HTTPException(status_code=404, detail="Object not found")

    if object_data.parent_id is not None:
        if object_data.parent_id == object_id:
            raise HTTPException(status_code=400, detail="Object cannot be its own parent")

        if object_data.parent_id > 0:
            parent = db.query(Object).filter(Object.id == object_data.parent_id).first()
            if not parent:
                raise HTTPException(status_code=400, detail="Parent object does not exist")

    # Update fields if provided
    if object_data.name is not None:
        _object.name = object_data.name

    if object_data.type is not None:
        _object.type = object_data.type

    if object_data.location_details is not None:
        _object.location_details = object_data.location_details

    if object_data.parent_id is not None:
        _object.parent_id = object_data.parent_id

    _object.updated_at = datetime.now()

    db.commit()
    db.refresh(_object)

    return _object


@router.post("/", status_code=201)
async def create_object(object_data: ObjectCreate, db: Session = Depends(get_db)):
    try:
        # Verify parent_id exists if provided
        if object_data.parent_id:
            parent = db.query(Object).filter(Object.id == object_data.parent_id).first()
            if not parent:
                raise HTTPException(status_code=400, detail=f"Parent object with id {object_data.parent_id} not found")

        # Create new object
        new_object = Object(
            name=object_data.name,
            type=object_data.type,
            parent_id=object_data.parent_id,
            location_details=object_data.location_details
        )

        db.add(new_object)
        db.commit()
        db.refresh(new_object)

        return new_object

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating object: {str(e)}")


@router.delete("/{object_id}", status_code=204)
def delete_object(
        object_id: int = Path(..., title="The ID of the object to delete"),
        db: Session = Depends(get_db)
):
    """Delete an object and all its children (cascade)"""
    # Get object
    _object = db.query(Object).filter(Object.id == object_id).first()
    if not _object:
        raise HTTPException(status_code=404, detail="Object not found")

    # Delete object (cascade will handle children and datapoints)
    db.delete(_object)
    db.commit()

    return None


# POST endpoint to create a datapoint under a specific object
@router.post("/{object_id}/datapoint/", response_model=DatapointResponse, status_code=201)
async def create_datapoint(
        object_id: int,
        datapoint_data: DatapointCreate,
        db: Session = Depends(get_db)
):
    try:
        # Create the datapoint
        new_datapoint = Datapoint(
            name=datapoint_data.name,
            value=datapoint_data.value,
            unit=datapoint_data.unit,
            is_fresh=datapoint_data.is_fresh,
            type=datapoint_data.type
        )

        db.add(new_datapoint)
        db.flush()  # Get the ID before committing

        # Associate with the specified object
        update_object_association(db, new_datapoint.id, object_id)

        db.commit()
        db.refresh(new_datapoint)

        # Return with associated object ID
        return DatapointResponse(
            id=new_datapoint.id,
            name=new_datapoint.name,
            value=new_datapoint.value,
            unit=new_datapoint.unit,
            created_at=new_datapoint.created_at.isoformat(),
            updated_at=new_datapoint.updated_at.isoformat(),
            is_fresh=new_datapoint.is_fresh,
            type=new_datapoint.type,
            object_id=object_id
        )

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating datapoint: {str(e)}")



@router.get("/query/{object_id}/{path:path}")
async def query_path(object_id: int, path: str, db: Session = Depends(get_db)):
    try:
        # Fetch subtree starting from the given object_id
        query_subtree = """
            WITH RECURSIVE object_hierarchy AS (
                SELECT 
                    o.id,
                    o.name,
                    o.type,
                    o.parent_id,
                    o.location_details
                FROM public."object" o
                WHERE o.id = :object_id
                UNION ALL
                SELECT 
                    o.id,
                    o.name,
                    o.type,
                    o.parent_id,
                    o.location_details FROM public."object" o
                INNER JOIN object_hierarchy oh ON o.parent_id = oh.id
            )
            SELECT 
                oh.id,
                oh.name,
                oh.type,
                oh.parent_id,
                oh.location_details,
                d.id as datapoint_id,
                d.name as datapoint_name,
                d.type as datapoint_type,
                d.value,
                d.unit,
                d.is_fresh,
                d.created_at,
                d.updated_at
            FROM object_hierarchy oh
            LEFT JOIN public.object_datapoint od ON oh.id = od."object_FK"
            LEFT JOIN public.datapoint d ON od."datapoint_FK" = d.id
            ORDER BY oh.id;
        """
        subtree_res = db.execute(text(query_subtree), {"object_id": object_id})
        objects = [dict(row) for row in subtree_res.mappings()]

        if not objects:
            raise HTTPException(status_code=404, detail=f"Object with id {object_id} not found")

        # Build the subtree starting from the root object
        subtree = build_subtree_with_datapoints(objects, object_id)

        result = resolve_relative_path(subtree[0], path)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
