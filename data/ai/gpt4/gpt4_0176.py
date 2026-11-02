import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Create the board with ROWS and COLS
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(LETTERS[:len(board[0])])
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Convert column letter to index
def column_to_index(column):
    if column in LETTERS:
        return LETTERS.index(column)
    return -1

# Check if a column is valid and not full
def is_valid_move(board, col_index):
    if 0 <= col_index < len(board[0]) and board[0][col_index] == " ":
        return True
    return False

# Place the checker in the specified column
def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

# Check for a win on the board
def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Horizontal win
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == checker:
                return True

    # Vertical win
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == checker:
                return True

    # Diagonal down-right win
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == checker:
                return True

    # Diagonal up-right win
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == checker:
                return True

    return False

# Check if the board is full (draw)
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main game function
def connect4():
    # Create the board
    board = create_board(ROWS, COLS)

    # Initialize players
    current_players = CHECKERS[:PLAYERS]
    random.shuffle(current_players)
    current_player_idx = 0

    print_board(board)

    # Game loop
    while True:
        current_checker = current_players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        column = input("> ").strip().upper()
        col_idx = column_to_index(column)

        if col_idx == -1 or not is_valid_move(board, col_idx):
            print("Invalid column! Please try again.")
            continue

        place_checker(board, col_idx, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect4()
