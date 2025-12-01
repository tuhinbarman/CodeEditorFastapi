import { useState,useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addRoom, selectRoom } from "../features/roomsSlice";

export default function LeftSidebar() {
  const [showForm, setShowForm] = useState(false);
  const [username, setUsername] = useState("");
  const [allowedUsers, setAllowedUsers] = useState(1);
  const rooms = useSelector((state) => state.rooms.list);
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchRooms = async () => {
      const res = await fetch("http://localhost:8000/rooms");
      const data = await res.json();
      const rooms = data?.data ? data?.data : []

      // add all rooms into redux store
      rooms.forEach(room => dispatch(addRoom(room)));
    };

    fetchRooms();
  }, [dispatch]);

  const createRoom = async () => {
    const response = await fetch("http://localhost:8000/rooms", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username,
        no_of_users_allowed: allowedUsers,
        code : ""
      }),
    });

    const data = await response.json();
    dispatch(addRoom(data));
    setShowForm(false);
  };

  return (
    <div className="h-full w-48 bg-gray-100 flex flex-col p-3 rounded-l-xl border-r">
      <button
        onClick={() => setShowForm(true)}
        className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded"
      >
        + Create Room
      </button>

      {showForm && (
        <div className="bg-white p-3 mt-3 rounded shadow flex flex-col gap-2">
          <input
            className="border p-1 rounded"
            placeholder="Username"
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="number"
            min="1"
            className="border p-1 rounded"
            placeholder="Allowed Users"
            onChange={(e) => setAllowedUsers(e.target.value)}
          />
          <button
            onClick={createRoom}
            className="bg-green-600 hover:bg-green-700 text-white p-1 rounded"
          >
            Create
          </button>
        </div>
      )}

      <div className="mt-4 flex flex-col gap-2">
        {rooms.map((room) => (
          <div
            key={room.roomid}
            onClick={() => dispatch(selectRoom(room))}
            className="p-2 cursor-pointer bg-white hover:bg-gray-200 rounded border"
          >
            <b>{room.roomid}</b> <br />
            <span className="text-xs text-gray-600">{room.createdby}</span>
          </div>
        ))}
      </div>
    </div>
  );
}