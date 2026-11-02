import os
import random
import string

# ------------ Constants -------------
ROWS = 6                # Number of rows in the board
COLS = 7                # Number of columns in the board (max 26)
NUM_PLAYERS = 2         # Number of players (between 2–5)

CHECKERS = ['X', 'O', 'V', 'H', 'M']   # Symbols for players

assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
assert 1 <= COLS <= 26, "Number of columns must be between 1 and 26"

SELECTED_CHECKERS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()

    header = "  " + "   ".join(COL_LABELS)
    separator = "+" + "---+" * COLS

    print(header)
    for row in board:
        print(separator)
        print("|", end='')
        for cell in row:
            print(f" {cell} |", end='')
        print()
    print(separator)

def get_valid_column_input(board):
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COL_LABELS:
            print(f"Invalid input. Please enter a single letter between A and {COL_LABELS[-1]}.")
            continue

        col_idx = COL_LABELS.index(col_input)
        # Check if column is not full
        if board[0][col_idx] != ' ':
            print("Column is full! You lose your turn.")
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    # Place from bottom to top
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return board.index(row), col_idx
    # Should not happen if validated before

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def check_win(board, row, col, checker):
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Current placed checker
        # Check in both directions
        for step in [1, -1]:
            r, c = row, col
            while True:
                r += dr * step
                c += dc * step
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def main():
    board = create_board(ROWS, COLS)
    players = [f"Player {checker}" for checker in SELECTED_CHECKERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"{players[current_player_idx]}, you start!\n")

    winner = None

    while True:
        player_checker = SELECTED_CHECKERS[current_player_idx]
        player_name = players[current_player_idx]

        print_board(board)
        print(f"{player_name}, it is your turn.")

        col_idx = get_valid_column_input(board)
        if col_idx is None:
            # Lose turn if column is full
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row_idx, col_idx = place_checker(board, col_idx, player_checker)

        # Check for win
        if check_win(board, row_idx, col_idx, player_checker):
            print_board(board)
            print(f"{player_name} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
