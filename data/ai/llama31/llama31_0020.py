import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(width, height):
    """
    Create a new Connect 4 board with the given width and height.
    """
    return [[" " for _ in range(width)] for _ in range(height)]

def print_board(board, width, height):
    """
    Print the Connect 4 board to the console.
    """
    os.system('clear')
    column_labels = "  A   B   C   D   E   F   G"
    print(column_labels[:width*4+1])
    for row in board:
        print("+---+" * width)
        print("|" + "|   ".join(row) + "|")
    print("+---+" * width)

def is_valid_move(board, column, width):
    """
    Check if a move is valid (i.e., the column is not full).
    """
    return board[0][column] == " "

def get_next_open_row(board, column, width):
    """
    Find the next open row in the given column.
    """
    for row in reversed(board):
        if row[column] == " ":
            return row

def drop_checker(board, column, checker, width):
    """
    Drop a checker into the given column.
    """
    next_open_row = get_next_open_row(board, column, width)
    next_open_row[column] = checker

def check_win(board, width, height, checker):
    """
    Check if the given player has won.
    """
    # Check horizontal locations for win
    for c in range(width-3):
        for r in range(height):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for c in range(width):
        for r in range(height-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(width-3):
        for r in range(height-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(width-3):
        for r in range(3, height):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

def play_game():
    """
    Play a game of Connect 4.
    """
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board, BOARD_WIDTH, BOARD_HEIGHT)
        print("Player", current_player, "please enter a column (A-" + chr(64 + BOARD_WIDTH) + "):")
        column = input().upper()
        if column < 'A' or column >= chr(65 + BOARD_WIDTH):
            print("Invalid column. Please try again.")
            continue
        column = ord(column) - 65

        if not is_valid_move(board, column, BOARD_WIDTH):
            print("Column is full. Please try again.")
            continue

        drop_checker(board, column, current_player, BOARD_WIDTH)

        if check_win(board, BOARD_WIDTH, BOARD_HEIGHT, current_player):
            print_board(board, BOARD_WIDTH, BOARD_HEIGHT)
            print("Player", current_player, "won!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

play_game()
