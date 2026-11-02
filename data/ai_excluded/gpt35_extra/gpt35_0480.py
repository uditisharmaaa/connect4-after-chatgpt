import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
WIN_COUNT = 4

# For submission: 2 players, board 6x7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border
    print("+---" * COLUMNS + "+")
    for row in board:
        # Print each row with | and cells
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")


def is_valid_column(col_idx, board):
    # Check if column index is in bounds and column not full
    if 0 <= col_idx < COLUMNS:
        return board[0][col_idx] == " "
    return False


def get_valid_input(player):
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip()
        if len(choice) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        if choice not in COLUMN_LABELS:
            print(f"Invalid column. Please choose a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue
        col_idx = ord(choice) - ord('A')
        if not is_valid_column(col_idx, board):
            # Column full: player loses turn (do not re-prompt)
            print(f"Column {choice} is full. You lose your turn.")
            return None
        return col_idx


def place_checker(board, col_idx, checker):
    # Place checker in lowest available row in col_idx
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # Should not happen if checked before


def check_winner(board, checker, row, col):
    # Check all directions for 4 in a row

    def count_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]

    for dr, dc in directions:
        # Count how many consecutive checkers in positive and negative directions
        total = 1  # include placed checker
        total += count_direction(dr, dc)
        total += count_direction(-dr, -dc)
        if total >= WIN_COUNT:
            return True
    return False


def check_draw(board):
    # If top row of every column is filled, draw
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True


# Initialize board and game state
board = create_board(ROWS, COLUMNS)
current_player_idx = random.randint(0, NUM_PLAYERS - 1)

print_board(board)

while True:
    player = PLAYERS[current_player_idx]

    # Get player input
    col = get_valid_input(player)
    if col is None:
        # Player loses turn, do not place checker, next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print_board(board)
        continue

    # Place checker
    placed = place_checker(board, col, player)

    print_board(board)

    # Check winner
    if placed and check_winner(board, player, placed[0], placed[1]):
        print(f"Player {player} won!")
        break

    # Check draw
    if check_draw(board):
        print("The game is a draw!")
        break

    # Next player's turn
    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
