import { configureStore } from "@reduxjs/toolkit";
import roomsReducer from "./features/roomsSlice";

export const store = configureStore({
  reducer: {
    rooms: roomsReducer,
  },
});