import { useEffect, useRef, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { selectRoom } from "../features/roomsSlice";
import CodeMirror from "@uiw/react-codemirror";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import { Box, Card, CardContent, Typography, Button } from "@mui/material";
import MeetingRoomIcon from "@mui/icons-material/MeetingRoom";
import suggestionExtension from "../utils/suggestionExtension"

export default function CodeEditor() {
  const room = useSelector((state) => state.rooms.selectedRoom);
  const wsRef = useRef(null);
  const textareaRef = useRef(null);
  const [code, setCode] = useState("// Start typing collaboratively...");
  const [suggestion, setSuggestion] = useState(""); // autocomplete suggestion
  const debounceRef = useRef(null);
  const dispatch = useDispatch()
  const [error,setError] = useState("") 
  const [extensions, setExtensions] = useState([]);


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

    useEffect(() => {
  setExtensions([suggestionExtension(suggestion)]);
}, [suggestion]);

  const handleTyping = (value) => {
    setCode(value);
    setSuggestion(""); 

    
    if (wsRef.current?.readyState === 1) wsRef.current.send(value);

    
    if (debounceRef.current) clearTimeout(debounceRef.current);

    debounceRef.current = setTimeout(async () => {
      try {
        const res = await fetch("http://localhost:8000/autocomplete", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ room_id : room?.roomid,
            code: value }),
        });

        const result = await res.json();
        if (result?.data?.prompt) {
          const lastWord = value.split(/\s/).pop() || "";
          const remaining = result.data.prompt.replace(lastWord, "");
          setSuggestion(remaining);

          // Show suggestion inside textarea using selection
          if (textareaRef.current && remaining) {
            textareaRef.current.value = value + remaining;
            textareaRef.current.setSelectionRange(value.length, value.length + remaining.length);
          }
        }
      } catch (err) {
        setSuggestion("");
      }
    }, 600);
  };

  if (!room) {
  return (
    <Box
      sx={{
        height: "100vh",
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f3f4f6",
        p: 2,
      }}
    >
      <Card
        sx={{
          minWidth: 380,
          p: 3,
          borderRadius: 3,
          textAlign: "center",
          background: "#ffffff",
          boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
        }}
      >
        <CardContent>
          <MeetingRoomIcon sx={{ fontSize: 50, color: "#3b82f6", mb: 1 }} />

          <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
            No Room Selected
          </Typography>

          <Typography variant="body2" sx={{ opacity: 0.7, mb: 3 }}>
            Select a room from the left sidebar and start coding collaboratively.
          </Typography>

          <Button
            variant="contained"
            sx={{
              backgroundColor: "#3b82f6",
              textTransform: "none",
              px: 3,
              py: 1,
              borderRadius: 2,
              fontWeight: 600,
            }}
            onClick={() => {}}
          >
            Choose a Room
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}

  return (
    
      <CodeMirror
        value={code}
        height="100vh"
        theme={vscodeDark}
        onChange={handleTyping}
        extensions={extensions}
        className="flex-1"
      />
  );
}
