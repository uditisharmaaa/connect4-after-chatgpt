import os
import random

ROWS = 6
COLS = 7
COL_LABELS = 'ABCDEFG'

# Tokens for players (max 5)
TOKENS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2 * COLS + 1))

def is_valid_column(col_idx, board):
    # Check col in range and top cell is empty (bottom of board = ROWS-1)
    return 0 <= col_idx < COLS and board[0][col_idx] == ' '

def drop_token(board, col_idx, token):
    # Start from bottom row find first empty slot
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = token
            return row, col_idx
    return -1, -1 # Shouldn't happen if validated

def check_winner(board, token):
    # Check horizontal, vertical, diagonal (both) for 4 in a row

    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == token for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == token for i in range(4)):
                return True

    # Diagonal down-right check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == token for i in range(4)):
                return True

    # Diagonal up-right check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == token for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])  # top row filled means board full

def get_player_count():
    while True:
        try:
            n = int(input(f"Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Please enter a valid integer.")

def get_move(player_token, board):
    while True:
        move = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if move in COL_LABELS:
            col_idx = COL_LABELS.index(move)
            if is_valid_column(col_idx, board):
                return col_idx
            else:
                print("That column is full. Choose another.")
        else:
            print("Invalid column. Choose a letter from A to G.")

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = TOKENS[:player_count]

    board = create_board()
    current_idx = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_idx]
        col = get_move(current_player, board)
        row, _ = drop_token(board, col, current_player)

        if check_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! Nobody wins.")
            break

        current_idx = (current_idx + 1) % player_count


if __name__ == "__main__":
    main()
