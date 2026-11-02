import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    horizontal_line = "+" + "---+" * COLUMNS
    for row in range(ROWS):
        print(horizontal_line)
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " {} |".format(board[row][col])
        print(row_str)
    print(horizontal_line)

def get_valid_column_input(player_check):
    while True:
        user_input = input(f"Player {player_check}, please enter a column: ").strip()
        if len(user_input) != 1:
            # Invalid length
            print(f"Invalid input. Please enter a single letter from A to {COLUMN_LABELS[-1]}.")
            continue
        col_char = user_input.upper()
        if col_char not in COLUMN_LABELS:
            # Not a valid column label
            print(f"Invalid input. Please enter a letter from A to {COLUMN_LABELS[-1]}.")
            continue
        col_index = ord(col_char) - ord('A')
        return col_index

def place_checker(board, col, checker):
    # Place checker in the lowest empty row in col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full
    return None, None

def check_winner(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    # We'll check in 8 directions around (row, col) but effectively 4 pairs
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        col = get_valid_column_input(checker)
        row_placed, col_placed = place_checker(board, col, checker)
        if row_placed is None:
            # Column full, lose turn
            print(f"Column {COLUMN_LABELS[col]} is full, {checker} loses turn.")
            # Advance player anyway as per assignment
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)

        # Check for win
        if check_winner(board, row_placed, col_placed, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
