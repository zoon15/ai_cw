# Part 1b: Sudoku Solver
# Approach: Backtracking with forward checking and MRV
import os
import random
import sys
import time

try:
    import tkinter as tk  # python library for GUI
    HAVE_TK = True
except ImportError:  
    HAVE_TK = False

# stores the number of steps taken to solve a puzzle and the number of backtracks
counter = {"steps": 0, "backtracks": 0}

# PART 1 : SOLVER 
#stores the folder with the puzzle files 
PUZZLE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puzzles")

# its a function that works out for each cell which other cells it shouldn't share a digit with
def peers_build():
    peers = {}
    # the two loops below iterate through each cell of the sudoku grid
    for rows in range(9):
        for columns in range(9):
            p = set()  # empty set to store the peers of the current cell
            for i in range(9):
                p.add((rows, i))  # adds every cell in the row
                p.add((i, columns))  # adds every cell in the column
            top, left = 3 * (rows // 3), 3 * (columns // 3)  # finds the top left corner of the cell's 3*3 block
            # the loops below iterate through the block and all the cells in it
            for x in range(top, top + 3):
                for y in range(left, left + 3):
                    p.add((x, y))
            p.remove((rows, columns))  # removes the cell as it isnt a peer of itself
            peers[(rows, columns)] = p  # stores the set
    return peers


PEERS = peers_build()  # runs the function once and stores the result


# its a function that checks if the numbers that are initially placed in the grid are valid or not
def valid_clue(grid):
    # goes through each key and value pair in PEERS, the key goes to (rows, columns) and the value goes to peers
    for (rows, columns), peers in PEERS.items():
        digit = grid[rows][columns]  # stores the digit in the current cell
        # only looks at the filled cells and checks if at least one peer holds the same number
        if digit != 0 and any(grid[peer_row][peer_column] == digit for (peer_row, peer_column) in peers):
            return False
    return True


# its a function that checks if a finished grid is valid
def valid_solution(grid):
    digits = set(range(1, 10))  # stores the digits from 1 to 9
    # checks if all the digits are there in each row
    rows_ok = all(set(row) == digits for row in grid)
    # checks if all the digits are there in each column
    columns_ok = all({grid[rows][columns] for rows in range(9)} == digits for columns in range(9))
    # checks if all the digits are there in each 3x3 block (top and left are the corner of each block)
    blocks_ok = all(
        {grid[top + i][left + j] for i in range(3) for j in range(3)} == digits
        for top in (0, 3, 6) for left in (0, 3, 6)
    )
    return rows_ok and columns_ok and blocks_ok  # its valid only if all the three conditions are true


# its a function that works out for each empty cell which numbers could still be placed in it
def initial_options(grid):
    options = {}  
    # the two loop iterate through each cell and keep only the ones that are empty 
    for rows in range(9):
        for columns in range(9):
            if grid[rows][columns] == 0:
                used = {grid[peer_row][peer_column] for (peer_row, peer_column) in PEERS[(rows, columns)]} # stores the digits that its peers have used 
                options[(rows, columns)] = set(range(1, 10)) - used  # stores the digits that are still possible for the cell to use 
    return options


# its a function that picks which empty cell to fill next using the MRV rule 
def pick_cell(options):
    def key(cell):
        empty_peers = sum(1 for p in PEERS[cell] if p in options) # stores the current cell's empty peers 
        return (len(options[cell]), -empty_peers, cell) #return a tuple with fewest options left, most empty peers and the cell coordinates 
    return min(options, key=key) # returns the tuple with the smallest values 


# its a recursive function that uses backtracking to fill the empty cells one at a time and also uses forward checking to spot ends early
def search(grid, options):
    if not options:
        return True  # no empty cells are left 

    cell = pick_cell(options)  # calls the function pick_cell to see which empty cell to fill next 
    row, col = cell  # unpacks the cell coordinates

    for number in sorted(options[cell]):  # the loop iterates to find each possible digit for that cell in ascending order 
        grid[row][col] = number  # places the digit in the cell 
        counter["steps"] += 1 # increases counter for steps taken to solve the puzzle 
        saved = options.pop(cell)  # removes the cell from empty list but keeps its options in saved if we need to undo later  
        removed = []  # a list storing the peers we changed so that we can undo later 
        dead_end = False # no error found yet 

        # does forward checking, for each peer that is still empty and has the digits as an option, it removes the digit from its options 
        for peer in PEERS[cell]: 
            if peer in options and number in options[peer]:
                options[peer].discard(number)
                removed.append(peer)
                # the peer has no options left so the current choice lead to dead end 
                if not options[peer]:  
                    dead_end = True
                    break
        # continues solving rest of the puzzles 
        if not dead_end and search(grid, options):  
            return True
        # backtracks and undoes the changes made 
        for peer in removed:
            options[peer].add(number)  # undoes the forward checking changes 
        options[cell] = saved  # puts the cells orginal option back so the cell is empty again 
        grid[row][col] = 0 #clears the digit 
        counter["backtracks"] += 1 #increases counter for backtracks 

    return False  # every digit was tried and none worked 


# its a setup function that checks if the clues are valid and the calls the function search to solve the puzzle
def solve(grid):
    counter["steps"] = 0 #resets the counter for steps 
    counter["backtracks"] = 0 #rests the counter for backtracks
    if not valid_clue(grid): # checks if the clues given are valid or not 
        return False  # if they arent valid  no solution is possible
    options = initial_options(grid) # build the starting options list for each empty cell     
    if any(len(o) == 0 for o in options.values()): # checks if any empty cell has no options left
        return False  # if so then there isnt a valid solution for it 
    return search(grid, options) # calls the recursive search function to solve the puzzle and return True if solved or False if no solution is possible 

# PART 2: INPUT AND TERMINAL OUTPUT

# reads a .txt or .csv file and returns it as a puzzle of 9x9 list of lists
def load_puzzle(filename):
    grid = [] # list storing the rows 
    # opens the file and reads it one line at a time 
    with open(filename) as f:  
        for line in f:
            line = line.strip() #removes the leading and trailing spaces 
            if line:
                #replaces the commas with whitespaces then uses split to split the line into a list of strings and then int(v) converts that list of strings into intergers 
                grid.append([int(v) for v in line.replace(",", " ").split()])
    # validates if there are exactly 9 rows and each row has exactly 9 values 
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("puzzle must be 9 lines of 9 values")
    # validates if the values are between 0 to 9 
    if any(v < 0 or v > 9 for row in grid for v in row):
        raise ValueError("values must be 0-9 (0 = empty)")
    return grid #returns the finished grid 


# its a funtion prints the grid in the terminal 
def print_grid(grid):
    # it iterates through each row and prints the values with lines seperating the 3x3 blocks 
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("------+-------+------")
        line = ""
        # it iterates through each column and prints the values with lines seperating the 3x3 blocks
        for c in range(9):
            if c % 3 == 0 and c != 0:
                line += "| "
            line += (str(grid[r][c]) if grid[r][c] != 0 else ".") + " "
        print(line.rstrip()) # prints the row without trailing spaces 

# its a function that prints the unsolved puzzle in the terminal
def print_unsolved(title, grid):
    print(f"\n=== {title} (unsolved) ===")
    print_grid(grid)


# its a function that prints the solved puzzle in the terminal along with the number of steps, backtracks and time taken to solve it
def print_result(title, grid, solved, seconds):
    if solved:
        print(f"\n=== {title} (solution) ===")
        print_grid(grid)
    else:
        print(f"\n=== {title} ===")
        print("No solution")
    print(f"Steps:      {counter['steps']}")
    print(f"Backtracks: {counter['backtracks']}")
    print(f"Time taken: {seconds:.4f} s")


# its a function that calls the solve function and also measures the time taken to solve the puzzle
def solve_timed(grid):
    start = time.perf_counter()
    solved = solve(grid)
    return solved, time.perf_counter() - start

# its a lookup dictionary that maps what the user types to the title 
LEVELS = {  
    "easy": "Easy puzzle",
    "medium": "Medium puzzle",
    "hard": "Hard puzzle",
}


# its a function that asks the user to choose a difficulty level and returns it, it keeps asking until the user types a valid answer
def ask_level():
    while True:
        answer = input("Choose a mode : easy / medium / hard ").strip().lower()
        if answer in LEVELS:
            return answer
        print("Please type easy, medium or hard.")


# its a function that picks a random puzzle file of the given difficulty level and returns it as a grid, it also returns the filename so that the next puzzle can be different
def random_puzzle(level, previous=None):
    if not os.path.isdir(PUZZLE_FOLDER):
        raise FileNotFoundError(f"puzzle folder not found: {PUZZLE_FOLDER}")
    files = sorted(name for name in os.listdir(PUZZLE_FOLDER)
                   if name.lower().startswith(level) and name.lower().endswith((".txt", ".csv")))
    if not files:
        raise FileNotFoundError(f"no {level} puzzle files in {PUZZLE_FOLDER}")
    choices = [name for name in files if name != previous] or files  # avoids repeating if there are other files
    filename = random.choice(choices)
    return load_puzzle(os.path.join(PUZZLE_FOLDER, filename)), filename

# PART 3: THE GUI

GIVEN_COLOUR = "black"  # color for the "clues" that were already in the puzzle
SOLVED_COLOUR = "#1f5fbf"  # color for the digits found by the solver
BLOCK_COLOURS = ("#ffffff", "#e8eef7")  # colors to alternate shading for the 3x3 blocks

# its a class that creates the window and handles the events in it
class SudokuWindow:
    def __init__(self, root, puzzle, title, level, filename=None):
        self.root = root
        root.title("Sudoku Solver - F29AI CW1")
        root.resizable(False, False)

        self.puzzle = [row[:] for row in puzzle]  # stores a copy of the unsolve puzzle so that "Reset" can show it again 
        self.title = title
        self.level = level  # None if the puzzle came from a file given by the user
        self.last_file = filename  # which puzzle file is showing at the moment
        self.labels = [[None] * 9 for _ in range(9)]  # the 81 boxes on the screen
        # live text for the windows and updates the labels 
        self.message = tk.StringVar()
        self.steps = tk.StringVar()
        self.backtracks = tk.StringVar()
        self.seconds = tk.StringVar()

        self.build_board()
        self.build_controls()
        self.show_puzzle()

    # its a function that builds the 9x9 grid of boxes 
    def build_board(self):
        board = tk.Frame(self.root, padx=12, pady=12)
        board.grid(row=0, column=0)
        for r in range(9):
            for c in range(9):
                shade = BLOCK_COLOURS[((r // 3) + (c // 3)) % 2] 
                label = tk.Label(board, width=2, font=("Helvetica", 22, "bold"),
                                 bg=shade, relief="solid", bd=1)
                label.grid(row=r, column=c, ipady=6,
                           padx=(8 if c in (3, 6) else 1, 1),
                           pady=(8 if r in (3, 6) else 1, 1))
                self.labels[r][c] = label

    # its a function that builds the buttons and labels below the grid
    def build_controls(self):
        panel = tk.Frame(self.root, padx=12, pady=6)
        panel.grid(row=1, column=0, sticky="we")

        numbers = tk.Frame(panel)
        numbers.pack(anchor="w")
        for text, var in (("Steps:", self.steps), ("Backtracks:", self.backtracks),
                          ("Time taken:", self.seconds)):
            tk.Label(numbers, text=text, font=("Helvetica", 12, "bold")).pack(side="left")
            tk.Label(numbers, textvariable=var, width=9, anchor="w",
                     font=("Helvetica", 12)).pack(side="left")

        buttons = tk.Frame(panel, pady=8)
        buttons.pack(anchor="w")
        tk.Button(buttons, text="Solve", font=("Helvetica", 12, "bold"),
                  command=self.solve_clicked).pack(side="left", padx=3)
        tk.Button(buttons, text="Reset", command=self.show_puzzle).pack(side="left", padx=3)
        again = tk.Button(buttons, text="Another puzzle (same difficulty)",
                          command=self.another_puzzle)
        again.pack(side="left", padx=3)
        if self.level is None:
            again.config(state="disabled") 

        tk.Label(panel, textvariable=self.message, anchor="w", justify="left",
                 wraplength=470, font=("Helvetica", 12)).pack(anchor="w")

    # its a function that writes the digits on the screen 
    def draw(self, grid):
        for r in range(9):
            for c in range(9):
                digit = grid[r][c]
                is_given = self.puzzle[r][c] != 0
                self.labels[r][c].config(text=str(digit) if digit else "",
                                         fg=GIVEN_COLOUR if is_given else SOLVED_COLOUR)

    # its a function that clears the unsolved puzzle and shows how it was at the start and erases the time, the backtrack and the steps 
    def show_puzzle(self):
        self.draw(self.puzzle)
        for var in (self.steps, self.backtracks, self.seconds):
            var.set("-")
        clues = sum(1 for row in self.puzzle for v in row if v)
        self.message.set(f"{self.title} ({clues} clues). Press Solve.")

    # its a function that runs when the solve button is pressed 
    def solve_clicked(self):
        grid = [row[:] for row in self.puzzle] 
        self.message.set("Solving...")
        self.root.update_idletasks()

        solved, seconds = solve_timed(grid)

        self.steps.set(str(counter["steps"]))
        self.backtracks.set(str(counter["backtracks"]))
        self.seconds.set(f"{seconds:.4f} s")
        if solved:
            self.draw(grid)
            check = "verified valid" if valid_solution(grid) else "CHECK FAILED"
            self.message.set(f"{self.title} solved ({check}).")
        else:
            self.message.set(f"{self.title}: No solution.")
        print_result(self.title, grid, solved, seconds)  

    # its a function that loads a different puzzle of the same difficulty
    def another_puzzle(self):
        grid, self.last_file = random_puzzle(self.level, self.last_file)
        self.puzzle = grid
        self.show_puzzle()
        print_unsolved(self.title, grid)


# its a function that opens the GUI window 
def open_window(puzzle, title, level, filename=None):
    if not HAVE_TK:
        return False
    try:
        root = tk.Tk()
    except tk.TclError:
        return False
    SudokuWindow(root, puzzle, title, level, filename)
    root.mainloop()  # keeps the window open until it is closed
    return True
    
# PART 4: MAIN PROGRAM

def main():
    if len(sys.argv) > 1:  # if the puzzle came from a file that the user inputed it loads it 
        try:
            grid = load_puzzle(sys.argv[1])
        except (OSError, ValueError) as error:
            print(f"Could not load puzzle: {error}")
            return
        title, level, filename = os.path.basename(sys.argv[1]), None, None
    else:  # it asks to pick a difficulty level and loads the file according to the level picked 
        try:
            level = ask_level()
            grid, filename = random_puzzle(level)
        except (EOFError, KeyboardInterrupt):
            print()
            return
        except (OSError, ValueError) as error:
            print(f"Could not load puzzle: {error}")
            return
        title = LEVELS[level]

    print_unsolved(title, grid)  # its displays the unsolved puzzle in the terminal 

    # open the GUI window to solve thew puzzle 
    if not open_window(grid, title, level, filename):
        print("\n(No window available on this computer, so solving in the terminal.)")
        solved, seconds = solve_timed(grid)
        print_result(title, grid, solved, seconds)


if __name__ == "__main__":
    main()
