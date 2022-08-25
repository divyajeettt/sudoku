import pygame
import random
import time
from itertools import product
import generator
import screens
import solver


"""
CONTROLS:

Left-click (on a box): Select the cell to select a cell
Arrow Keys: Change the selected cell
Backspace/Delete: Empty out the selected cell
Numbers (1-9): Enter the number in the selected cell*
Numbers (1-9) on numeric-keypad: Enter upto 4 guesses in the cell*

*enter the same number twice to remove it from the selected cell

NOTE: Please do not close the application while the algorithm is solving the
Sudoku as ongoing system processes may cause the app to crash

To visualize the backtracking, the solving algo has been slowed down.
To change the speed of the algorithm:
    • increase the speed by decreasing the value of SOLVING_DELAY
    • decrease the speed by increasing the value of SOLVING_DELAY
variable SOLVING_DELAY defined on LINE: 78
"""


pygame.font.init()
screens.main()


SIDE: float = 625.0        # side of the main window
BOX: float = SIDE / 9      # side of each cell

WINDOW = pygame.display.set_mode((SIDE+200, SIDE+5))
FPS: int = 60

LEVEL: int = screens.level
HINTS = {1: 35, 2: random.randint(25, 30), 3: random.randint(20, 22)}[LEVEL]
EMPTY = 81 - HINTS

# colors
Color = tuple[int, int, int]

BLACK: Color = (0, 0, 0)
WHITE: Color = (255, 255, 255)
GRAY: Color = (190, 190, 190)
GREEN: Color = (0, 150, 0)
ORANGE: Color = (255, 165, 0)
YELLOW: Color = (255, 215, 0)
RED: Color = (255, 0, 0)
BLUE: Color = (0, 0, 255)

FONT0 = pygame.font.SysFont("consolas", 20)
FONT1 = pygame.font.SysFont("consolas", 30)
FONT2 = pygame.font.SysFont("consolas", 35)

GRID: list[list[int]] = generator.grid()

HINT_INDICES: list[tuple[int, int]] = []
GUESSES: list[list[list[int]]] = [[[] for _ in range(9)] for _ in range(9)]

LINES: list[list[list[pygame.Rect]]] = [
    [
        [pygame.Rect(BOX*i-1, 0, (3 if i % 3 else 6), SIDE), BLACK]
        for i in range(10)
    ],
    [
        [pygame.Rect(0, BOX*i-1, SIDE+5, (3 if i % 3 else 6)), BLACK]
        for i in range(10)
    ],
]

SOLVING_DELAY: int = 50

pygame.display.set_caption(f"Sudoku (LEVEL: {LEVEL})")


def empty_grid():
    count = 0
    while count != EMPTY:
        i, j = random.randrange(9), random.randrange(9)
        while GRID[i][j] is None:
            i, j = random.randrange(9), random.randrange(9)
        GRID[i][j] = None
        count += 1

    for i, j in product(range(9), range(9)):
        if GRID[i][j] is not None:
            HINT_INDICES.append((i, j))


def draw_boxes(indices):
    counter, value = 0, (625 / 3)
    for i, j in product(range(3), range(3)):
        color = GRAY if counter % 2 else WHITE
        pygame.draw.rect(WINDOW, color, (value*i, value*j, value, value))
        counter += 1

    if indices is not None:
        x, y = indices
        pygame.draw.rect(WINDOW, YELLOW, (BOX*y, 0, BOX, SIDE))
        pygame.draw.rect(WINDOW, YELLOW, (0, BOX*x, SIDE, BOX))
        pygame.draw.rect(WINDOW, ORANGE, (BOX*y, BOX*x, BOX, BOX))


def draw_lines():
    for i, j in product(range(2), range(10)):
        line, color = LINES[i][j]
        pygame.draw.rect(WINDOW, color, line)


def draw_numbers():
    for i, j in product(range(9), range(9)):
        if (text := GRID[i][j]) is not None:
            color = BLACK if (i, j) in HINT_INDICES else BLUE
            WINDOW.blit(FONT2.render(str(text), 1, color), (BOX*j+25, BOX*i+22))


def draw_guesses():
    for i, j in product(range(9), range(9)):
        if (guess := GUESSES[i][j]):
            for k, num in enumerate(guess):
                X, Y = BOX*j+10*k+7, BOX*i+7
                WINDOW.blit(FONT0.render(str(num), 1, RED), (X, Y))


def select_cell(x=None, y=None):
    for i, j in product(range(2), range(10)):
        LINES[i][j][1] = BLACK

    if (x, y) in HINT_INDICES or (x is None and y is None):
        draw_boxes(None)
        return None

    LINES[1][x][1] = LINES[1][x+1][1] = GREEN
    LINES[0][y][1] = LINES[0][y+1][1] = GREEN

    return True


def change_selection(key, indices):
    x, y = indices

    dx = -1 if key == pygame.K_UP else +1 if key == pygame.K_DOWN else 0
    dy = -1 if key == pygame.K_LEFT else +1 if key == pygame.K_RIGHT else 0

    x = 9 if (x == 0 and dx == -1) else -1 if (x == 8 and dx == +1) else x
    y = 9 if (y == 0 and dy == -1) else -1 if (y == 8 and dy == +1) else y

    while (selection := select_cell(x+dx, y+dy)) is None:
        x, y = x+dx, y+dy
        x = 9 if (x == 0 and dx == -1) else -1 if (x == 8 and dx == +1) else x
        y = 9 if (y == 0 and dy == -1) else -1 if (y == 8 and dy == +1) else y

    return x+dx, y+dy


def enter_number(number, indices):
    x, y = indices
    GRID[x][y] = number if GRID[x][y] != number else None

    GUESSES[x][y] = []

    if GRID[x][y] is not None:
        WINDOW.blit(FONT2.render(str(number), 1, BLUE), (BOX*x+25, BOX*y+22))


def enter_guess(number, indices):
    x, y = indices
    GRID[x][y] = None

    if number in GUESSES[x][y]:
        GUESSES[x][y].remove(number)
    else:
        GUESSES[x][y].append(number)

    if len(GUESSES[x][y]) > 4:
        GUESSES[x][y].pop(0)

    for i, num in enumerate(GUESSES[x][y]):
        WINDOW.blit(FONT0.render(str(num), 1, RED), (BOX*x+10*i+7, BOX*y+7))


def draw_timer(seconds):
    hours = str(int(seconds / 3600)).zfill(2)
    minutes = str(int(seconds / 60)).zfill(2)
    seconds = str(seconds % 60).zfill(2)

    text = f"{hours}:{minutes}:{seconds}"

    pygame.draw.rect(WINDOW, BLACK, (640, 590, 200, 100))
    WINDOW.blit(FONT1.render(text, 1, WHITE), (660, 593))

    return hours, minutes, seconds


def reset():
    for i, j in product(range(9), range(9)):
        if (i, j) not in HINT_INDICES:
            GRID[i][j] = None
            GUESSES[i][j] = []


def restart():
    for i, j in product(range(2), range(10)):
        LINES[i][j][1] = BLACK

    pygame.draw.rect(WINDOW, BLACK, (640, 590, 200, 100))

    GRID = generator.grid()
    HINT_INDICES = []
    GUESSES = [[[] for _ in range(9)] for _ in range(9)]

    globals().update(locals())

    empty_grid()
    draw_boxes(None)


def main():
    INDICES = None
    SOLVED_BY_COMP = False
    arrow_keys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    clock = pygame.time.Clock()

    pygame.draw.rect(WINDOW, BLACK, (630, 0, 200, 200))
    pygame.draw.rect(WINDOW, WHITE, (630, 0, 3, SIDE+5))
    pygame.draw.rect(WINDOW, WHITE, (630, 580, 200, 3))

    WINDOW.blit(FONT1.render("00:00:00", 1, WHITE), (660, 593))

    texts = ("RESET", "RESTART", "SOLVE")
    for i, text in enumerate(texts):
        WINDOW.blit(FONT1.render(text.center(8), 1, WHITE), (665, 52*i+11))
        pygame.draw.rect(WINDOW, WHITE, (625, 50*(i+1), 200, 3))

    empty_grid()
    draw_boxes(None)

    start_time = time.time()
    timer = 0

    RUN = True
    while RUN:
        clock.tick(FPS)

        if ((curr_time := time.time()) - start_time) >= 1:
            start_time = curr_time
            draw_timer(timer := timer+1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    continue
                else:
                    x, y = event.pos

                if x <= 625:
                    selection = select_cell(int(y // BOX), int(x // BOX))
                    if selection is not None:
                        INDICES = (int(y // BOX), int(x // BOX))
                    else:
                        INDICES = None

                elif y < 51:
                    INDICES = None
                    select_cell()
                    reset()

                elif 51 < y < 101:
                    select_cell()
                    restart()
                    timer, INDICES, SOLVED_BY_COMP = 0, None, False
                    WINDOW.blit(FONT1.render("00:00:00", 1, WHITE), (660, 593))

                elif 101 < y < 151:
                    INDICES, SOLVED_BY_COMP = None, True
                    select_cell()
                    reset()
                    pygame.draw.rect(WINDOW, BLACK, (640, 590, 200, 100))
                    solver.solve(
                        GRID,
                        draw_numbers, draw_lines,
                        (lambda: pygame.time.delay(SOLVING_DELAY)),
                        pygame.display.update,
                        draw_boxes, select_cell
                    )
                    select_cell()

                else:
                    INDICES = None
                    for i, j in product(range(2), range(10)):
                        LINES[i][j][1] = BLACK

            if INDICES is not None:
                if event.type != pygame.KEYDOWN:
                    continue

                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    x, y = INDICES
                    enter_number(GRID[x][y], INDICES)

                for num in range(1, 10):
                    if event.key == getattr(pygame, f"K_{num}"):
                        enter_number(num, INDICES)
                    elif event.key == getattr(pygame, f"K_KP{num}"):
                        enter_guess(num, INDICES)

                if event.key in arrow_keys:
                    INDICES = change_selection(event.key, INDICES)

        draw_boxes(INDICES)
        draw_numbers()
        draw_lines()
        draw_guesses()

        pygame.display.update()

        if generator.valid(GRID):
            # Sudoku Solved
            if SOLVED_BY_COMP:
                text = "Sudoku Solved Successfully!"
            else:
                hours, minutes, seconds = draw_timer(timer)
                total = f"{seconds.lstrip('0')} Second(s)"

                if minutes != "00":
                    total = f"{minutes.lstrip('0')} Minute(s) and {total}"
                if hours != "00":
                    total = f"{hours.lstrip('0')} Hour(s) and {total}"

                text = f"CONGRATS! You solved the Sudoku in {total}!"

            if screens.ending(text):
                select_cell()
                restart()
                timer, INDICES, SOLVED_BY_COMP = 0, None, False
                WINDOW.blit(FONT1.render("00:00:00", 1, WHITE), (660, 593))
            else:
                RUN = False

    pygame.quit()


if __name__ == "__main__":
    main()
