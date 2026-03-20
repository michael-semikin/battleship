<script setup lang="ts">

import GameBoard from './components/GameBoard.vue';
import type { IPoint } from './logic/models';
import { useGameStart, useMakeTurn } from './logic/services/apiService';

const {playerName, boardData, trackingData, getPlayerInfo} = useGameStart();
const { makeTurn } = useMakeTurn();

const boardClikced = async (point: IPoint) => {
  makeTurn(point);
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
      <GameBoard :player-name="'Enemy'" :board-data="trackingData" @board-clicked="boardClikced"></GameBoard>

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
