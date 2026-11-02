import os
import random
import sys

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Validate constants
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)

SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]
LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_and_print_board(board):
    os.system('clear')
    cols = len(board[0])
    rows = len(board)

    # Header with column letters
    print("  " + "   ".join(LETTERS[:cols]))
    # Print grid
    sep_line = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep_line)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep_line)

def input_column(prompt):
    while True:
        try:
            user_in = input(prompt).strip().upper()
        except EOFError:
            # Treat EOF as invalid input, reprompt
            continue
        if len(user_in) != 1 or not user_in.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(user_in) - ord('A')
        if 0 <= col < COLS:
            return col
        else:
            print(f"Invalid column. Please enter a letter between A and {LETTERS[COLS-1]}.")

def find_drop_row(board, col):
    # Return the lowest available row index in the column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def check_win(board, last_r, last_c, symbol):
    # Check 4 in a row including the last placed position
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal up-right
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # include last placed
        # forward
        r, c = last_r + dr, last_c + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = last_r - dr, last_c - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    # Randomly choose starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    clear_and_print_board(board)

    while True:
        symbol = SYMBOLS[current_player]
        # Show board and prompt
        clear_and_print_board(board)
        prompt = f"Player {symbol}, please enter a column: "
        col = input_column(prompt)

        drop_row = find_drop_row(board, col)
        if drop_row is None:
            # Column full, turn lost
            print(f"Column {LETTERS[col]} is full. Player {symbol} loses the turn.")
            input("Press Enter to continue...")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker
        board[drop_row][col] = symbol

        # Print updated board
        clear_and_print_board(board)

        # Check for win
        if check_win(board, drop_row, col, symbol):
            print(f"Player {symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
