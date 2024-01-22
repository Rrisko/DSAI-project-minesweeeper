from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import clingo
import numpy as np


def click_id(driver, cid):
    stock_code = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, cid))
    )
    stock_code.click()


def knowledge_matrix_conversion(matrix, dim=9):
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


def get_clingo_input(driver, dim=9):
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


def return_matching_strings(matrix):
    output_list = []
    indices = np.where(matrix == 2)

    for i, j in zip(indices[0], indices[1]):
        output_list.append(f"value({i},{j}")
        output_list.append(f"bomb({i},{j})")
    return output_list


def filter_clingo_output(matches, output):
    return [
        string for string in output if any(substring in string for substring in matches)
    ]


def write_clingo_file(file_path, clingo_input):
    with open(file_path, "w") as file:
        # Add a new line
        file.write(
            """

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
               
                   """
        )

        file.write("\n")
        # Add input
        file.write(clingo_input)
        file.write("\n")
        file.write("#show bomb/2.")
        file.write("\n")
        file.write("#show value/3.")


def clingo_solve(file_path):
    ctl = clingo.Control()

    ctl.load(file_path)
    ctl.ground([("base", [])])

    models = []

    with ctl.solve(yield_=True) as handle:
        for model in handle:
            models.append(format(model))

    return models[0].split()


def filter_clingo_solve(file_path, matrix):
    solved_list = clingo_solve(file_path)
    matches = return_matching_strings(matrix)
    filtered_solved_list = filter_clingo_output(matches, solved_list)
    left_clicks = [
        "cell_{}_{}".format(s[6:7], s[8:9])
        for s in filtered_solved_list
        if s.startswith("value")
    ]

    return left_clicks


###################################
###################################
###################################

lp_path = "minesweeper.lp"
url = "https://minesweeper.online/new-game"
driver = webdriver.Chrome()
driver.get(url)

time.sleep(2)

click_id(driver, "cell_4_4")

clingo_input, mx = get_clingo_input(driver, 9)

write_clingo_file(lp_path, clingo_input)

left_clicks = filter_clingo_solve(lp_path, mx)

solved = False


while not solved:
    face_class = driver.find_element(By.ID, "top_area_face").get_attribute("class")
    if face_class == "top-area-face zoomable hd_top-area-face-unpressed":
        solved = False
    else:
        solved = True

    click_id(driver, left_clicks[0])

    clingo_input, mx = get_clingo_input(driver, 9)

    write_clingo_file(lp_path, clingo_input)

    left_clicks = filter_clingo_solve(lp_path, mx)

time.sleep(30)
