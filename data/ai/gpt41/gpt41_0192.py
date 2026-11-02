import os
import random
import sys

# --------------- CONSTANTS ---------------
NUM_ROWS = 6
NUM_COLS = 7        # can be any value, max 26
NUM_PLAYERS = 2     # can be between 2 and 5

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --------------- FUNCTIONS ---------------

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(f" {label}  ", end="")
    print()
    # Print horizontal line
    print("+" + "---+"*NUM_COLS)
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+"*NUM_COLS)

def get_valid_input(board):
    while True:
        move = input().strip().upper()
        if len(move) != 1 or move not in COLUMN_LABELS:
            print(f"Invalid input. Please enter one of {', '.join(COLUMN_LABELS)}:")
        else:
            col = COLUMN_LABELS.index(move)
            if board[0][col] != " ":
                print("Column is full! You lose your turn.")
                return None  # Lose the turn
            else:
                return col

def place_checker(board, col, symbol):
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col
    return None

def check_win(board, last_row, last_col, symbol):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1),  # diagonal /
    ]

    for dr, dc in directions:
        count = 1    # current checker
        # Forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    # Prepare game settings
    if NUM_COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: Board cannot have more than 26 columns and number of players must be 2-5.")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {player_symbols[current]}, please enter a column:")

    while True:
        # Input loop
        col = get_valid_input(board)
        if col is None:
            # Current player loses the turn if column is full
            current = (current + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            print(f"Player {player_symbols[current]}, please enter a column:")
            continue

        # Place checker and find the row
        row, _ = place_checker(board, col, player_symbols[current])

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row, col, player_symbols[current]):
            print(f"Player {player_symbols[current]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Move to next player
        current = (current + 1) % NUM_PLAYERS
        print(f"Player {player_symbols[current]}, please enter a column:")


if __name__ == "__main__":
    main()
