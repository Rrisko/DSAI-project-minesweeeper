

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
               
                   
value(0,0,0). value(0,1,0). value(0,2,0). value(0,3,0). value(0,4,1). value(0,6,2). value(0,8,1). value(1,0,1). value(1,1,1). value(1,2,2). value(1,3,1). value(1,4,2). value(1,5,1). value(1,6,2). value(1,7,2). value(1,8,2). value(2,0,1). value(2,2,2). value(2,4,1). value(2,5,0). value(2,6,0). value(2,7,1). value(3,0,1). value(3,1,1). value(3,2,2). value(3,3,1). value(3,4,1). value(3,5,0). value(3,6,0). value(3,7,1). value(3,8,1). value(4,0,0). value(4,1,0). value(4,2,0). value(4,3,0). value(4,4,1). value(4,5,1). value(4,6,1). value(4,7,0). value(4,8,0). value(5,0,0). value(5,1,0). value(5,2,1). value(5,3,1). value(5,4,2). value(5,6,2). value(5,7,1). value(5,8,0). value(6,0,1). value(6,1,1). value(6,2,2). value(6,4,2). value(6,5,2). value(6,7,1). value(6,8,0). value(7,0,2). value(7,2,3). value(7,3,1). value(7,4,1). value(7,5,1). value(7,6,1). value(7,7,1). value(7,8,0). value(8,0,2). value(8,2,2). value(8,3,0). value(8,4,0). value(8,5,0). value(8,6,0). value(8,7,0). value(8,8,0).
#show bomb/2.
#show value/3.