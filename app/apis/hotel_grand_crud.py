from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from databases.postgresql import get_db
from models.bases.object_base import Object
from models.bases.datapoint_base import Datapoint
from models.objects.hotel_grand_objects import Building, Floor, Room, Device
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class ObjectBase(BaseModel):
    name: str
    location_details: Optional[dict] = None
    parent_object_id: Optional[int] = None


class ObjectCreate(ObjectBase):
    pass


class ObjectResponse(ObjectBase):
    id: int
    type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DatapointBase(BaseModel):
    value: str
    unit: Optional[str] = None


class DatapointCreate(DatapointBase):
    pass


class DatapointResponse(DatapointBase):
    datapoint_id: int
    object_FK: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# CRUD operations for Buildings
@app.post("/buildings/", response_model=ObjectResponse)
def create_building(building: ObjectCreate, db: Session = Depends(get_db)):
    db_building = Building(
        name=building.name,
        location_details=building.location_details
    )
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


@app.get("/buildings/", response_model=List[ObjectResponse])
def read_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buildings = db.query(Building).offset(skip).limit(limit).all()
    return buildings


@app.get("/buildings/{building_id}", response_model=ObjectResponse)
def read_building(building_id: int, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.id == building_id).first()
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


# Similar CRUD operations for floors, rooms, and devices
@app.post("/floors/", response_model=ObjectResponse)
def create_floor(floor: ObjectCreate, db: Session = Depends(get_db)):
    db_floor = Floor(
        name=floor.name,
        location_details=floor.location_details,
        parent_object_id=floor.parent_object_id
    )
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor


# Example of a hierarchical query
@app.get("/buildings/{building_id}/hierarchy")
def get_building_hierarchy(building_id: int, db: Session = Depends(get_db)):
    building = db.query(Building).filter(Building.id == building_id).first()
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    result = {
        "id": building.id,
        "name": building.name,
        "type": building.type,
        "floors": []
    }

    for floor in building.get_floors():
        floor_data = {
            "id": floor.id,
            "name": floor.name,
            "type": floor.type,
            "rooms": []
        }

        for room in floor.get_rooms():
            room_data = {
                "id": room.id,
                "name": room.name,
                "type": room.type,
                "devices": []
            }

            for device in room.get_devices():
                device_data = {
                    "id": device.id,
                    "name": device.name,
                    "type": device.type
                }
                room_data["devices"].append(device_data)

            floor_data["rooms"].append(room_data)

        result["floors"].append(floor_data)

    return result
