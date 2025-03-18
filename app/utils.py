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
def resolve_path_by_type(objects, path: str) -> Union[dict, List[dict], None]:
    parts = path.split('.')
    current_level = objects

    # Traverse the path for object types
    for i, part in enumerate(parts):
        next_level = []
        is_last = (i == len(parts) - 1)

        for obj in current_level:
            if obj["type"].lower() == part.lower():
                if is_last and not any(p["type"].lower() == part.lower() for p in obj["datapoints"]):
                    # Path ends with object type
                    next_level.append(obj)
                elif not is_last:
                    # Continue traversing children
                    children = [o for o in objects if o.get("parent_id") == obj["id"]]
                    next_level.extend(children)
            if is_last and any(p["type"].lower() == part.lower() for p in obj["datapoints"]):
                # Path ends with datapoint type
                datapoints = [dp for dp in obj["datapoints"] if dp["type"].lower() == part.lower()]
                return datapoints

        if not next_level and not is_last:
            return []
        current_level = next_level

    return current_level


def find_by_path(data, path_string):
    """
    Traverse hierarchical data following a path of "type" field values using dot notation.
    Returns all matches found.

    Args:
        data: The root node of the hierarchical data
        path_string: String with dot-delimited type values defining the path to follow (e.g., "folder.document")

    Returns:
        List of all nodes that match the complete path
    """
    # Convert the dot-delimited string to a list of path components
    path = path_string.split(".")

    def traverse(node, path_parts):
        matches = []

        if not path_parts:
            return [node]

        current_type = path_parts[0]
        remaining_path = path_parts[1:]

        # Check if current node matches the first type in path
        if node.get("type") == current_type:
            if not remaining_path:
                matches.append(node)
            else:
                # If we have more path to traverse, look in children
                if "children" in node and isinstance(node["children"], list):
                    for child in node["children"]:
                        matches.extend(traverse(child, remaining_path))

        # If we're at root level, also search all children for direct matches
        elif not remaining_path and "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                if child.get("type") == current_type:
                    matches.append(child)

        # If first element doesn't match, try to search all children for the full path
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                matches.extend(traverse(child, path_parts))

        return matches

    return traverse(data, path)


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
