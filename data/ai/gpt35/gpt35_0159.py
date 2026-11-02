import os
import random
import string

# CONSTANTS
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS_COUNT = 2  # Change this number between 2 and 5 (must be 2 for submission)
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Create a board filled with spaces (rows x cols)
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join(COLUMN_LABELS[:len(board[0])]))
    # Print rows and separators
    for row in board:
        print('+' + '---+' * len(row))
        print('| ' + ' | '.join(row) + ' |')
    print('+' + '---+' * len(board[0]))

def get_valid_column_input(player, board):
    valid_columns = COLUMN_LABELS[:len(board[0])]
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        # Validate input: single uppercase letter, in valid range
        if len(choice) != 1 or choice not in valid_columns:
            # invalid input
            continue
        col_idx = valid_columns.index(choice)
        # Check if column is full
        if board[0][col_idx] != ' ':
            # column full = player loses turn
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available row of the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = checker
            return r, col_idx
    # Column full, shouldn't reach here because we check before placing
    return None

def check_winner(board, row, col, checker):
    # Check four directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    # Draw if top row has no empty spaces
    return all(cell != ' ' for cell in board[0])

def main():
    # Validate constants for submission requirements
    if ROWS != 6 or COLUMNS != 7 or PLAYERS_COUNT != 2:
        # Per assignment submission instructions board must be 6x7 and 2 players enabled
        print("Error: Board dimensions must be 6x7 and number of players must be 2 for submission.")
        return

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS_COUNT]

    # Randomly select starting player index
    current_player_index = random.randint(0, PLAYERS_COUNT - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        col_idx = get_valid_column_input(current_checker, board)

        if col_idx is None:
            # Column full, player loses turn silently (no re-input)
            # Just print board and go next player
            print_board(board)
            current_player_index = (current_player_index + 1) % PLAYERS_COUNT
            continue

        row_idx, _ = place_checker(board, col_idx, current_checker)
        print_board(board)

        # Check win
        if check_winner(board, row_idx, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
