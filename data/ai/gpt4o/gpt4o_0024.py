import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Global variable for board
board = []

def clear_screen():
    os.system('clear')

def print_board():
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def initialize_board():
    global board
    board = [[" "] * COLUMNS for _ in range(ROWS)]

def is_full():
    return all(board[0][col] != " " for col in range(COLUMNS))

def drop_checker(col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None

def is_winning_move(row, col, checker):
    # Check horizontal
    count = 0
    for c in range(COLUMNS):
        count = count + 1 if board[row][c] == checker else 0
        if count == 4:
            return True

    # Check vertical
    count = 0
    for r in range(ROWS):
        count = count + 1 if board[r][col] == checker else 0
        if count == 4:
            return True

    # Check diagonal /
    count = 0
    for d in range(-min(col, ROWS - 1 - row), min(COLUMNS - col, row + 1)):
        if board[row - d][col + d] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal \
    count = 0
    for d in range(-min(col, row), min(COLUMNS - col, ROWS - row)):
        if board[row + d][col + d] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    return False

def get_valid_column():
    while True:
        col_input = input("Enter a column: ").strip().upper()
        if len(col_input) != 1 or not 'A' <= col_input <= 'A' + chr(COLUMNS - 1):
            print("Invalid column. Try again.")
            continue
        col = ord(col_input) - ord('A')
        if board[0][col] == " ":
            return col
        else:
            print("Column is full. Try again.")

def play_game():
    initialize_board()
    num_players = 2
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    print_board()
    while not is_full():
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn.")
        col = get_valid_column()
        row = drop_checker(col, current_player)

        print_board()

        if is_winning_move(row, col, current_player):
            print(f"Player {current_player} won!")
            return

        current_player_index = (current_player_index + 1) % num_players

    print("The game is a draw!")

if __name__ == "__main__":
    play_game()
