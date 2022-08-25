# sudoku

## About sudoku

sudoku is a simple playable [Sudoku Game](https://en.wikipedia.org/wiki/Sudoku) which is built using [`pygame`](https://www.pygame.org/docs/) in Python. It is a graphical-user interface based project. \
*Date of creation:* `27 June, 2021`

This project is a single-player. After choosing a difficulty level, the player can start solving the puzzle on the 9×9 Grid.

## Features

The following features are provided in the game:
- Three difficulty levels, i.e., easy, medium, and hard
- A sudoku-generator that generates random sudoku-grids
- A sudoku-solver that solves a sudoku-grid using backtracking
- Visualization of working of the solving algorithm, with a variable speed

## Controls

- Left-click (on a box): Select the cell to select a cell
- Arrow Keys: Change the selected cell
- Backspace/Delete: Empty out the selected cell
- Numbers (1-9): Enter the number in the selected cell
- Numbers (1-9) on numeric-keypad: Enter upto 4 guesses in the cell

*Note: Enter an already entered number in the selected cell to remove it. Guesses are inserted in a [FIFO]([https://en.wikipedia.org/wiki/FIFO](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics))) manner.*

## Change the Speed of the visualization of solver

The solver-algorithm has been slowed down to visualize the backtracking has been slowed down. To change the speed of the algorithm, go to [Line 77]() in `main.py` and change the value of the variable `SOLVING_DELAY`:
- <b>Increase the speed</b> by decreasing `SOLVING_DELAY`
- <b>Decrease the speed</b> by increasing `SOLVING_DELAY`

Time complexity of Solver: `O(9ᴹ)`, where `M` is the number of unfilled cells (Attributing to the fact that there are 9 possibilities for each empty cell).

## Footnotes

- Difficulty level corresponds to the number of cells of the grid whose values are known. The harder the level, the fewer initial values are given in the grid.
- The number of cells initially given are chosen randomly according to the selected level.
- Some sudoku-grids have [multiple solutions](https://masteringsudoku.com/can-sudoku-have-multiple-solutions/).
- <b>Do not</b> close the application while the algorithm is solving the Sudoku as ongoing system processes may cause the app to crash.

## Run

To play, clone the repository on your device, navigate to the folder, and execute:

```
python3 main.py
```

## References

- [Sudoku-Solver Tutorial with Backtracking Pt. 1 (YouTube)](https://www.youtube.com/watch?v=eqUwSA0xI-s)
- [Sudoku-Solver Tutorial with Backtracking Pt. 2 (YouTube)](https://www.youtube.com/watch?v=lK4N8E6uNr4)
- [Sudoku-Grid Generator (YouTube)](https://www.youtube.com/watch?v=LHCHH5siBCg)
- [SudokuGridGenerator (GitHub)](https://github.com/mfgravesjr/finished-projects/tree/master/SudokuGridGenerator)
