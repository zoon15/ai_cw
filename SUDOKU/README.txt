Part 1b - Sudoku solver 
- tested with python 3.12

Files 
- sudoku_solver.py : the solver gives a terminal output and GUI window 
- puzzles : has sudoku files of different difficulties including a file that doest have a solution 

How to run 
- in terminal run python3 sudoku_solver.py 
- choose your difficulty level
- unsolved puzzle is printed in terminal andd GUI window open 
- click "Solve" on the window and solution appears with number of steps, backtracks and time taken 
- "Reset" shows unsolved puzzle again 
- "Another puzzle" loads a different puzzle of same difficulty 

To test no solution puzzle 
- in terminal run python3 sudoku_solver.py puzzles/unsolvable_puzzles.txt