from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint, JSON, DateTime, Text

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.database import Base

# SQLAlchemy Models
class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    location_details = Column(JSON, nullable=True)
    parent_object_id = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    children = relationship("Object",
                           cascade="all, delete-orphan",
                           backref=ForeignKey("parent", remote_side=[id]))
    datapoints = relationship("Datapoint", back_populates="object", cascade="all, delete-orphan")

class Datapoint(Base):
    __tablename__ = "datapoints"

    datapoint_id = Column(Integer, primary_key=True, index=True)
    object_FK = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"), nullable=False)
    value = Column(Text, nullable=False)
    unit = Column(String(50), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    object = relationship("Object", back_populates="datapoints")

# Pydantic Models for API
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