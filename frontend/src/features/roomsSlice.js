import { createSlice } from "@reduxjs/toolkit";

const roomsSlice = createSlice({
  name: "rooms",
  initialState: {
    list: [],
    selectedRoom: null,
  },
  reducers: {
    addRoom(state, action) {
      state.list.push(action.payload);
    },
    selectRoom(state, action) {
      state.selectedRoom = action.payload;
    },
  },
});

export const { addRoom, selectRoom } = roomsSlice.actions;
export default roomsSlice.reducer;