import os
import random
import string

# Constants - set for submission requirements
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players, use first NUM_PLAYERS for this game
WIN_COUNT = 4
COLUMN_LABELS = string.ascii_uppercase[:COLS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border and board rows
    row_border = "+" + "---+" * COLS
    for r in range(ROWS):
        print(row_border)
        print("| " + " | ".join(board[r]) + " |")
    print(row_border)

def is_valid_column(col):
    return col in COLUMN_LABELS

def is_column_full(board, col_idx):
    # If top row cell in this column is occupied, column is full
    return board[0][col_idx] != " "

def get_next_open_row(board, col_idx):
    # Returns the last free row in column or -1 if full
    for r in range(ROWS-1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return -1

def place_checker(board, col_idx, checker):
    row = get_next_open_row(board, col_idx)
    if row == -1:
        return False
    board[row][col_idx] = checker
    return True

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal check (positive slope)
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal check (negative slope)
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def check_draw(board):
    # If no empty spaces left in top row, board is full
    return all(cell != " " for cell in board[0])

def input_column(player, checker):
    while True:
        col = input(f"Player {checker}, please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input. Enter a single uppercase letter for the column.")
            continue
        if not is_valid_column(col):
            print("Invalid column letter. Please enter a valid column letter from A to {}.".format(COLUMN_LABELS[-1]))
            continue
        col_idx = COLUMN_LABELS.index(col)
        if is_column_full(board, col_idx):
            # Turn is lost if column full
            print(f"Column {col} is full. You lose your turn.")
            return -1
        return col_idx

# Initialize the game
board = create_board(ROWS, COLS)
players_checkers = CHECKERS[:NUM_PLAYERS]
# Choose random starting player index
current_player_idx = random.randint(0, NUM_PLAYERS - 1)

print_board(board)

while True:
    checker = players_checkers[current_player_idx]
    col_idx = input_column(current_player_idx, checker)
    if col_idx == -1:
        # Move lost, switch player and print board
        print_board(board)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        continue
    placed = place_checker(board, col_idx, checker)
    print_board(board)
    if not placed:
        # Should not happen due to prior full check, but safe fallback
        print(f"Column {COLUMN_LABELS[col_idx]} is full. You lose your turn.")
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        continue
    if check_win(board, checker):
        print(f"Player {checker} won!")
        break
    if check_draw(board):
        print("Game is a draw!")
        break
    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
