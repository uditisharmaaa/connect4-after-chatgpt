import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to clear the game screen
def clear_screen():
    os.system('clear')

# Function to create the board
def create_board():
    board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

# Function to print the board
def print_board(board, current_player):
    print("  A   B   C   D   E   F   G")
    for i in range(BOARD_ROWS):
        print("+---+---+---+---+---+---+---+")
        row = ""
        for j in range(BOARD_COLUMNS):
            row += "| " + board[i][j] + " "
        print(row + "|")
    print("+---+---+---+---+---+---+---+")
    print("Player " + CHECKERS[current_player] + ", please enter a column:")

# Function to get the column index from the user's input
def get_column_index(column):
    column_index = ord(column.upper()) - ord('A')
    return column_index

# Function to check if the user's input is valid
def is_valid_input(board, column):
    try:
        column_index = get_column_index(column)
        if column_index < 0 or column_index >= BOARD_COLUMNS:
            return False
        if board[0][column_index]!= " ":
            return False
        return True
    except ValueError:
        return False

# Function to place the checker on the board
def place_checker(board, column, player):
    column_index = get_column_index(column)
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][column_index] == " ":
            board[i][column_index] = CHECKERS[player]
            break

# Function to check for a win
def check_win(board, player):
    checker = CHECKERS[player]
    # Check horizontal
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == checker and board[i][j + 1] == checker and board[i][j + 2] == checker and board[i][j + 3] == checker:
                return True
    # Check vertical
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLUMNS):
            if board[i][j] == checker and board[i + 1][j] == checker and board[i + 2][j] == checker and board[i + 3][j] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == checker and board[i + 1][j + 1] == checker and board[i + 2][j + 2] == checker and board[i + 3][j + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for i in range(3, BOARD_ROWS):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == checker and board[i - 1][j + 1] == checker and board[i - 2][j + 2] == checker and board[i - 3][j + 3] == checker:
                return True
    return False

# Function to check for a draw
def check_draw(board):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS):
            if board[i][j] == " ":
                return False
    return True

# Main game loop
def play_game():
    board = create_board()
    players = random.sample(range(PLAYERS), PLAYERS)
    current_player = 0
    while True:
        clear_screen()
        print_board(board, current_player)
        column = input().strip()
        while not is_valid_input(board, column):
            print("Invalid input. Please enter a valid column.")
            column = input().strip()
        place_checker(board, column, players[current_player])
        if check_win(board, players[current_player]):
            clear_screen()
            print_board(board, current_player)
            print("Player " + CHECKERS[players[current_player]] + " won!")
            break
        elif check_draw(board):
            clear_screen()
            print_board(board, current_player)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

play_game()
