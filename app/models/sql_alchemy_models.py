from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint, JSON, DateTime, Text, Boolean, \
    UniqueConstraint

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.database import Base


# SQLAlchemy Models
class Object(Base):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("object.id", ondelete="CASCADE"), nullable=True)
    location_details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    # children = relationship("Object",
    #                        cascade="all, delete-orphan",
    #                        backref="parent_id",
    #                        remote_side=[id])
    # datapoints = relationship("Datapoint",
    #                           secondary="object_datapoint",
    #                           back_populates="object")


class Datapoint(Base):
    __tablename__ = "datapoint"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(2555), nullable=False)
    value = Column(Text, nullable=False)
    unit = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_fresh = Column(Boolean, default=True)
    type = Column

    # Relationships
    # objects = relationship("Object",
    #                        secondary="object_datapoint",
    #                        back_populates="datapoints")


class ObjectDatapoint(Base):
    __tablename__ = "object_datapoint"

    id = Column(Integer, primary_key=True, index=True)
    object_FK = Column(Integer, ForeignKey("object.id", ondelete="CASCADE"), nullable=False)
    datapoint_FK = Column(Integer, ForeignKey("datapoint.id", ondelete="CASCADE"), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (optional, for direct access)
    # object = relationship("Object", backref="object_datapoint_associations")
    # datapoint = relationship("Datapoint", backref="object_datapoint_associations")

    __table_args__ = (
        # Unique constraint to prevent duplicate object-datapoint pairs
        UniqueConstraint("object_FK", "datapoint_FK", name="unique_object_datapoint"),
    )
