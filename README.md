# sudoku

## About sudoku

sudoku is a simple playable [Sudoku Game](https://en.wikipedia.org/wiki/Sudoku) which is built using [`pygame`](https://www.pygame.org/docs/) in Python. It is a graphical-user interface based project. \
*Date of creation:* `27 June, 2021`

This project is a single-player. After choosing a difficulty level, the player can start solving the puzzle on the 9×9 Grid.

## Features

The following features are provided in the game:
- Three difficulty levels, i.e., easy, medium, and hard.
- A sudoku-generator that generates random sudoku-grids.
- A sudoku-solver that solves a sudoku-grid using backtracking.

## Footnotes

- Difficulty level corresponds to the number of cells of the grid whose values are known. The harder the level, the fewer initial values are given.
- The number of cells initially given are chosen randomly according to the selected level.
- Some sudoku-grids have [multiple solutions](https://masteringsudoku.com/can-sudoku-have-multiple-solutions/).

## Run

To play, clone the repository on your device, navigate to the folder, and execute:

```
python3 main.py
```

## References

- [Sudoku-Solver Tutorial with Backtracking Pt. 1 (YouTube)](https://www.youtube.com/watch?v=eqUwSA0xI-s)
- [Sudoku-Solver Tutorial with Backtracking Pt. 2 (YouTube)](https://www.youtube.com/watch?v=lK4N8E6uNr4)
- [Sudoku-Grid Generator (YouTube)](https://www.youtube.com/watch?v=LHCHH5siBCg)
