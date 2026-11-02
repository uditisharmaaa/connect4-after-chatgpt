import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]  # You can extend this list for more players (V, H, M)

# Initialize board
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def drop_checker(column, player):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return True
    return False

def valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLUMNS - 1)

def check_win(player):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == player for i in range(4)) or
                r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)) or
                r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == player for i in range(4)) or
                r - 3 >= 0 and c + 3 < COLUMNS and all(board[r - i][c + i] == player for i in range(4))):
                return True
    return False

def check_draw():
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main game loop
player_index = random.randint(0, len(PLAYERS) - 1)
while True:
    print_board()
    current_player = PLAYERS[player_index]
    
    # Get valid input from the player
    while True:
        column_input = input(f"Player {current_player}, please enter a column: ").upper()
        if valid_input(column_input):
            column = ord(column_input) - 65
            if drop_checker(column, current_player):
                break
            else:
                print("Column is full! Choose another column.")
        else:
            print("Invalid input! Please enter a valid column letter (A-G).")
    
    if check_win(current_player):
        print_board()
        print(f"Player {current_player} won!")
        break
    if check_draw():
        print_board()
        print("It's a draw!")
        break

    # Switch players
    player_index = (player_index + 1) % len(PLAYERS)
