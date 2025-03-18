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
    parent_id: Optional[int] = None

class ObjectCreate(ObjectBase):
    """Model for creating a new object"""
    pass

class ObjectUpdate(BaseModel):
    """Model for updating an existing object"""
    name: Optional[str] = None
    type: Optional[str] = None
    parent_id: Optional[int] = None
    location_details: Optional[Dict[str, Any]] = None

class ObjectInDB(ObjectBase):
    """Model for object as stored in the database"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Datapoints
class DatapointCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the datapoint")
    value: Optional[str] = Field(None, description="Value of the datapoint")
    unit: Optional[str] = Field(None, max_length=50, description="Unit of measurement")
    is_fresh: Optional[bool] = Field(True, description="Whether the datapoint is fresh")
    type: Optional[str] = Field(None, max_length=255, description="Type of the datapoint")

    class Config:
        from_attributes = True

class DatapointUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    value: Optional[str] = None
    unit: Optional[str] = Field(None, max_length=50)
    is_fresh: Optional[bool] = None
    type: Optional[str] = Field(None, max_length=255)

    class Config:
        from_attributes = True

class DatapointResponse(BaseModel):
    id: int
    name: str
    value: Optional[str]
    unit: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_fresh: bool
    type: str
    object_id: Optional[int] = Field(None, description="ID of the associated object")

    class Config:
        from_attributes = True
