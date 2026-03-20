import { io } from "socket.io-client";
import { reactive } from "vue";

const URL = 'http://localhost:8000';

export const socketState = reactive({
  connected: false,
  logs: []
});

export const socket = io(URL, {
  transports: ["websocket"] 
});

socket.on('connect', () => {
  socketState.connected = true;
});

socket.on('disconnect', () => {
  socketState.connected = false;
});

socket.on('log_sent', (data) => {
  socketState.logs = data;
});

