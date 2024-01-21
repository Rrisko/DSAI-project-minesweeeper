# DSAI-project-minesweeeper

Minesweeper project uses Answer set programming and Python selenium module to solve minesweeper game

**Scripts in the repo:**
- ```minesweeperModule.py``` with all functions and classes defintions
- ```minesweeper.lp``` used for writing constraints and facts about the game
- ```callMinesweeper``` which plays the game and references the first two files

## How does it work?

### Answer set programming

The game is defined by following rules:

- cells have X,Y coordinates
- each cell has a value (0-8) or a bomb
- based on X,Y coordinates, cell can have up to 8 neighbours
- if cell has a value, the value must correspond to number of bombs in the neighbourhood

Or in clingo:

```
% Cell has X,Y coordinates
% In begginer's game, grid is 9x9

cell(X, Y) :- 0 <= X <= 8 , 0 <= Y <= 8.

% Cell either has a value (0-8) or a bomb
1 = {value(X, Y, V) : 0 <= V <= 8 ; bomb(X, Y)} :- cell(X, Y).

% Neighbour cells definition
neighbour(X1,Y1,X2,Y2) :- cell(X1,Y1), cell(X2,Y2), Y1 = Y2, |X1 - X2| = 1.
neighbour(X1,Y1,X2,Y2) :- cell(X1,Y1), cell(X2,Y2), X1 = X2, |Y1 - Y2| = 1.
neighbour(X1,Y1,X2,Y2) :- cell(X1,Y1), cell(X2,Y2), |X1 - X2| = 1, |Y1 - Y2| = 1.

% Constraints - cell's value equals number of bombs in the neighbourhood

V = {bomb(X2, Y2) : neighbour(X2, Y2, X, Y)} :- value(X, Y, V).
```

### Web game interaction

https://minesweeper.online/ has a simple page structure, allowing us to refer to the cells in the grid by their **id**, which is in format *cell_x_y* . From the **class** of the cell the status of the cell can be extracted (covered/uncovered and the cell's value).

### Interaction with clingo

The program runs in loops, each loop extracts the available information from the web game, formats it as facts for clingo and writes it in the ```minesweeeper.lp``` file. Next, clingo solver is called, and it outputs facts about all cells. This output is filtered only for the cells neighbouring the uncovered region. A cell, which is deemed as safe, is clicked on, starting a new iteration of the loop.

Looping terminates with game's end: either by uncovering all safe cells or hitting a mine.

### Limitations

Clingo outputs possible solution for given configuation, but not necessary the correct one. This leads to hitting bombs in cells, clingo finds safe.
Bomb can be also hit by chance, as the first step in the game is always a guess.

### Recordings

In folder ```recordings```, you can find recordings of runs of the game. Some of them are unsuccessful, due to one of the limitations.

### What modules do you need?

The scripts in this repo use ```numPy```, ```selenium```, ```clingo```

### Sources

- https://github.com/potassco/guide/releases/tag/v2.2.0
- notebook unit5_03_logic_programming_part_2_answer_set_programming.ipynb from Unit 5 of DS&AI 1 course by Axel Polleres
- https://blog.dodgyfysix.com/
- https://minesweeper.online/
- https://selenium-python.readthedocs.io/





