# Helper function to build tree structure
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import Union, List
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
            if obj['parent_id'] == current_node['id'] and obj['id'] != current_node['id']:
                child = {
                    'id': obj['id'],
                    'name': obj['name'],
                    'type': obj['type'],
                    'location_details': obj['location_details'],
                    'datapoints': [],
                    'children': build_subtree_with_datapoints(objects_list, obj['id'])
                }
                current_node['children'].append(child)

            if obj['datapoint_id'] and obj['id'] == current_node['id']:
                current_node['datapoints'].append({
                    'id': obj['datapoint_id'],
                    'name': obj['datapoint_name'],
                    'type': obj['datapoint_type'],
                    'value': obj['value'],
                    'unit': obj['unit'],
                    'is_fresh': obj['is_fresh'],
                    'created_at': obj['created_at'],
                    'updated_at': obj['updated_at']
                })
    return tree


# Updated path resolution using type
def resolve_path_by_type(hierarchy, path: str) -> Union[dict, List[dict], None]:
    parts = path.split('.')
    current = hierarchy

    for part in parts:
        found = False

        # If current is a list (multiple objects at this level)
        if isinstance(current, list):
            for item in current:
                if item['type'].lower() == part.lower():  # Case-insensitive match
                    current = item
                    found = True
                    break

        # If current is a single object
        elif isinstance(current, dict):
            # Check datapoints
            for dp in current['datapoints']:
                if dp['type'] and dp['type'].lower() == part.lower():
                    return dp

            # Check children
            for child in current['children']:
                if child['type'].lower() == part.lower():
                    current = child
                    found = True
                    break

        if not found:
            return None

    return current


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
