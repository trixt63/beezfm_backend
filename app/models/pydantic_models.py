from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, List, Any

# ---- Object Models ----
class ObjectBase(BaseModel):
    """Base model for object data"""
    name: str
    type: str
    location_details: Optional[Dict[str, Any]] = None
    parent_object_id: Optional[int] = None

class ObjectCreate(ObjectBase):
    """Model for creating a new object"""
    pass

class ObjectUpdate(BaseModel):
    """Model for updating an existing object"""
    name: Optional[str] = None
    location_details: Optional[Dict[str, Any]] = None
    parent_object_id: Optional[int] = None

class ObjectInDB(ObjectBase):
    """Model for object as stored in the database"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DatapointBase(BaseModel):
    """Base model for datapoint data"""
    object_FK: int
    value: str
    unit: Optional[str] = None

class DatapointCreate(DatapointBase):
    """Model for creating a new datapoint"""
    pass

class DatapointUpdate(BaseModel):
    """Model for updating an existing datapoint"""
    value: Optional[str] = None
    unit: Optional[str] = None

class DatapointInDB(DatapointBase):
    """Model for datapoint as stored in the database"""
    datapoint_id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ObjectWithChildren(ObjectInDB):
    """Model for object with its children"""
    children: Optional[List[ObjectInDB]] = None

class ObjectWithDatapoints(ObjectInDB):
    """Model for object with its datapoints"""
    datapoints: Optional[List[DatapointInDB]] = None

class ObjectWithRelations(ObjectInDB):
    """Model for object with both children and datapoints"""
    children: Optional[List[ObjectInDB]] = None
    datapoints: Optional[List[DatapointInDB]] = None
