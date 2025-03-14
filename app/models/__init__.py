from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# ---- Object Models ----

class ObjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., pattern="^(building|floor|room|device)$")  # Matches type constraint
    location_details: Optional[dict] = None

class ObjectCreate(ObjectBase):
    parent_id: Optional[int] = None

class Object(ObjectBase):
    id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    children: Optional[List["Object"]] = None  # Recursive hierarchy
    datapoints: Optional[List["Datapoint"]] = None  # Many-to-many with Datapoint

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy ORM
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Serialize timezone-aware datetime
        }

# ---- Datapoint Models ----

class DatapointBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)  # Assuming 255, not 2555
    value: str = Field(..., min_length=1)
    unit: Optional[str] = Field(None, max_length=50)
    is_fresh: bool = True

class DatapointCreate(DatapointBase):
    pass  # No additional fields needed for creation

class Datapoint(DatapointBase):
    id: int
    created_at: datetime
    updated_at: datetime
    objects: Optional[List["Object"]] = None  # Many-to-many with Object

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# ---- ObjectDatapoint Models ----

class ObjectDatapointBase(BaseModel):
    object_FK: int
    datapoint_FK: int

class ObjectDatapointCreate(ObjectDatapointBase):
    last_updated: datetime = Field(default_factory=lambda: datetime.now())
    is_fresh: bool = True
    metadata: Optional[dict] = None

class ObjectDatapoint(ObjectDatapointBase):
    id: int
    last_updated: datetime
    is_fresh: bool
    metadata: Optional[dict] = None
    object: Optional["Object"] = None  # Optional relationship
    datapoint: Optional["Datapoint"] = None  # Optional relationship

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Resolve forward references for recursive types
Object.update_forward_refs()
Datapoint.update_forward_refs()
ObjectDatapoint.update_forward_refs()
