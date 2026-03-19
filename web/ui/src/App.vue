<script setup lang="ts">

import { ref } from 'vue';
import axios from 'axios';
import GameBoard from './components/GameBoard.vue';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/game',
  timeout: 10000
});

// test
const playerName = ref('')
const boardData = ref(Array(10).fill(0).map(() => Array(10).fill(0)))
const trackingData = ref(Array(10).fill(0).map(() => Array(10).fill(0)))

const getPlayerInfo = async () => {
  const response = apiClient.post('/start');
  const data = (await response).data;

  playerName.value = data.name;
  boardData.value = data.board;
  trackingData.value = data.trackingBoard;

  console.log(data);

  const xx = apiClient.post('/make_turn', { row: 2, column: 3 });

  const dd = (await xx).data;
  console.log(dd);
}

const connect = () => {
  getPlayerInfo();
}

</script>

<template>
  <h1>Battleship game</h1>

  <div class="main-layout">

    <div class="boards-layout">

      <GameBoard :player-name="playerName" :board-data="boardData"></GameBoard>
      <GameBoard :board-data="trackingData"></GameBoard>

      <div>[Stats]</div>
    </div>

    <div class="actions">
      <button class="player-button" @click="connect()">Start</button>
    </div>

    <div class="log-area"> <textarea style="min-width: 320px;"></textarea></div>

  </div>
</template>

<style scoped>

  .boards-layout {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    
    gap: 2vw;
  }

  .main-layout {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 64px 1fr;
    gap: 1px;
  }

  .actions {
    margin: 32px;

    .player-button {

      background-color: #2196f3; 
      color: #ffffff;           
      border: 2px solid #333333; 
      

      font-family: 'Courier New', Courier, monospace;
      font-weight: bold;
      text-transform: uppercase;
      
      padding: 8px 20px;
      border-radius: 0;
      cursor: pointer;
      transition: all 0.2s ease;
    }  

    .player-button:hover {
      background-color: #4682b4;
      color: #ffffff;         
      border-color: #000000;
    }    
  }

 .log-area {
    margin: 32px;
  }  

</style>
