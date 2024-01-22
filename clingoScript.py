import clingo
import numpy as np

ctl = clingo.Control()

from pathlib import Path

ctl.load("c:/Users/errik/Desktop/WU/DE/Third Semester/DSAI/project_Axel/sudoku.lp")
ctl.ground([("base", [])])
# ctl.solve(on_model=on_model)
models = []

# call the solver and store all formatted models
# as output by clingo in the list models:
with ctl.solve(yield_=True) as handle:
    for model in handle:
        models.append(format(model))

print(models, "\n\n")

# convert model[0] into a more readable matrix:
matrix = np.empty((9, 9))

m = models[0].replace("tab(", "").replace(")", "").split(" ")
for i in m:
    tab = i.split(",")
    matrix[int(tab[0]), int(tab[1])] = int(tab[2])
print(matrix)
