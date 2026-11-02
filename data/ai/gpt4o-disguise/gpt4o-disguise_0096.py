import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]

# Create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the game screen
    print("  ", end="")
    for i in range(COLS):
        print(chr(i + 65), end="   ")
    print()
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

# Check if input is valid
def is_valid_input(input, board):
    if len(input) != 1:
        return False
    if input not in [chr(i + 65) for i in range(COLS)]:
        return False
    col = ord(input) - 65
    if board[0][col] != " ":
        return False
    return True

# Place the checker in the chosen column
def place_checker(board, col, checker):
    for i in range(ROWS-1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            break

# Check for win condition
def check_win(board, checker):
    for i in range(ROWS):
        for j in range(COLS-3):
            if (board[i][j], board[i][j+1], board[i][j+2], board[i][j+3]) == (checker, checker, checker, checker):
                return True

    for i in range(ROWS-3):
        for j in range(COLS):
            if (board[i][j], board[i+1][j], board[i+2][j], board[i+3][j]) == (checker, checker, checker, checker):
                return True

    for i in range(ROWS-3):
        for j in range(COLS-3):
            if (board[i][j], board[i+1][j+1], board[i+2][j+2], board[i+3][j+3]) == (checker, checker, checker, checker):
                return True

    for i in range(3, ROWS):
        for j in range(COLS-3):
            if (board[i][j], board[i-1][j+1], board[i-2][j+2], board[i-3][j+3]) == (checker, checker, checker, checker):
                return True

    return False

# Check if the board is full
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        valid_input = False
        while not valid_input:
            player_input = input(f"Player {current_player}, please enter a column: ")
            valid_input = is_valid_input(player_input, board)

        col = ord(player_input) - 65
        place_checker(board, col, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

play_game()
