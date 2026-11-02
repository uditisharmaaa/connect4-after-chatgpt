import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # Extend this list if more players are needed

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal for visuals
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col.upper()) - 65

def place_checker(board, col, player):
    col_index = get_column_index(col)
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player
            return True
    return False

def check_winner(board, player):
    # Check horizontal, vertical and diagonal
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def connect_4():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col = input(f"Player {current_player}, please enter a column: ").strip().upper()

        while not is_valid_input(col) or not place_checker(board, col, current_player):
            print("Invalid input or column is full. Please try again.")
            col = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    connect_4()
