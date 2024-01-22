from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import clingo
import numpy as np

url = "https://minesweeper.online/new-game"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

stock_code = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.ID, "cell_0_0"))
)
stock_code.click()

cell_list = []

knowledge_matrix = np.zeros((9, 9), dtype=int)


def knowledge_matrix_conversion(matrix=knowledge_matrix, dim=9):
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


time.sleep(1)

for row in range(9):
    for col in range(9):
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
print(clingo_input)
converted_matrix = knowledge_matrix_conversion()
matches = return_matching_strings(converted_matrix)

print(converted_matrix)
print(matches)


with open(
    "c:/Users/errik/Desktop/WU/DE/Third Semester/DSAI/project_Axel/minesweeper.lp", "w"
) as file:
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

ctl = clingo.Control()


ctl.load("c:/Users/errik/Desktop/WU/DE/Third Semester/DSAI/project_Axel/minesweeper.lp")
ctl.ground([("base", [])])
# ctl.solve(on_model=on_model)
models = []

# call the solver and store all formatted models
# as output by clingo in the list models:
with ctl.solve(yield_=True) as handle:
    for model in handle:
        models.append(format(model))

preds = filter_clingo_output(matches, models[0].split())
print(preds)

print("###")

left_clicks = [
    "cell_{}_{}".format(s[6:7], s[8:9]) for s in preds if s.startswith("value")
]
right_clicks = [
    "cell_{}_{}".format(s[5:6], s[7:8]) for s in preds if s.startswith("bomb")
]

print(left_clicks)
print(right_clicks)

for cid in left_clicks:
    stock_code = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, cid))
    )
    stock_code.click()

time.sleep(30)
