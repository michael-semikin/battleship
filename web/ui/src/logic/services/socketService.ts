import { io } from "socket.io-client";
import { reactive } from "vue";

const URL = 'http://localhost:8000';

export const socketState = reactive({
  connected: false,
  logs: [],
  winner: ''
});

export const socket = io(URL, {
  transports: ["websocket"] 
});

socket.on('connect', () => {
  socketState.connected = true;
  socketState.logs = [];
  socketState.winner = '';
});

socket.on('disconnect', () => {
  socketState.connected = false;
});

socket.on('log_sent', (data) => {
  socketState.logs = data;
});

socket.on('game_over', (data) => {
  socketState.winner = data;
});

