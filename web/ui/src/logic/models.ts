export enum CellState {
    Empty = 0,
    Ship = 1,
    Hit = 2,
    Miss = 3
}

export interface IBoardCell {
  index: number
  cssClasses: string[],
  dataRow: number, 
  dataColumn: number
}

export interface IPoint {
    row: number
    column: number
}