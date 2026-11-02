import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("|   " * BOARD_COLS + "|")
        print("| ", end="")
        for cell in row:
            print(cell, end=" | ")
        print()
        print("+---" * BOARD_COLS + "+")

def is_valid_input(column):
    """Check if the input is a valid column letter."""
    return 'A' <= column <= 'G'

def get_column_number(column):
    """Convert column letter to number (0-indexed)."""
    return ord(column) - ord('A')

def is_column_full(board, column):
    """Check if a column is full."""
    return board[0][column]!= " "

def get_next_open_row(board, column):
    """Find the next open row in a column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row

def drop_checker(board, row, column, checker):
    """Drop a checker into a column."""
    board[row][column] = checker

def check_win(board, checker):
    """Check if there is a win in any direction."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check if the board is full."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def game():
    """Main game loop."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print("Player", current_player, "turn. Choose a column (A-G):")
        column = input().upper()

        while not is_valid_input(column) or is_column_full(board, get_column_number(column)):
            if not is_valid_input(column):
                print("Invalid input. Please enter a column letter (A-G).")
            else:
                print("Column is full. Please choose another column.")
            column = input().upper()

        row = get_next_open_row(board, get_column_number(column))
        drop_checker(board, row, get_column_number(column), current_player)

        if check_win(board, current_player):
            print_board(board)
            print("Player", current_player, "won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

game()
