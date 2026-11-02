import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Add more players if needed: ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console output
    print("  " + "   ".join(chr(i + 65) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_idx(column):
    return ord(column) - 65

def drop_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom row
        if row[get_column_idx(column)] == " ":
            row[get_column_idx(column)] = checker
            return True
    return False  # The column is full

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal win
    for r in range(ROWS):
        for c in range(COLS):
            # Check horizontal
            if c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)):
                return True
            # Check vertical
            if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                return True
            # Check diagonal (bottom-left to top-right)
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            # Check diagonal (top-left to bottom-right)
            if r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select first player
    game_over = False

    print_board(board)

    while not game_over:
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()

        while not is_valid_input(column) or not drop_checker(board, column, current_player):
            if not is_valid_input(column):
                print("Invalid input. Please enter a letter between A and " + chr(65 + COLS - 1) + ":")
            else:
                print("Column is full. Please choose another column:")
            column = input().upper()

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
