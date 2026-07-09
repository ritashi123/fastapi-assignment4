from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

events = [
    {
        "id": 1,
        "title": "Python Backend Workshop",
        "category": "Workshop",
        "location": "Hyderabad",
        "date": "2026-07-20",
        "organizer": "Code Club",
        "capacity": 100,
        "is_open": True
    },
    {
        "id": 2,
        "title": "Tech Career Fair",
        "category": "Career",
        "location": "Bengaluru",
        "date": "2026-07-25",
        "organizer": "Career Connect",
        "capacity": 300,
        "is_open": True
    },
    {
        "id": 3,
        "title": "Cultural Evening",
        "category": "Cultural",
        "location": "Hyderabad",
        "date": "2026-08-02",
        "organizer": "Arts Forum",
        "capacity": 500,
        "is_open": False
    }
]

class EventCreate(BaseModel):
    title: str
    category: str
    location: str
    date: str
    organizer: str
    capacity: int
    is_open: bool

class EventUpdate(BaseModel):
    title: str
    category: str
    location: str
    date: str
    organizer: str
    capacity: int
    is_open: bool

class EventPatch(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    date: Optional[str] = None
    organizer: Optional[str] = None
    capacity: Optional[int] = None
    is_open: Optional[bool] = None

@app.get("/")
def read_root():
    return {"message": "Events API is running"}

@app.get("/events")
def read_events(
    category: Optional[str] = None,
    location: Optional[str] = None,
    is_open: Optional[bool] = None
):
    filtered_events = events
    if category is not None:
        filtered_events = [e for e in filtered_events if e["category"].lower() == category.lower()]
    if location is not None:
        filtered_events = [e for e in filtered_events if e["location"].lower() == location.lower()]
    if is_open is not None:
        filtered_events = [e for e in filtered_events if e["is_open"] == is_open]
    return filtered_events

@app.get("/events/{event_id}")
def read_event(event_id: int):
    for event in events:
        if event["id"] == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@app.post("/events", status_code=201)
def create_event(event: EventCreate):
    new_id = max([e["id"] for e in events], default=0) + 1
    new_event = event.model_dump()
    new_event["id"] = new_id
    events.append(new_event)
    return {"message": "Event created successfully", "event": new_event}

@app.put("/events/{event_id}")
def update_event(event_id: int, event: EventUpdate):
    for i, existing_event in enumerate(events):
        if existing_event["id"] == event_id:
            updated_event = event.model_dump()
            updated_event["id"] = event_id
            events[i] = updated_event
            return updated_event
    raise HTTPException(status_code=404, detail="Event not found")

@app.patch("/events/{event_id}")
def patch_event(event_id: int, event: EventPatch):
    for i, existing_event in enumerate(events):
        if existing_event["id"] == event_id:
            update_data = event.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                existing_event[key] = value
            return existing_event
    raise HTTPException(status_code=404, detail="Event not found")

@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    for i, existing_event in enumerate(events):
        if existing_event["id"] == event_id:
            deleted_event = events.pop(i)
            return {"message": "Event deleted successfully", "event": deleted_event}
    raise HTTPException(status_code=404, detail="Event not found")
