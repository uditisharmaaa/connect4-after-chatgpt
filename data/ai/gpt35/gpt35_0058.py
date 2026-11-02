import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # max allowed columns
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Number of players and their checkers; adjust here if needed
NUM_PLAYERS = 2  # for submission, must be 2
PLAYER_MARKS = ["X", "O", "V", "H", "M"]  # up to 5 players

# Ensure constants are within valid bounds
assert 1 <= ROWS <= 100, "ROWS must be positive and reasonable"
assert 1 <= COLUMNS <= MAX_COLUMNS, f"COLUMNS must be between 1 and {MAX_COLUMNS}"
assert MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS, f"NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}"

# Function to create a blank board with white spaces
def create_board(rows, cols):
    # Board is list of rows, each row is list of cols filled with " "
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the board with format as specified
def print_board(board):
    os.system('clear')  # clear screen before printing
    rows = len(board)
    cols = len(board[0])
    # Print column headers as letters starting from 'A'
    headers = "  " + "   ".join(chr(ord('A') + c) for c in range(cols))
    print(headers)
    # Print top line of board
    line = "+" + "---+" * cols
    for r in range(rows):
        print(line)
        # Print row with checkers
        row_str = "| " + " | ".join(board[r][c] for c in range(cols)) + " |"
        print(row_str)
    print(line)

# Function to validate input from player: must be letter within board columns
def valid_input(user_input, cols):
    if len(user_input) != 1:
        return False
    col_index = ord(user_input) - ord('A')
    if 0 <= col_index < cols:
        return True
    return False

# Function to place checker in the correct position, or "lose turn" if full
def place_checker(board, col_index, checker):
    # Place at lowest available row in column
    # Start from bottom row (ROWS-1) to top (0)
    for row in range(len(board)-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True  # placed successfully
    return False  # column full, lose turn

# Function to check horizontal, vertical, diagonal wins
def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    win_length = 4

    # Horizontal check
    for r in range(rows):
        for c in range(cols - win_length + 1):
            if all(board[r][c + i] == checker for i in range(win_length)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - win_length + 1):
            if all(board[r + i][c] == checker for i in range(win_length)):
                return True

    # Diagonal check (down-right)
    for r in range(rows - win_length + 1):
        for c in range(cols - win_length + 1):
            if all(board[r + i][c + i] == checker for i in range(win_length)):
                return True

    # Diagonal check (down-left)
    for r in range(rows - win_length + 1):
        for c in range(win_length - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(win_length)):
                return True

    return False

# Check if board is full (draw)
def board_full(board):
    # If any cell in top row is empty, board not full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)

    # Select first player randomly
    current_player = random.randint(0, NUM_PLAYERS-1)

    print_board(board)

    while True:
        checker = PLAYER_MARKS[current_player]
        # Prompt player until valid move or column full (lose turn)
        while True:
            print(f"Player {checker}, please enter a column:")
            user_input = input().strip().upper()
            if not valid_input(user_input, COLUMNS):
                # Invalid input, ask again
                continue
            col_index = ord(user_input) - ord('A')
            placed = place_checker(board, col_index, checker)
            if not placed:
                # Column full, lose turn
                # break to switch player
                break
            else:
                # Checker placed successfully
                break

        print_board(board)

        # If placed successfully, check win condition
        if placed and check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw condition
        if board_full(board):
            print("The game is a draw.")
            break

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
