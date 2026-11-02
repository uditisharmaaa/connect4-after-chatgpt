import os
import random
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Supports 2 to 5 players
WIN_LENGTH = 4   # Always 4 to win
TOKENS = ['X', 'O', 'V', 'H', 'M']  # In order

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # Supports up to 26 columns (A-Z)
    if cols < 1 or cols > 26:
        raise ValueError("Number of columns must be between 1 and 26.")
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    print("  " + "   ".join(labels))
    # Rows
    horiz = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(horiz)
        row_line = "|"
        for c in range(len(board[0])):
            row_line += f" {board[r][c]} |"
        print(row_line)
    print(horiz)

def parse_input_to_col(user_input, cols):
    if not user_input or len(user_input) != 1:
        return None
    ch = user_input.upper()
    labels = column_labels(cols)
    if ch not in labels:
        return None
    return ord(ch) - ord('A')

def find_drop_row(board, col):
    # Return the row index where the checker will land, or None if the column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def place_checker(board, col, token):
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return row

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, token):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def is_winner_after_move(board, last_r, last_c, token):
    # Check four directions (horizontal, vertical, diag down-right, diag down-left)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = (
            count_in_direction(board, last_r, last_c, dr, dc, token) +
            count_in_direction(board, last_r, last_c, -dr, -dc, token) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False
    return True

def next_player_index(current, total):
    return (current + 1) % total

def main():
    # Validate player count and tokens
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.", file=sys.stderr)
        return
    tokens = TOKENS[:NUM_PLAYERS]

    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_token = tokens[current_player]
        print(f"Player {current_token}, please enter a column:", end=' ')
        user_input = input().strip()

        # Validate input (reprompt on invalid input)
        col = parse_input_to_col(user_input, COLS)
        while col is None:
            print("Invalid input. Please enter a valid column letter:", end=' ')
            user_input = input().strip()
            col = parse_input_to_col(user_input, COLS)

        # Check if column is full -> player loses turn
        drop_row = find_drop_row(board, col)
        if drop_row is None:
            print("Column is full. You lose your turn.")
            current_player = next_player_index(current_player, NUM_PLAYERS)
            continue

        # Place checker
        placed_row = place_checker(board, col, current_token)

        # Update screen and board
        clear_screen()
        print_board(board)

        # Check win
        if is_winner_after_move(board, placed_row, col, current_token):
            print(f"Player {current_token} won!")
            break

        # Check draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player_index(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    main()
