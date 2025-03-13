from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Datapoint:
    __tablename__ = 'datapoints'

    datapoint_id = Column(Integer, primary_key=True)
    object_FK = Column(Integer, ForeignKey('objects.id', ondelete='CASCADE'), nullable=False)
    value = Column(String(255), nullable=False)
    unit = Column(String(50))
    timestamp = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    object = relationship("Object", back_populates="datapoints")

    def to_dict(self):
        return {
            'datapoint_id': self.datapoint_id,
            'object_FK': self.object_FK,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
