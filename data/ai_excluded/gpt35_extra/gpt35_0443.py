import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players supported
REQUIRED_TO_WIN = 4
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows with separators
    for row in board:
        print("+" + "---+" * COLUMNS)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * COLUMNS)

def get_valid_input(current_player):
    prompt = f"Player {current_player}, please enter a column: "
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1:
            # Must be a single character
            continue
        if user_input not in COLUMN_LABELS:
            continue
        return user_input

def place_checker(board, column_idx, checker):
    # Place checker at lowest empty slot in column
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][column_idx] == " ":
            board[row_idx][column_idx] = checker
            return row_idx, column_idx
    # Column full; invalid move
    return None

def check_winner(board, row, col, checker):
    def count_direction(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        ((0, 1), (0, -1)),
        ((1, 0), (-1, 0)),
        ((1, 1), (-1, -1)),
        ((1, -1), (-1, 1))
    ]

    for dir1, dir2 in directions:
        total = 1  # count current checker
        total += count_direction(*dir1)
        total += count_direction(*dir2)
        if total >= REQUIRED_TO_WIN:
            return True
    return False

def board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randrange(PLAYERS)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        col_letter = get_valid_input(checker)
        col_idx = COLUMN_LABELS.index(col_letter)
        pos = place_checker(board, col_idx, checker)
        if pos is None:
            # Column full, lose turn silently as per spec
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, pos[0], pos[1], checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
