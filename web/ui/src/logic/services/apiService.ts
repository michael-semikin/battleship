import axios from "axios";
import { ref } from "vue";
import type { IGameStat, IPoint } from "../models";

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/game',
  timeout: 1000000
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

        const response = apiClient.get('/update_board', { withCredentials: true });
        const data = (await response).data;

        if (!data) {
            return;
        }

        playerName.value = data.name;
        boardData.value = data.board;
        trackingData.value = data.trackingBoard;
    }

    return { playerName, boardData, trackingData, makeTurn }
}

export function useGameStats() {
    const stats = ref<IGameStat[]>([])

    const getGameStats = async () => {
        const response = apiClient.get('/get_stats', { withCredentials: true });
        const data = (await response).data as IGameStat[];

        if (!data) {
            return;
        }
        
        stats.value = data.map(x => ({
            shipType: x.shipType,
            playerOneCount: x.playerOneCount,
            playerTwoCount: x.playerTwoCount
        }));
    }

    return { stats, getGameStats }
}

export function useGameOver() {
    const gameOver = async () => {
        const response = apiClient.post('/set_game_over', {}, { withCredentials: true });
        await response;      
    }

    return { gameOver }
}