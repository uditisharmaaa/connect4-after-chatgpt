import os
import random
import string

# === CONSTANT VARIABLES ===
ROWS = 6             # Number of rows of the board
COLS = 7             # Number of columns of the board (cannot be more than 26)
NUM_PLAYERS = 2      # Number of players (between 2-5)
CHECKER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 supported
WIN_CONDITION = 4    # Number of checkers in a row to win

# === GAME BOARD SETUP ===
def create_board(rows, cols):
    """Creates and returns a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, col_labels):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal (use 'cls' on Windows)
    # Print column labels
    print("  ", end="")
    for label in col_labels:
        print(f" {label}  ", end="")
    print()
    # Print board
    horiz_line = "+" + "---+" * len(col_labels)
    for row in board:
        print(horiz_line)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print(horiz_line)

def get_col_labels(cols):
    """Returns a list of column labels (A, B, ..., up to max 26)."""
    return list(string.ascii_uppercase[:cols])

# === INPUT VALIDATION ===
def get_player_input(col_labels, player_symbol):
    """Prompts user for a valid column letter and returns its index."""
    while True:
        column = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(column) != 1 or column not in col_labels:
            print("Invalid input. Please enter a valid column letter.")
            continue
        return col_labels.index(column)

# === GAME LOGIC ===
def find_row_to_place(board, col):
    """Returns lowest available row in the column. If full, returns -1."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, row, col, symbol):
    """Place the checker for the player at the given row, col."""
    board[row][col] = symbol

def check_four_in_a_row(board, symbol):
    """Checks all directions for a win with the specified symbol."""
    rows, cols = len(board), len(board[0])
    # Horizontal, Vertical, Diagonal(\), Diagonal(/)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while (
                    0 <= nr < rows and
                    0 <= nc < cols and
                    board[nr][nc] == symbol
                ):
                    count += 1
                    if count == WIN_CONDITION:
                        return True
                    nr += dr
                    nc += dc
    return False

def check_draw(board):
    """Checks if the board is full (draw)."""
    for row in board:
        if " " in row:
            return False
    return True

# === MAIN GAME LOOP ===
def main():
    # Set up
    col_labels = get_col_labels(COLS)
    board = create_board(ROWS, COLS)
    players = [CHECKER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    # Select random player to start
    curr_player = random.randint(0, NUM_PLAYERS-1)
    print_board(board, col_labels)
    print(f"Randomly selected Player {players[curr_player]} to start!")
    
    while True:
        print_board(board, col_labels)
        col = get_player_input(col_labels, players[curr_player])
        row = find_row_to_place(board, col)
        if row == -1:
            print(f"Column {col_labels[col]} is full. Player {players[curr_player]} loses their turn!")
            curr_player = (curr_player + 1) % NUM_PLAYERS
            continue
        place_checker(board, row, col, players[curr_player])
        if check_four_in_a_row(board, players[curr_player]):
            print_board(board, col_labels)
            print(f"Player {players[curr_player]} won!")
            break
        if check_draw(board):
            print_board(board, col_labels)
            print("It's a draw!")
            break
        curr_player = (curr_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
