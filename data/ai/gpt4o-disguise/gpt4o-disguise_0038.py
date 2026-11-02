import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(chr(i) for i in range(65, 65 + BOARD_COLS)))
    print("+" + "---+" * BOARD_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * BOARD_COLS)

def make_move(board, col, symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            return True
    return False

def check_win(board, player):
    # Horizontal & vertical check
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS - 3):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True
    for r in range(BOARD_ROWS - 3):
        for c in range(BOARD_COLS):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True
    # Diagonal check
    for r in range(BOARD_ROWS - 3):
        for c in range(BOARD_COLS - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True
    for r in range(3, BOARD_ROWS):
        for c in range(BOARD_COLS - 3):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def valid_input(input_str, num_cols):
    if len(input_str) != 1:
        return False
    if not input_str.isalpha():
        return False
    col = ord(input_str.upper()) - 65
    if col < 0 or col >= num_cols:
        return False
    return True

def main():
    players = ['X', 'O']  # 2 players game
    current_player = random.choice(players)
    board = create_board()
    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip()
        while not valid_input(col_input, BOARD_COLS):
            col_input = input(f"Invalid input! Player {current_player}, please enter a column again: ").strip()

        col = ord(col_input.upper()) - 65
        if make_move(board, col, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = 'X' if current_player == 'O' else 'O'
        else:
            print(f"Column {col_input} is full! Player {current_player} loses the turn.")

main()
