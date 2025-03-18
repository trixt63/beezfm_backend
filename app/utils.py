# Helper function to build tree structure
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import Union, List, Dict
from app.models.sql_alchemy_models import Object, Datapoint, ObjectDatapoint
from app.models.pydantic_models import DatapointCreate, DatapointUpdate, DatapointResponse
from sqlalchemy.orm import Session


def build_tree(objects_list, parent_id=None):
    tree = []
    for obj in objects_list:
        if obj['parent_id'] == parent_id:
            # Create node
            node = {
                'id': obj['id'],
                'name': obj['name'],
                'type': obj['type'],
                'children': build_tree(objects_list, obj['id'])
            }
            tree.append(node)
    return tree


# Helper function to build tree with datapoints
def build_subtree_with_datapoints(objects_list, root_id=None):
    tree = []
    current_node = None

    for obj in objects_list:
        # Start with the root object
        if obj['id'] == root_id and not current_node:
            current_node = {
                'id': obj['id'],
                'name': obj['name'],
                'type': obj['type'],
                'location_details': obj['location_details'],
                'datapoints': [],
                'children': []
            }
            tree.append(current_node)

        # Add children and datapoints
        if current_node:
            obj_datapoint = {
                'id': obj['datapoint_id'],
                'name': obj['datapoint_name'],
                'type': obj['datapoint_type'],
                'value': obj['value'],
                'unit': obj['unit'],
                'is_fresh': obj['is_fresh'],
                'created_at': obj['created_at'],
                'updated_at': obj['updated_at']
            }
            if obj['parent_id'] == current_node['id'] and obj['id'] != current_node['id']:
                _child_existed = False
                # if old child:
                for _child in current_node['children']:
                    if obj['id'] == _child['id']:
                        _child_existed = True
                        _child['datapoints'].append(obj_datapoint)
                # if new child:
                if not _child_existed:
                    child = {
                        'id': obj['id'],
                        'name': obj['name'],
                        'type': obj['type'],
                        'location_details': obj['location_details'],
                        'datapoints': [obj_datapoint],
                        'children': build_subtree_with_datapoints(objects_list, obj['id'])
                    }
                    current_node['children'].append(child)

            if obj['datapoint_id'] and obj['id'] == current_node['id']:
                current_node['datapoints'].append(obj_datapoint)
    return tree


# Updated path resolution using type
def resolve_path_by_type(objects, path: str) -> Union[dict, List[dict], None]:
    parts = path.split('.')
    datapoint_type = parts.pop()
    current_level = objects

    # Traverse the path for object types
    for i, part in enumerate(parts):
        next_level = []
        is_last = (i == len(parts) - 1)

        for obj in current_level:
            if obj["type"].lower() == part.lower():
                # if is_last and not any(p["type"].lower() == part.lower() for p in obj["datapoints"]):
                #     # Path ends with object type
                #     next_level.append(obj)
                if not is_last:
                    # Continue traversing children
                    children = [o for o in objects if o.get("parent_id") == obj["id"]]
                    next_level.extend(children)
            if is_last and any(p["type"].lower() == datapoint_type.lower() for p in obj["datapoints"]):
                # Path ends with datapoint type
                datapoints = [dp for dp in obj["datapoints"] if dp["type"].lower() == datapoint_type.lower()]
                return datapoints

        if not next_level and not is_last:
            return []
        else:
            current_level = next_level

    return current_level


# Helper function to manage single object association
def update_object_association(db: Session, datapoint_id: int, object_id: int):
    # Validate object exists
    if not db.query(Object).filter(Object.id == object_id).first():
        raise HTTPException(status_code=404, detail=f"Object with id {object_id} not found")

    # Remove any existing association
    db.query(ObjectDatapoint).filter(ObjectDatapoint.datapoint_FK == datapoint_id).delete()

    # Create new association
    new_assoc = ObjectDatapoint(object_FK=object_id, datapoint_FK=datapoint_id)
    db.add(new_assoc)
