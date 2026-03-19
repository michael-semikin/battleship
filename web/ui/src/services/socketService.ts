import { io } from "socket.io-client";
import { reactive } from "vue";

const URL = 'http://localhost:8000';

export const state = reactive({
  connected: false,
  fooEvents: [],
  barEvents: []
});

export const socket = io(URL);

socket.on("connect", () => {
  state.connected = true;
});

socket.on("disconnect", () => {
  state.connected = false;
});