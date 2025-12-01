from fastapi import APIRouter,Depends,WebSocket,WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette import status
from database import *
from utils import generator
from models import Rooms
from schemas.room import RoomRequest,AutoCompleteRequest
from datetime import datetime
from controller.controller import WebsocketManager,AutoCompleteManager

router = APIRouter(prefix='',tags=['rooms'])
manager = WebsocketManager()
autocomplete_manager = AutoCompleteManager()


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
        
        request_data = request.model_dump()

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
        print(err)
        db.rollback()
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)


@router.websocket(path = '/ws/{room_id}')
async def websocket_endpoint(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):

    try:

        room = db.query(Rooms).filter(Rooms.id == room_id).first()
        if not room:
            await websocket.close(code=1008, reason="Room not found")
        
        room_max_count = room.no_of_users_allowed
        

        connect_status = await manager.connect(websocket=websocket,room_id=room_id,room_count=room_max_count)

        if not connect_status:
            websocket.close(code=1008, reason="Room is full")

        try:
            while True:
                data = await websocket.receive_text()  
                await manager.broadcast(data, room_id)

        except WebSocketDisconnect:
            manager.disconnect(websocket, room_id)
       
    except Exception as err:
        manager.disconnect(websocket, room_id)
        await websocket.close(code=1011, reason="Internal server error")

@router.post('/autocomplete')
async def autocomplete(request : AutoCompleteRequest,db : Session = Depends(get_db)):
    try:
        request_data = request.model_dump()
        autocomplete_response = autocomplete_manager.get_response(request_data['code'])
        result = {
            'data' : {
                'code' : request_data['code'],
                'prompt' : autocomplete_response
            },
            'message' : 'Success'
        }

        return JSONResponse(content=result,status_code=200)

    except Exception as err:
        db.rollback()
        return JSONResponse(content = {'data' : 'Something went wrong!!','message' : 'Fail'},
                                       status_code=500)





    
