import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Extend for more players: ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print(" ", "   ".join(chr(65 + c) for c in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def place_checker(board, column, checker):
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal (positive and negative slope)
    for r in range(ROWS):
        for c in range(COLS):
            if (
                (c + 3 < COLS and all(board[r][c + i] == checker for i in range(4))) or  # Horizontal
                (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or  # Vertical
                (c + 3 < COLS and r + 3 < ROWS and all(board[r + i][c + i] == checker for i in range(4))) or  # Diagonal \
                (c - 3 >= 0 and r + 3 < ROWS and all(board[r + i][c - i] == checker for i in range(4)))  # Diagonal /
            ):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_checker = PLAYERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column: ").upper()
        
        while not is_valid_input(column) or not place_checker(board, column, current_checker):
            print("Invalid input. Please try again.")
            column = input(f"Player {current_checker}, please enter a column: ").upper()

        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
