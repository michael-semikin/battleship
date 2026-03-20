import axios from "axios";
import { ref } from "vue";
import type { IPoint } from "../models";

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/game',
  timeout: 10000
});

const playerName = ref('')
const boardData = ref(Array(10).fill(0).map(() => Array(10).fill(0)))
const trackingData = ref(Array(10).fill(0).map(() => Array(10).fill(0)))

export function useGameStart() {
    const getPlayerInfo = async () => {
        const response = apiClient.post('/start', {}, { withCredentials: true });
        const data = (await response).data;

        playerName.value = data.name;
        boardData.value = data.board;
        trackingData.value = data.trackingBoard;        
    }

    return { playerName, boardData, trackingData, getPlayerInfo }
}

export function useMakeTurn() {
    const makeTurn = async (point: IPoint) => {
        const sendMakeTurn = apiClient.post('/make_turn', point, { withCredentials: true });
        await sendMakeTurn;

        const response = apiClient.post('/update_board', {}, { withCredentials: true });
        const data = (await response).data;

        playerName.value = data.name;
        boardData.value = data.board;
        trackingData.value = data.trackingBoard;
    }

    return { playerName, boardData, trackingData, makeTurn }
}