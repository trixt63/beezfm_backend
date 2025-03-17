import json

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, text, case
from typing import List, Dict, Optional
from datetime import datetime

from app.database import get_db
from app.models.sql_alchemy_models import Object, Datapoint
from app.models.pydantic_models import (
    ObjectBase,
    ObjectCreate, ObjectUpdate, ObjectInDB,
    ObjectWithRelations,
)

from app.utils import build_tree, build_subtree_with_datapoints, resolve_path_by_type

router = APIRouter(prefix="/api/objects")


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

# @router.put("/{object_id}", response_model=ObjectInDB)
# def update_object(
#         object_id: int = Path(..., title="The ID of the object to update"),
#         object_data: ObjectUpdate = None,
#         db: Session = Depends(get_db)
# ):
#     """Update an existing object"""
#     # Get object
#     object = db.query(Object).filter(Object.id == object_id).first()
#     if not object:
#         raise HTTPException(status_code=404, detail="Object not found")
#
#     # Validate parent exists if provided
#     if object_data.parent_object_id is not None:
#         if object_data.parent_object_id == object_id:
#             raise HTTPException(status_code=400, detail="Object cannot be its own parent")
#
#         if object_data.parent_object_id > 0:  # Only check if it's not being set to NULL
#             parent = db.query(Object).filter(Object.id == object_data.parent_object_id).first()
#             if not parent:
#                 raise HTTPException(status_code=400, detail="Parent object does not exist")
#
#     # Update fields if provided
#     if object_data.name is not None:
#         object.name = object_data.name
#
#     if object_data.location_details is not None:
#         object.location_details = object_data.location_details
#
#     if object_data.parent_object_id is not None:
#         object.parent_id = object_data.parent_object_id
#
#     object.updated_at = datetime.now()
#
#     db.commit()
#     db.refresh(object)
#
#     return object
#
#
# @router.delete("/{object_id}", status_code=204)
# def delete_object(
#         object_id: int = Path(..., title="The ID of the object to delete"),
#         db: Session = Depends(get_db)
# ):
#     """Delete an object and all its children (cascade)"""
#     # Get object
#     object = db.query(Object).filter(Object.id == object_id).first()
#     if not object:
#         raise HTTPException(status_code=404, detail="Object not found")
#
#     # Delete object (cascade will handle children and datapoints)
#     db.delete(object)
#     db.commit()
#
#     return None


# @router.get("/{object_id}/path", response_model=Dict[str, str])
# def get_object_path(
#         object_id: int = Path(..., title="The ID of the object to get path for"),
#         db: Session = Depends(get_db)
# ):
#     """Get the full hierarchical path for an object (e.g., Hotel.Floor.Room)"""
#     # Check if object exists
#     object = db.query(Object).filter(Object.id == object_id).first()
#     if not object:
#         raise HTTPException(status_code=404, detail="Object not found")
#
#     # Use a raw SQL query with a recursive CTE to get the path
#     # SQLAlchemy Core doesn't directly support recursive CTEs
#     query = text("""
#     WITH RECURSIVE object_path AS (
#         SELECT id, name, parent_object_id, ARRAY[name] as path
#         FROM objects
#         WHERE id = :object_id
#
#         UNION ALL
#
#         SELECT o.id, o.name, o.parent_object_id, o.name || op.path
#         FROM objects o
#         JOIN object_path op ON o.id = op.parent_object_id
#     )
#     SELECT array_to_string(path, '.') as full_path
#     FROM object_path
#     WHERE parent_object_id IS NULL
#     """)
#
#     result = db.execute(query, {"object_id": object_id}).first()
#
#     if not result or not result.full_path:
#         raise HTTPException(status_code=404, detail="Object path not found")
#
#     return {"path": result.full_path}


# @router.get("/query/path", response_model=List[ObjectInDB])
# async def query_by_path(
#         path: str = Query(..., title="Dot-separated path (e.g. Hotel.Floor.Room)"),
#         db: Session = Depends(get_db)
# ):
#     """Find objects by hierarchical path"""
#     path_segments = path.split('.')
#
#     if not path_segments:
#         raise HTTPException(status_code=400, detail="Invalid path format")
#
#     # Start with the root object
#
#     # mock_data =


GET_OBJECT_SUBTREE = """
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
@router.get("/query/{object_id}/{path:path}")
async def query_subtree(object_id: int, path: str, db: Session = Depends(get_db)):
    try:
        # Fetch subtree starting from the given object_id
        result = db.execute(text(GET_OBJECT_SUBTREE), {"object_id": object_id})
        objects = [dict(row) for row in result.mappings()]

        if not objects:
            raise HTTPException(status_code=404, detail=f"Object with id {object_id} not found")

        # Build the subtree starting from the root object
        subtree = build_subtree_with_datapoints(objects, object_id)

        # Resolve the path within the subtree
        # TODO: fix resolve_path_by_type
        result = resolve_path_by_type(subtree, path)

        if result is None:
            raise HTTPException(status_code=404, detail=f"Path '{path}' not found in subtree of object {object_id}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# TODO: add get subtree api