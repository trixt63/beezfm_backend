from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Dict, Optional
from datetime import datetime

from app.database import get_db
from app.models.models import (
    Object,
    ObjectCreate, ObjectUpdate, ObjectInDB,
    ObjectWithChildren, ObjectWithDatapoints, ObjectWithRelations,
    Datapoint
)

router = APIRouter(prefix="/api/objects")


@router.post("/", response_model=ObjectInDB, status_code=201)
async def create_object(object_data: ObjectCreate, db: Session = Depends(get_db)):
    """Create a new object in the hierarchy"""
    # Validate object type
    valid_types = ['building', 'floor', 'room', 'device']
    if object_data.type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {', '.join(valid_types)}")

    if object_data.parent_object_id:
        parent = db.query(Object).filter(Object.id == object_data.parent_object_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent object does not exist")

        # Create object
    new_object = Object(
        name=object_data.name,
        type=object_data.type,
        location_details=object_data.location_details,
        parent_object_id=object_data.parent_object_id
    )

    db.add(new_object)
    db.commit()
    db.refresh(new_object)

    return new_object


@router.get("/", response_model=List[ObjectInDB])
def get_objects(
        parent_id: Optional[int] = None,
        type: Optional[str] = None,
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    """
    Get objects with optional filtering by parent_id or type.
    If parent_id is not provided, returns top-level objects.
    """
    query = db.query(Object)

    # Filter by parent_id
    if parent_id is not None:
        query = query.filter(Object.parent_object_id == parent_id)
    else:
        query = query.filter(Object.parent_object_id == None)

    # Filter by type
    if type is not None:
        query = query.filter(Object.type == type)

    # Add pagination
    objects = query.order_by(Object.name).limit(limit).offset(offset).all()

    return objects


@router.get("/{object_id}", response_model=ObjectWithRelations)
def get_object(
        object_id: int = Path(..., title="The ID of the object to retrieve"),
        include_children: bool = False,
        include_datapoints: bool = False,
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
        "parent_object_id": _object.parent_object_id,
        "created_at": _object.created_at,
        "updated_at": _object.updated_at
    }

    # Include children if requested
    if include_children:
        children = db.query(Object).filter(Object.parent_object_id == object_id).all()
        result["children"] = children

    # Include datapoints if requested
    if include_datapoints:
        datapoints = db.query(Datapoint).filter(Datapoint.object_FK == object_id).order_by(
            Datapoint.timestamp.desc()).all()
        result["datapoints"] = datapoints

    return result


@router.put("/{object_id}", response_model=ObjectInDB)
def update_object(
        object_id: int = Path(..., title="The ID of the object to update"),
        object_data: ObjectUpdate = None,
        db: Session = Depends(get_db)
):
    """Update an existing object"""
    # Get object
    object = db.query(Object).filter(Object.id == object_id).first()
    if not object:
        raise HTTPException(status_code=404, detail="Object not found")

    # Validate parent exists if provided
    if object_data.parent_object_id is not None:
        if object_data.parent_object_id == object_id:
            raise HTTPException(status_code=400, detail="Object cannot be its own parent")

        if object_data.parent_object_id > 0:  # Only check if it's not being set to NULL
            parent = db.query(Object).filter(Object.id == object_data.parent_object_id).first()
            if not parent:
                raise HTTPException(status_code=400, detail="Parent object does not exist")

    # Update fields if provided
    if object_data.name is not None:
        object.name = object_data.name

    if object_data.location_details is not None:
        object.location_details = object_data.location_details

    if object_data.parent_object_id is not None:
        object.parent_object_id = object_data.parent_object_id

    object.updated_at = datetime.now()

    db.commit()
    db.refresh(object)

    return object


@router.delete("/{object_id}", status_code=204)
def delete_object(
        object_id: int = Path(..., title="The ID of the object to delete"),
        db: Session = Depends(get_db)
):
    """Delete an object and all its children (cascade)"""
    # Get object
    object = db.query(Object).filter(Object.id == object_id).first()
    if not object:
        raise HTTPException(status_code=404, detail="Object not found")

    # Delete object (cascade will handle children and datapoints)
    db.delete(object)
    db.commit()

    return None


@router.get("/{object_id}/path", response_model=Dict[str, str])
def get_object_path(
        object_id: int = Path(..., title="The ID of the object to get path for"),
        db: Session = Depends(get_db)
):
    """Get the full hierarchical path for an object (e.g., Hotel.Floor.Room)"""
    # Check if object exists
    object = db.query(Object).filter(Object.id == object_id).first()
    if not object:
        raise HTTPException(status_code=404, detail="Object not found")

    # Use a raw SQL query with a recursive CTE to get the path
    # SQLAlchemy Core doesn't directly support recursive CTEs
    query = text("""
    WITH RECURSIVE object_path AS (
        SELECT id, name, parent_object_id, ARRAY[name] as path
        FROM objects
        WHERE id = :object_id

        UNION ALL

        SELECT o.id, o.name, o.parent_object_id, o.name || op.path
        FROM objects o
        JOIN object_path op ON o.id = op.parent_object_id
    )
    SELECT array_to_string(path, '.') as full_path
    FROM object_path
    WHERE parent_object_id IS NULL
    """)

    result = db.execute(query, {"object_id": object_id}).first()

    if not result or not result.full_path:
        raise HTTPException(status_code=404, detail="Object path not found")

    return {"path": result.full_path}


@router.get("/query/path", response_model=List[ObjectInDB])
async def query_by_path(
        path: str = Query(..., title="Dot-separated path (e.g. Hotel.Floor.Room)"),
        db: Session = Depends(get_db)
):
    """Find objects by hierarchical path"""
    path_segments = path.split('.')

    if not path_segments:
        raise HTTPException(status_code=400, detail="Invalid path format")

    # Start with the root object
    query = """
    WITH RECURSIVE object_hierarchy AS (
        -- Start with objects matching the first segment
        SELECT id, name, type, parent_object_id, location_details, created_at, updated_at, 1 as level, 
               ARRAY[id] as path_ids
        FROM objects
        WHERE name = $1 AND parent_object_id IS NULL

        UNION ALL

        -- Join with child objects matching the next segment
        SELECT o.id, o.name, o.type, o.parent_object_id, o.location_details, o.created_at, o.updated_at, 
               oh.level + 1, oh.path_ids || o.id
        FROM objects o
        JOIN object_hierarchy oh ON o.parent_object_id = oh.id
        WHERE oh.level < $3
    )
    -- Get objects at the final level with the correct path
    SELECT DISTINCT ON (path_ids) id, name, type, parent_object_id, location_details, created_at, updated_at
    FROM object_hierarchy
    WHERE level = $3 AND name = $2
    """

    # rows = await conn.fetch(query,
    #                         path_segments[0],
    #                         path_segments[-1],
    #                         len(path_segments)
    #                         )
    rows = db.query(query)

    # Now we need to verify complete paths match
    if len(path_segments) > 2:
        result = []
        # For each potential match, verify the complete path
        for row in rows:
            # Check if this path matches all segments
            is_valid_path = True
            object_id = row['id']

            # Get the full path for this object
            path_query = """
            WITH RECURSIVE object_path AS (
                SELECT id, name, parent_object_id, ARRAY[name] as path
                FROM objects
                WHERE id = $1

                UNION ALL

                SELECT o.id, o.name, o.parent_object_id, o.name || op.path
                FROM objects o
                JOIN object_path op ON o.id = op.parent_object_id
            )
            SELECT array_to_string(path, '.') as full_path
            FROM object_path
            WHERE parent_object_id IS NULL
            """

            full_path = db.query(path_query)

            # Compare with requested path
            if full_path == path:
                result.append(dict(row))

        return result

    return [dict(row) for row in rows]
