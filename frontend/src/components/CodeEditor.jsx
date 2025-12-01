import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {selectRoom} from "../features/roomsSlice";

export default function CodeEditor() {
  const room = useSelector((state) => state.rooms.selectedRoom);
  const wsRef = useRef(null);
  const [code, setCode] = useState("// Start typing collaboratively...");
  const [error, setError] = useState("");
  const dispatch = useDispatch()

  useEffect(() => {
  if (!room) return;

  const ws = new WebSocket(`ws://localhost:8000/ws/${room.roomid}`);
  wsRef.current = ws;

  ws.onopen = () => setError("");

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);  // parse JSON

      if (data.status_code === 200) {
        setCode(data.data);
      } else if (data.status_code === 400) {
        alert(data.data); 
         // room full, etc.
        dispatch(selectRoom(null))
      }
    } catch (err) {
      console.error("Invalid JSON received:", event.data);
    }
  };

  ws.onclose = () => console.log("Socket closed");
  ws.onerror = () => setError("WebSocket connection failed");

  return () => ws.close();
}, [room]);

  const handleTyping = (e) => {
    const value = e.target.value;
    setCode(value);

    if (wsRef.current?.readyState === 1) {
      wsRef.current.send(value); 
    }
  };

  if (!room)
    return (
      <div className="flex items-center justify-center w-full h-full text-gray-500 text-lg">
        Select a room to start coding...
      </div>
    );

  return (
    <div className="w-full h-full flex flex-col">
      {error && <div className="p-2 bg-red-600 text-white text-sm">{error}</div>}

      <textarea
        value={code}
        onChange={handleTyping}
        className="w-full h-full bg-gray-900 text-white p-4 rounded-md outline-none resize-none"
        style={{ fontFamily: "monospace", fontSize: "15px", lineHeight: "20px" }}
      />
    </div>
  );
}
