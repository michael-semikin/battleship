<script setup lang="ts">
import { CellState, type IBoardCell, type IPoint } from '@/logic/models';

defineProps<{
    playerName: string,
    boardData: number[][]
}>()

const emit = defineEmits<{
    boardClicked: [point: IPoint]
}>()

const getBoardCells = (matrix: number[][]) => {
  const cells: IBoardCell[] = [];

  for (let row = 0; row < 10; row++) {
    for (let col = 0; col < 10; col++) {
      const cellIndex = col + row * 10;

      const cell: IBoardCell =  {
        index: cellIndex,
        cssClasses: ['field-cell'],
        dataRow: row,
        dataColumn: col
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

const onBoardClicked = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    const cell = target.closest('.field-cell');
    
    if (cell instanceof HTMLElement) {
        const row = Number(cell.dataset.row);
        const column = Number(cell.dataset.column);
        
        emit('boardClicked', {
            row,
            column
        });
    }
}

</script>

<template>
    <div class="board-container">
        <div class="board-header"><span v-if="playerName">[{{ playerName }}'s Board]</span></div>
        <div class="letters">
            <div class="letters-container">
            <div v-for="letter in 'abcdefghij'" :key="letter" class="field-cell">{{ letter }}</div>
            </div>
        </div>

        <div class="board">
            <div class="battlefield" @click="onBoardClicked">
            <div v-for="cell in getBoardCells(boardData)" :key="cell.index" :class="cell.cssClasses" :data-row="cell.dataRow" :data-column="cell.dataColumn"></div>
            </div>
        </div>

        <div class="numbers">
            <div class="numbers-container">
            <div v-for="n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]" :key="n" class="field-cell">{{ n }}</div>
            </div>
        </div>

        <div class="empty_space"></div>
    </div>
</template>

<style lang="scss" scoped>
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
    background-color: #2c3e50;
    border: 1px solid #ff6b6b;
  }

  .field-cell.fire {
    background-color: yellow;
    border: 1px solid yellow;
  }

  .field-cell.miss {
    background-color: wheat;
    border: 1px solid black;
  }

</style>