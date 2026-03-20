<script setup lang="ts">

import GameBoard from './components/GameBoard.vue';
import type { IPoint } from './logic/models';
import { useGameStart, useGameStats, useMakeTurn } from './logic/services/apiService';
import { socketState } from './logic/services/socketService';

const {playerName, boardData, trackingData, getPlayerInfo} = useGameStart();
const { makeTurn } = useMakeTurn();
const { stats, getGameStats } = useGameStats();



const boardClikced = async (point: IPoint) => {
  await makeTurn(point);
  await getGameStats();
}

const connect = async () => { 
  await getPlayerInfo();
  await getGameStats();
}

</script>

<template>
  <h1>Battleship game: {{ socketState.connected ? 'Connected' : 'Disconnected' }}</h1>

  <div class="main-layout">

    <div class="boards-layout">

      <GameBoard :player-name="playerName" :board-data="boardData"></GameBoard>
      <GameBoard :player-name="'Enemy'" :board-data="trackingData" @board-clicked="boardClikced"></GameBoard>

      <div class="stats">
        <div></div>
        <div class="header">[Stats]</div>

        <div></div>
        <div class="stat-data">[My Afloat]</div>
        <div class="stat-data">[Enemy Killed]</div>

        <div v-for="(item, index) in stats" :key="index" style="display: contents;">
          <div>{{ item.shipType }}:</div>
          <div class="stat-data">{{ item.playerOneCount }}</div>
          <div class="stat-data">{{ item.playerTwoCount }}</div>          
        </div>

      </div>
    </div>

    <div class="actions">
      <button class="player-button" @click="connect()">Start</button>
    </div>

    <div class="log-area"> <textarea style="min-width: 700px; min-height: 250px;" v-model="socketState.logs"></textarea></div>

  </div>
</template>

<style scoped>
  .stats {
    display: grid;
    gap: 1px;
    width: max-content;
    height: max-content;
    grid-template-columns: 1fr 1fr 1fr;
  }

  .stats .header {
    display: flex;
    align-items: center;
    justify-content: center;
    grid-column: 2 / span 2;
  }

  .stats .stat-data {
    display: flex;
    align-items: center;
    justify-content: center;
  }

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
