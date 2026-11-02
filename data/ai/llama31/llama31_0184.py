import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def initialize_board():
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + " ".join([chr(65+i) for i in range(BOARD_COLS)]))
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

# Check if a column is valid
def is_valid_column(board, column):
    return board[0][column] == " "

# Get the next available row in a column
def get_next_row(board, column):
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][column] == " ":
            return row
    return -1

# Check for a win
def check_win(board, player_checker):
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col] == player_checker and board[row][col+1] == player_checker and board[row][col+2] == player_checker and board[row][col+3] == player_checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS-3):
            if board[row][col] == player_checker and board[row+1][col] == player_checker and board[row+2][col] == player_checker and board[row+3][col] == player_checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS-3):
        for col in range(BOARD_COLS-3):
            if board[row][col] == player_checker and board[row+1][col+1] == player_checker and board[row+2][col+2] == player_checker and board[row+3][col+3] == player_checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col] == player_checker and board[row-1][col+1] == player_checker and board[row-2][col+2] == player_checker and board[row-3][col+3] == player_checker:
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

# Main game loop
def play_game():
    board = initialize_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    print("Player", current_player, "goes first.")
    while True:
        print_board(board)
        print("Player", current_player, ", please enter a column (A-", chr(64+BOARD_COLS), "): ")
        column = input().upper()
        while not column.isalpha() or not 'A' <= column <= chr(64+BOARD_COLS):
            print("Invalid column. Please enter a letter between A and", chr(64+BOARD_COLS), ":")
            column = input().upper()
        column = ord(column) - 65
        while not is_valid_column(board, column):
            print("Column is full. Please choose another column.")
            print("Player", current_player, ", please enter a column (A-", chr(64+BOARD_COLS), "): ")
            column = input().upper()
            column = ord(column) - 65
        row = get_next_row(board, column)
        board[row][column] = current_player
        if check_win(board, current_player):
            print_board(board)
            print("Player", current_player, "won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player)+1) % len(players)]

play_game()
