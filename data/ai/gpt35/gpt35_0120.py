import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Support up to 5 players
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print top border
    print('+' + '---+' * COLS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * COLS)


def is_valid_column(input_str):
    if len(input_str) != 1:
        return False
    if input_str not in COLUMN_LABELS:
        return False
    return True


def column_full(board, col_idx):
    # If top cell in the column is not empty, column is full
    return board[0][col_idx] != ' '


def place_checker(board, col_idx, checker):
    # Place from bottom row upwards the checker
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # Should not happen if checked with column_full before


def check_win(board, checker, last_row, last_col):
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the last placed checker
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    # If any top cell in any column is empty, board not full
    for col_idx in range(COLS):
        if board[0][col_idx] == ' ':
            return False
    return True


def input_column(current_player_checker):
    while True:
        print(f"Player {current_player_checker}, please enter a column:")
        user_input = input().strip().upper()
        if not is_valid_column(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = ord(user_input) - ord('A')
        if column_full(board, col_idx):
            # Player loses the turn according to assignment
            return None
        return col_idx


if __name__ == "__main__":
    # Setup
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]
        col_idx = input_column(current_checker)
        if col_idx is None:
            # Column full, player loses turn
            # Move to next player
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        move = place_checker(board, col_idx, current_checker)
        print_board(board)

        if check_win(board, current_checker, move[0], move[1]):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS
