import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = 2

def create_board():
    """Create an empty board with whitespaces."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| {} |".format(" | ".join(row)))
    print("+---" * BOARD_COLS + "+")
    print("  A B C D E F G")

def is_valid_move(board, col):
    """Check if a column is not full."""
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Get the next available row in a column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row

def drop_checker(board, col, checker):
    """Drop a checker into a column."""
    row = get_next_open_row(board, col)
    board[row][col] = checker

def winning_move(board, checker):
    """Check for a winning move."""
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

def is_draw(board):
    """Check if the board is full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def game():
    """Play the game."""
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print("Player {}, please enter a column:".format(current_player))
        col = input().upper()
        if not col.isalpha() or not 'A' <= col <= 'G':
            print("Invalid input. Please enter a letter between A and G.")
            continue
        col = ord(col) - ord('A')
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        drop_checker(board, col, current_player)
        if winning_move(board, current_player):
            print_board(board)
            print("Player {} won!".format(current_player))
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

game()
