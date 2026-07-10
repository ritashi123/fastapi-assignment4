from fastapi import FastAPI,HTTPException
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

@app.get('/')
def home():
    return{
        "message" : "Welcome to the home page!"
    }

@app.get('/events')
def get_events():
    return events

@app.get('/events/category')
def get_event_by_category(category : str):
    result = []
    for event in events:
        if event["category"] == category:
            result.append(event)
    return result

@app.get('/events/location')
def get_event_by_location(location : str):
    result = []
    for event in events:
        if event["location"] == location:
            result.append(event)
    return result

@app.get('/events/status')
def get_event_by_status(is_open : bool):
    result = []
    for event in events:
        if event["is_open"] == is_open:
            result.append(event)
    return result

@app.get('/events/{event_id}')
def get_event_by_id(event_id : int):
    for event in events:
        if event["id"] == event_id:
            return event
    raise HTTPException(status_code = 404 , detail = "EVENT NOT FOUND")

class EventCreate(BaseModel):
    title : str
    category : str
    location : str
    date : str
    organizer : str
    capacity : int
    is_open : bool

@app.post('/events',status_code=201)
def create_event(event:EventCreate):
    new_id = max((event["id"] for event in events),default=0)+1
    new_event={
        "id" : new_id,
        "title" : event.title,
        "category" : event.category,
        "location" : event.location,
        "date" : event.date,
        "organizer" : event.organizer,
        "capacity" : event.capacity,
        "is_open" : event.is_open
    }
    events.append(new_event)
    return {
        "message": "Event Created Successfully",
        "event": new_event
    }
   


class EventUpdate(BaseModel):
    title : str
    category : str
    location : str
    date : str
    organizer : str
    capacity : int
    is_open : bool

@app.put('/events/{event_id}')
def update_event(event_id:int , event:EventUpdate):
    for existing_event in events:
        if existing_event["id"] == event_id:
            existing_event.update(event.model_dump())
            return{
                "message" : "Event Updated Succesfully",
                "event" : existing_event
            }
    raise HTTPException(status_code=404 , detail="EVENT NOT FOUND!!")

class EventPatch(BaseModel):
    title : Optional[str] = None
    category : Optional[str] = None
    location : Optional[str] = None
    date : Optional[str] = None
    organizer : Optional[str] = None
    capacity : Optional[int] = None
    is_open : Optional[bool] = None

@app.patch('/events/{event_id}')
def event_patch(event_id : int , event : EventPatch):
    for existing_event in events:
        if existing_event["id"] == event_id:
            if event.title is not None:
                existing_event["title"] = event.title
            if event.category is not None:
                existing_event["category"] = event.category
            if event.location is not None:
                existing_event["location"] = event.location
            if event.date is not None:
                existing_event["date"] = event.date
            if event.organizer is not None:
                existing_event["organizer"] = event.organizer
            if event.capacity is not None:
                existing_event["capacity"] = event.capacity
            if event.is_open is not None:
                existing_event["is_open"] = event.is_open
            return {
                "message" : "ATTRIBUTE OF EVENT UPDATED SUCESSFULLY!!",
                "event" : existing_event
            }
    raise HTTPException(status_code=404,detail="EVENT NOT FOUND!!")

@app.delete('/events/{event_id}')
def delete_event(event_id:int):
    for existing_event in events:
        if existing_event["id"] == event_id:
            events.remove(existing_event)
            return {
            "message" : "EVENT DELETED SUCESSFULLY!!",
            "event" : existing_event
            }
       
    raise HTTPException(status_code=404, detail="EVENT NOT FOUND!!")
