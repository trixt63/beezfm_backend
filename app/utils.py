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


def resolve_relative_path(object_root, path, list_returns=None):
    parts = path.split('.')
    # remove the first level of path:
    if parts[0].lower() == object_root['type']:
        parts.pop(0)

    current_obj = object_root
    if list_returns is None:
        list_returns = []

    current_part = parts[0]
    if any([current_part.lower() == _child['type'].lower() for _child in current_obj['children']]):
        # traverse children
        next_path = '.'.join([p_ for p_ in parts[1:]])
        for _child in current_obj['children']:
            resolve_relative_path(_child, next_path, list_returns)
    else:
        for _datapoint in current_obj['datapoints']:
            if _datapoint.get('type') and (current_part.lower() == _datapoint['type'].lower()):
                list_returns.append({
                    "id": current_obj["id"],
                    "name": current_obj["name"],
                    "type": current_obj["type"],
                    "location_details": current_obj["location_details"],
                    "datapoints": _datapoint
                })

    return list_returns


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
