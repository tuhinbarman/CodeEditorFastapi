from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette import status
from database import *
from utils import generator
from models import Rooms
from schemas.room import RoomRequest
from datetime import datetime

router = APIRouter(prefix='',tags=['rooms'])


@router.get(path='/rooms')
async def get_rooms(db : Session = Depends(get_db)):

    try:
        room_data = db.query(Rooms).with_entities(
                Rooms.id, Rooms.createdby, Rooms.no_of_users_allowed, Rooms.code
            ).all()
        
        result = []
        for room in generator(room_data):
            result.append({
                'roomid' : room.id,
                'createdby' : room.createdby,
                'no_of_users_allowed' : room.no_of_users_allowed,
                'code' : room.code
            })

        return JSONResponse(content={'data' : result,'message' : 'Success'},status_code=200)

    except Exception as err:
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)

@router.post(path='/rooms')
async def create_room(request : RoomRequest,db : Session = Depends(get_db)):
    try:
        request_data = RoomRequest.model_dump()

        new_room = Rooms(
            createdby = request_data['username'],
            no_of_users_allowed = request_data['no_of_users_allowed'],
            code = request_data['code'],
            createddate = datetime.utcnow()
        )

        db.add(new_room)
        db.commit()
        db.refresh(new_room)

        result = {
            'room_id' : new_room.id,
            'createdby' : new_room.createdby,
            'no_of_users_allowed' : new_room.no_of_users_allowed,
            'code' : new_room.code,
            'createddate' : new_room.createddate.isoformat()
        }

        return JSONResponse(content={'data' : result,'message' : 'Success'},status_code=200)

    except Exception as err:
        db.rollback()
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)


    
