import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal before printing the board
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(column):
    return 0 <= column < COLS

def is_column_full(board, column):
    return board[0][column] != " "

def place_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical and diagonal (both directions)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS[:2])  # Randomly choose first player
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")
        input_column = input().strip().upper()

        if len(input_column) != 1 or not input_column.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue
        
        column = ord(input_column) - 65
        
        if not is_valid_column(column):
            print("Invalid column. Please enter a letter corresponding to a valid column.")
            continue
        
        if is_column_full(board, column):
            print("Column is full. Please choose another column.")
            continue
        
        place_checker(board, column, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw.")
            break

        # Switch players
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % len(PLAYERS[:2])]

if __name__ == "__main__":
    main()
