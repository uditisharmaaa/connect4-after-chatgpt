import os
import random

# Constants for the game
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(width, height):
    """
    Create a 2D board with the given width and height.
    """
    return [[" " for _ in range(width)] for _ in range(height)]

def print_board(board):
    """
    Print the current state of the board.
    """
    os.system('clear')
    print("  A", end="")
    for col in range(1, BOARD_WIDTH):
        print("   " + chr(ord('A') + col), end="")
    print("\n" + "+---" * BOARD_WIDTH + "+")
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            print("| " + board[row][col] + " ", end="")
        print("|\n" + "+---" * BOARD_WIDTH + "+")

def is_valid_input(input_str):
    """
    Check if the input is a valid column letter.
    """
    if len(input_str)!= 1:
        return False
    if not input_str.isalpha():
        return False
    if not 'A' <= input_str <= chr(ord('A') + BOARD_WIDTH - 1):
        return False
    return True

def get_column_from_input(input_str):
    """
    Convert the input column letter to a column index.
    """
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, col):
    """
    Check if the given column is full.
    """
    return board[0][col]!= " "

def get_next_open_row(board, col):
    """
    Get the next open row in the given column.
    """
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def check_win(board, player_checker):
    """
    Check if the given player has won.
    """
    # Check horizontal locations for win
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == player_checker and board[r][c + 1] == player_checker and board[r][c + 2] == player_checker and board[r][c + 3] == player_checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == player_checker and board[r + 1][c] == player_checker and board[r + 2][c] == player_checker and board[r + 3][c] == player_checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == player_checker and board[r + 1][c + 1] == player_checker and board[r + 2][c + 2] == player_checker and board[r + 3][c + 3] == player_checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == player_checker and board[r - 1][c + 1] == player_checker and board[r - 2][c + 2] == player_checker and board[r - 3][c + 3] == player_checker:
                return True

def check_draw(board):
    """
    Check if the game is a draw.
    """
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == " ":
                return False
    return True

def game():
    """
    Main game loop.
    """
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        print("Player " + players[current_player_index] + ", please enter a column:")
        input_str = input().strip().upper()
        while not is_valid_input(input_str):
            print("Invalid input. Please enter a column letter.")
            input_str = input().strip().upper()
        col = get_column_from_input(input_str)
        if is_column_full(board, col):
            print("Column is full. Please choose another column.")
            continue
        row = get_next_open_row(board, col)
        board[row][col] = players[current_player_index]
        if check_win(board, players[current_player_index]):
            print_board(board)
            print("Player " + players[current_player_index] + " won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

game()
