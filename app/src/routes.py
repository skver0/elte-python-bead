from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer

router = APIRouter()
efm = EventFileManager()

@router.get("/events", response_model=List[Event])
async def get_all_events():
    return efm.read_events_from_file()


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    filtered_events = []

    for event in efm.read_events_from_file():
        if date and date != event["date"]:
            continue
        if organizer and organizer != event["organizer"]["name"]:
            continue
        if status and status != event["status"]:
            continue
        if event_type and event_type != event["type"]:
            continue

        filtered_events.append(event)

    return filtered_events


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    for event in efm.read_events_from_file():
        if event["id"] == event_id:
            return event
        
    raise HTTPException(status_code=404, detail="Event not found")

@router.post("/events", response_model=Event)
async def create_event(event: Event):
    # check if event already exists
    events = efm.read_events_from_file()
    for e in events:
        if e["id"] == event.id:
            raise HTTPException(status_code=400, detail="Event already exists")

    # create event
    events.append(event.dict())
    efm.write_events_to_file(events)
    
    return event

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    # check if event exists
    events = efm.read_events_from_file()
    for e in events:
        if e["id"] == event_id:
            # remove the id from the event object
            event.id = event_id
            
            # update the event
            e.update(event.dict())
            efm.write_events_to_file(events)
            return event

    raise HTTPException(status_code=404, detail="Event not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    # check if event exists
    events = efm.read_events_from_file()
    for e in events:
        if e["id"] == event_id:
            events.remove(e)
            efm.write_events_to_file(events)
            return {"message": "Event deleted successfully"}

    raise HTTPException(status_code=404, detail="Event not found")


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    list_of_joiners = EventAnalyzer().get_joiners_multiple_meetings_method(efm.read_events_from_file())
    if not list_of_joiners:
        return {"message": "No joiners attending at least 2 meetings"} 
    return list_of_joiners