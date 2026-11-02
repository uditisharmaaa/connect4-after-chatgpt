import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column, board):
    if column not in range(COLS):
        return False
    return board[0][column] == " "

def get_column_choice(player):
    while True:
        choice = input(f"Player {PLAYER_SYMBOLS[player]}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(choice) != 1 or choice < 'A' or choice >= chr(65 + COLS):
            print("Invalid input. Please enter a letter representing a column.")
            continue
        column = ord(choice) - 65
        if is_valid_input(column, board):
            return column
        else:
            print("Column is full. Please choose another column.")

def place_checker(board, column, symbol):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = symbol
            return

def check_win(board, symbol):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == symbol:
                # Check horizontally
                if c + 3 < COLS and all(board[r][c + i] == symbol for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r + i][c] == symbol for i in range(4)):
                    return True
                # Check diagonally \
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == symbol for i in range(4)):
                    return True
                # Check diagonally /
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == symbol for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game loop
board = create_board()
current_player = random.randint(0, len(PLAYER_SYMBOLS) - 1)

print_board(board)

while True:
    column = get_column_choice(current_player)
    place_checker(board, column, PLAYER_SYMBOLS[current_player])

    print_board(board)

    if check_win(board, PLAYER_SYMBOLS[current_player]):
        print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
        break
    
    if check_draw(board):
        print("The game is a draw!")
        break

    current_player = (current_player + 1) % len(PLAYER_SYMBOLS)
