# sudoku

## About sudoku

sudoku is a simple playable [Sudoku Game](https://en.wikipedia.org/wiki/Sudoku) which is built using [`pygame`](https://www.pygame.org/docs/) in Python. It is a graphical-user interface based project.

*Date of creation:* `27 June, 2021`

This project is a single-player. After choosing a difficulty level, the player can start solving the puzzle on the 9×9 Grid.

## Features

The following features are provided in the game:
- Three difficulty levels, i.e., easy, medium, and hard
- A sudoku-generator that generates random sudoku-grids
- A sudoku-solver that solves a sudoku-grid using backtracking
- Visualization of working of the solving-algorithm, with variable speed

## Controls

- Left-click (on a box/cell): Select the cell
- Arrow Keys: Change the selected cell
- Backspace/Delete: Empty out the selected cell
- Numbers (1-9): Enter the number in the selected cell
- Numbers (1-9) on numeric-keypad: Enter upto 4 guesses in the cell

*Note: Enter an already entered number in the selected cell to remove it. Guesses are inserted in a [FIFO]([https://en.wikipedia.org/wiki/FIFO](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics))) manner.*

## Change the speed of visualization of the solver

The solving-algorithm has been slowed down to visualize the backtracking. To change its speed, go to [Line 78](https://github.com/divyajeettt/sudoku/blob/5de7e4737595f8eb88356cb185de44a3f9a0b2d2/main.py#L78) in `main.py` and change the value of the variable `SOLVING_DELAY`:
- **Increase the speed** by decreasing the DELAY
- **Decrease the speed** by increasing the DELAY

For reference, Line 78 is the following variable definition:

```python
SOLVING_DELAY: int = 50
```

Time complexity of Solver: `O(9ᴹ)`, where `M` is the number of unfilled cells (Attributing to the fact that there are 9 possibilities for each empty cell).

## Footnotes

- Difficulty level corresponds to the number of initially filled cells in the grid. The harder the level, the fewer initial values are given in the grid.
- The number of cells initially given are chosen randomly according to the selected level.
- Some sudoku-grids have [multiple solutions](https://masteringsudoku.com/can-sudoku-have-multiple-solutions/).
- **Do not close** the application while the algorithm is solving the Sudoku as ongoing system processes may cause the app to crash.

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
