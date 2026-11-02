import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

# Initialize board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Validates input
def valid_input(input, board):
    return input in [chr(65 + i) for i in range(COLS)] and board[0][ord(input) - 65] == " "

# Place the checker in column
def place_checker(board, player, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[player]
            break

# Check win
def check_win(board, player):
    checker = CHECKERS[player]
    # Check horizontal, vertical and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if col <= COLS - 4 and all(board[row][col+i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row+i][col] == checker for i in range(4)):
                return True
            if col <= COLS - 4 and row <= ROWS - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if col >= 3 and row <= ROWS - 4 and all(board[row+i][col-i] == checker for i in range(4)):
                return True
    return False

# Check draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Play game
def play_connect4():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        player_input = input().strip().upper()
        if not valid_input(player_input, board):
            continue
        place_checker(board, current_player, ord(player_input) - 65)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

# Run the game
play_connect4()
