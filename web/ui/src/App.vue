<script setup lang="ts">

import { reactive } from 'vue';

enum CellState {
    Empty = 0,
    Ship = 1,
    Hit = 2,
    Miss = 3
}

enum ShipOrientation {
  None = 0,
  Horizontal = 1,
  Vertical = 2,
}

enum ShipType {
  Scout,
  Destroyer,
  Cruiser,
  Battleship
}

interface IBoardCell {
  index: number
  cssClasses: string[]
}

// test
const board_data = Array(10).fill(0).map(() => Array(10).fill(0))
// test data

board_data[1] = [0 ,0 ,3, 0, 0, 0, 0, 1, 0, 0]
board_data[2] = [0 ,0 ,0, 0, 0, 0, 0, 2, 0, 0]
board_data[3] = [0 ,1 ,1, 1, 1, 0, 0, 1, 0, 0]
board_data[4] = [0 ,0 ,0, 0, 0, 0, 0, 1, 0, 0]

const getBoardCells = () => {
  const cells: IBoardCell[] = [];
  const matrix = board_data;

  for (let row = 0; row < 10; row++) {
    for (let col = 0; col < 10; col++) {
      const cellIndex = col + row * 10;

      const cell: IBoardCell =  {
        index: cellIndex,
        cssClasses: ['field-cell']
      }

      cells.push(cell);

      switch(matrix[row][col]) {
        case CellState.Empty:
          cell.cssClasses.push('empty')
          break;
        case CellState.Ship:
          cell.cssClasses.push('ship')
          break;
        case CellState.Hit:
          cell.cssClasses.push('fire')
          break;          
        case CellState.Miss:
          cell.cssClasses.push('miss')
          break;
      }
    }
  }

  return cells;
}

</script>

<template>
  <h1>Battleship game</h1>

  <div class="main-layout">

    <div class="board-container">
      <div class="board-header"> [Player Board] </div>
      <div class="letters">
        <div class="letters-container">
          <div v-for="letter in 'abcdefghij'" :key="letter" class="field-cell">{{ letter }}</div>
        </div>
      </div>

      <div class="board">
        <div class="battlefield">
          <div v-for="cell in getBoardCells()" :key="cell.index" :class="cell.cssClasses">.</div>
        </div>
      </div>

      <div class="numbers">
        <div class="numbers-container">
          <div v-for="n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]" :key="n" class="field-cell">{{ n }}</div>
        </div>
      </div>

      <div class="empty_space"></div>
    </div>


    <div class="board-container">
      <div class="board-header"> [Enemy Board] </div>
      <div class="letters">
        <div class="letters-container">
          <div v-for="letter in 'abcdefghij'" :key="letter" class="field-cell">{{ letter }}</div>
        </div>
      </div>

      <div class="board">
        <div class="battlefield">
          <div v-for="cell in getBoardCells()" :key="cell.index" :class="cell.cssClasses">.</div>
        </div>
      </div>

      <div class="numbers">
        <div class="numbers-container">
          <div v-for="n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]" :key="n" class="field-cell">{{ n }}</div>
        </div>
      </div>

      <div class="empty_space"></div>
    </div>

    <div>Stats</div>
  </div>

</template>

<style scoped>
  .board-container {
    display: grid;
    gap: 1px;

    width: max-content;

    grid-template-areas:
      "empty_space    header"
      "empty_space    letters"
      "numbers        board";  
  }

  .board-header {
    grid-area: header;
    display: flex;
    align-items: center;
    justify-content: center;    
  }

  .letters {
    grid-area: letters;
  }

  .board {
    grid-area: board;
  }

  .empty_space {
    grid-area: empty_space;
  }

  .numbers {
    grid-area: numbers;
  }

  .letters-container {
    display: grid;
    gap: 1px;

    grid-template-columns: repeat(10, 32px);
    grid-template-rows: 32px;

    width: max-content;    
  }

  .numbers-container {
    display: grid;
    gap: 1px;

    grid-template-rows: repeat(10, 32px);
    grid-template-columns: 32px;

    width: max-content;    
  }
  
  .battlefield {
    display: grid;
    grid-template-columns: repeat(10, 32px);
    grid-template-rows: repeat(10, 32px);
    gap: 1px;

    width: max-content;
  }

  .field-cell {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .field-cell.empty {
    background-color: #1e90ff;
    border: 1px solid #4682b4;
  }

  .field-cell.ship {
    background-color: red;
    border: 1px solid #ff6b6b;
  }

  .field-cell.fire {
    background-color: yellow;
    border: 1px solid yellow;
  }

  .field-cell.miss {
    background-color: black;
    border: 1px solid black;
  }

  .main-layout {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 2vw;
  }
</style>
