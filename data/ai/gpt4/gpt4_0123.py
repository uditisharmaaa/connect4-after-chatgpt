import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Global Variables
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
player_symbols = CHECKERS[:PLAYERS]

def clear_screen():
    os.system('clear')

def print_board():
    clear_screen()
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def initialize_game():
    print_board()

def is_valid_column(col):
    return col.isalpha() and len(col) == 1 and 0 <= ord(col.upper()) - 65 < COLS

def is_column_full(col_num):
    for row in board:
        if row[col_num] == " ":
            return False
    return True

def place_checker(col_num, symbol):
    for row in reversed(board):
        if row[col_num] == " ":
            row[col_num] = symbol
            break

def check_win(symbol):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Vertical Check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Diagonal Check (Top-left to Bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Diagonal Check (Bottom-left to Top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw():
    return all(row[col] != " " for col in range(COLS) for row in board)

# Main Game Loop
def main():
    current_player = random.randint(0, PLAYERS - 1)
    initialize_game()

    while True:
        print_board()
        print(f"Player {player_symbols[current_player]}, please enter a column: ")
        
        col_input = input().strip().upper()
        
        while not is_valid_column(col_input):
            print("Invalid column. Try again.")
            col_input = input().strip().upper()

        col_num = ord(col_input) - 65
        
        if is_column_full(col_num):
            print("This column is full. You lose your turn.")
            current_player = (current_player + 1) % PLAYERS
            continue

        place_checker(col_num, player_symbols[current_player])

        if check_win(player_symbols[current_player]):
            print_board()
            print(f"Player {player_symbols[current_player]} won!")
            break

        if check_draw():
            print_board()
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
