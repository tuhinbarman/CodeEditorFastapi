from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json

class WebsocketManager:
    def __init__(self):
        self.rooms = {}

    async def connect(self, websocket: WebSocket, room_id: str,room_count : int):
        
        if room_id not in self.rooms:
            self.rooms[room_id] = set()

        if room_count < len(self.rooms[room_id]):
            await websocket.accept()
            await websocket.send_json({'data' : "Room is full",'status_code' : 400})
            await websocket.close(code=1008, reason="Room is full")
            return False
            
        await websocket.accept()
        self.rooms[room_id].add(websocket)
        return True

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.rooms:
            self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:  
                del self.rooms[room_id]

    async def broadcast(self, message: str, room_id: str, sender: WebSocket = None):
        
        if room_id not in self.rooms:
            return

        disconnected = []
        for connection in self.rooms[room_id]:
            if sender and connection == sender:
                continue  
            try:
                await connection.send_json({'data' : message,'status_code' : 200})
                # await connection.send_text(message)
            except WebSocketDisconnect:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn, room_id)

class AutoCompleteManager():

    def get_response(self,code : str):
        if not code:
            return ""

        return "Test autocomplete code" 