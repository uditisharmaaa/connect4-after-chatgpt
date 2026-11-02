import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Extend as needed

# Initialize board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Choose starting player
def choose_starting_player():
    return random.randint(0, NUM_PLAYERS - 1)

# Get and validate player input
def get_valid_input():
    while True:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ")
        if len(column) == 1 and column.isalpha():
            col_index = ord(column.upper()) - 65
            if 0 <= col_index < COLS and board[0][col_index] == " ":
                return col_index
        print("Invalid input, try again.")

# Place checker
def place_checker(col_index):
    for row_index in range(ROWS-1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = CHECKERS[current_player]
            return row_index

# Check for a win
def check_for_win(row, col, player):
    # Horizontal, Vertical, Diagonal checks
    def check_direction(delta_row, delta_col):
        count = 1
        for d in [-1, 1]:
            r, c = row + d * delta_row, col + d * delta_col
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == CHECKERS[player]:
                count += 1
                r += d * delta_row
                c += d * delta_col
        return count >= 4

    return any(check_direction(delta_row, delta_col)
               for delta_row, delta_col in [(1, 0), (0, 1), (1, 1), (1, -1)])

# Check for draw
def check_for_draw():
    return all(board[0][c] != " " for c in range(COLS))

# Main game loop
board = create_board(ROWS, COLS)
current_player = choose_starting_player()

while True:
    print_board(board)
    col_index = get_valid_input()
    row_index = place_checker(col_index)
    
    if check_for_win(row_index, col_index, current_player):
        print_board(board)
        print(f"Player {CHECKERS[current_player]} won!")
        break
        
    if check_for_draw():
        print_board(board)
        print("The game is a draw!")
        break
        
    current_player = (current_player + 1) % NUM_PLAYERS
