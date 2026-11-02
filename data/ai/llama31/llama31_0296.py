import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with specified dimensions."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A", "B", "C", "D", "E", "F", "G")
    for i in range(BOARD_ROWS):
        print("+---" * BOARD_COLS)
        print("|", end="")
        for j in range(BOARD_COLS):
            print(f" {board[i][j]} |", end="")
        print()
    print("+---" * BOARD_COLS)

def is_valid_input(col):
    """Check if the input is a valid column."""
    return col.isalpha() and col.upper() in "ABCDEFG"

def get_column_number(col):
    """Convert column letter to column number."""
    return ord(col.upper()) - 65

def is_column_full(board, col):
    """Check if the column is full."""
    return board[0][col]!= " "

def get_next_open_row(board, col):
    """Get the next open row in a column."""
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][col] == " ":
            return i

def drop_checker(board, col, checker):
    """Drop a checker in a column."""
    row = get_next_open_row(board, col)
    board[row][col] = checker

def check_win(board, checker):
    """Check for a win."""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return " " not in [cell for row in board for cell in row]

def play_game():
    """Play the game."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        col = input(f"Player {current_player}, please enter a column: ")
        if not is_valid_input(col):
            print("Invalid input. Please try again.")
            continue
        col_num = get_column_number(col)
        if is_column_full(board, col_num):
            print("Column is full. Please try again.")
            continue
        drop_checker(board, col_num, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

play_game()
