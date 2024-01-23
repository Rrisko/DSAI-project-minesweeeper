from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import clingo
import numpy as np


def click_id(driver: webdriver, cid: str):
    """Clicks element on the webpage by id (input cid)"""

    stock_code = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, cid))
    )
    stock_code.click()


def knowledge_matrix_conversion(matrix, dim: int = 9) -> np.array:
    """
    Outputs a matrix of the game grid.
    Value 1 means complete information,
    0 means no information,
    2 means the cell borders a cell with complete information
    """

    output_matrix = matrix.copy()
    for i in range(dim):
        for j in range(dim):
            if matrix[i][j] != 0:
                next
            l = max(0, j - 1)
            r = min(dim - 1, j + 1) + 1
            u = max(0, i - 1)
            d = min(dim - 1, i + 1) + 1
            if np.sum(matrix[u:d, l:r]) > 0:
                output_matrix[i][j] = 2
            if matrix[i][j] == 1:
                output_matrix[i][j] = 1
    return output_matrix


def get_clingo_input(driver: webdriver, dim: int = 9) -> tuple[str, np.array]:
    """
    Gets information from web in clingo format: value(X,Y,Value).
    Also outputs knowledge matrix (see knowledge_matrix conversion).
    """

    cell_list = []
    knowledge_matrix = np.zeros((dim, dim), dtype=int)

    for row in range(dim):
        for col in range(dim):
            cell_id = "cell_{}_{}".format(row, col)
            cell_value = driver.find_element(By.ID, cell_id).get_attribute("class")
            cell_value = cell_value[-1]
            try:
                cell_value = int(cell_value)
                cell_encoding = "value({},{},{})".format(row, col, cell_value)
                cell_list.append(cell_encoding)
                knowledge_matrix[row][col] = 1
            except:
                next

    clingo_input = ". ".join(cell_list) + "."

    return clingo_input, knowledge_matrix_conversion(knowledge_matrix, dim)


def return_matching_strings(matrix: np.array) -> list:
    """Returns matches knowledge matrix cells with value 2 in clingo format: value(X,Y or bomb(X,Y)"""

    output_list = []
    indices = np.where(matrix == 2)

    for i, j in zip(indices[0], indices[1]):
        output_list.append(f"value({i},{j}")
        output_list.append(f"bomb({i},{j})")
    return output_list


def filter_clingo_output(matches, output) -> list:
    """Filters output of clingo - only solutions that overlap with matches are returned"""

    return [
        string for string in output if any(substring in string for substring in matches)
    ]


def write_clingo_file(file_path: str, clingo_input: str, dim: int = 9):
    """Writes constraints and facts to clingo file."""

    with open(file_path, "w") as file:
        file.write(
            f"""

% Cell has X,Y coordinates
% In begginer's game, grid is 9x9

cell(X, Y) :- 0 <= X <= {dim-1} , 0 <= Y <= {dim-1}.
"""
            + """

% Cell either has a value (0-8) or a bomb
1 = {value(X, Y, V) : 0 <= V <= 8 ; bomb(X, Y)} :- cell(X, Y).

% Neighbour cells definition
neighbour(X1,Y1,X2,Y2) :- cell(X1,Y1), cell(X2,Y2), Y1 = Y2, |X1 - X2| = 1.
neighbour(X1,Y1,X2,Y2) :- cell(X1,Y1), cell(X2,Y2), X1 = X2, |Y1 - Y2| = 1.
neighbour(X1,Y1,X2,Y2) :- cell(X1,Y1), cell(X2,Y2), |X1 - X2| = 1, |Y1 - Y2| = 1.

% Constraints - cell's value equals number of bombs in the neighbourhood

V = {bomb(X2, Y2) : neighbour(X2, Y2, X, Y)} :- value(X, Y, V).
               
                   """
        )

        file.write("\n")
        # Add input
        file.write(clingo_input)
        file.write("\n")
        file.write("#show value/3.")


def clingo_solve(file_path, clingo_input, model_count, dim: int = 9) -> list:
    """Gets solution from .lp file using clingo"""

    write_clingo_file(file_path, clingo_input, dim)

    ctl = clingo.Control("9")

    ctl.load(file_path)
    ctl.ground([("base", [])])

    models = []

    with ctl.solve(yield_=True) as handle:
        for model in handle:
            models.append(format(model))

    try:
        models = [m.split() for m in models]
        models_set = set(models[0]).intersection(*models[1:])
        models_list = list(models_set)

        if model_count > 1:
            return models_list

        return models[0]

    except:
        return models[0]


def filter_clingo_solve(file_path: str, clingo_input, matrix: np.array) -> list:
    """Filters clingo output for matches (knowledge matrix field = 2)"""

    solved_list = clingo_solve(file_path, clingo_input, 9)
    matches = return_matching_strings(matrix)

    filtered_solved_list = filter_clingo_output(matches, solved_list)
    left_clicks = [
        "cell_{}_{}".format(s[6:7], s[8:9])
        for s in filtered_solved_list
        if s.startswith("value")
    ]

    if len(left_clicks) < 1:
        solved_list = clingo_solve(file_path, clingo_input, 1)
        filtered_solved_list = filter_clingo_output(matches, solved_list)
        left_clicks = [
            "cell_{}_{}".format(s[6:7], s[8:9])
            for s in filtered_solved_list
            if s.startswith("value")
        ]

    return left_clicks
