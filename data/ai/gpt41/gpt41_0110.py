import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYER_CHARS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Set to 2 for assignment
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def is_valid_column(col_str, cols):
    if len(col_str) != 1 or not col_str.isalpha() or not col_str.isupper():
        return False
    idx = ord(col_str) - ord('A')
    return 0 <= idx < cols

def is_column_full(board, col_idx):
    return all(row[col_idx] != " " for row in board)

def drop_checker(board, col_idx, checker):
    # Start from bottom row, find the first empty spot
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Check diagonal /
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Check diagonal \
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_valid_column(board, cols):
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if not is_valid_column(col_input, cols):
            print("Invalid input. Please enter a valid (A-{}) column.".format(chr(ord('A') + cols - 1)))
            continue
        col_idx = ord(col_input) - ord('A')
        if is_column_full(board, col_idx):
            print("Column is full. You lose your turn.")
            return None  # No valid move in this column, lose turn
        return col_idx

def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_CHARS[:NUM_PLAYERS]
    player_names = ["Player {}".format(p) for p in players]
    current_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print("{} ({}), starts first!".format(player_names[current_idx], players[current_idx]))
    input("Press Enter to start...")
    game_over = False
    winner = None
    turns = 0
    while not game_over:
        print_board(board)
        curr_player = players[current_idx]
        print("{}, it's your turn ({}).".format(player_names[current_idx], curr_player))
        col_idx = get_valid_column(board, COLS)
        if col_idx is None:
            # If column is full, skip the turn as per assignment
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue
        drop_checker(board, col_idx, curr_player)
        turns += 1
        if check_win(board, curr_player):
            print_board(board)
            print("{} won!".format(player_names[current_idx]))
            game_over = True
            winner = curr_player
            break
        if is_board_full(board):
            print_board(board)
            print("The board is full. It's a draw!")
            break
        current_idx = (current_idx + 1) % NUM_PLAYERS
    # End of game
    print("Game over.")

if __name__ == "__main__":
    main()
