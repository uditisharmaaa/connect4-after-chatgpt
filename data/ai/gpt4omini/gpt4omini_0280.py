import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # Extend this for more players

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= 'G'

def place_checker(board, column, checker):
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical and diagonal
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
        for c in range(3, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_checker = PLAYERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column (A-G): ").upper()

        while not is_valid_input(column) or not place_checker(board, column, current_checker):
            print("Invalid input or column full. Try again.")
            column = input(f"Player {current_checker}, please enter a column (A-G): ").upper()

        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
