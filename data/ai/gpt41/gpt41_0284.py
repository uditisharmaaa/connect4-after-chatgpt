import os
import random
import string
import sys

# ----------------- Constants --------------------
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2                    # Can be set to up to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = list(string.ascii_uppercase)[:COLUMNS]

# ----------------- Board Functions -----------------
def create_board(rows, cols):
    """Create and return a game board with whitespaces"""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clear screen and print the game board"""
    os.system('clear')     # Use 'cls' for Windows
    # Print column headers
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    print("+" + "---+" * COLUMNS)
    for row in board:
        line = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(line)
        print("+" + "---+" * COLUMNS)

# ----------------- Game Logic Functions -----------------

def valid_column(input_str):
    """Returns True if input_str is a valid column label"""
    return input_str in COLUMN_LABELS

def is_column_full(board, col):
    """Returns True if the specified column is full"""
    return board[0][col] != " "

def place_checker(board, col, checker):
    """Place checker in column col, return (row, col) or None if col is full"""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    return None

def check_for_win(board, player_checker):
    """Check all win conditions for current player."""
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Returns True if the board is full and no player has won."""
    return all(cell != " " for row in board for cell in row)

def get_column_index(input_str):
    """Returns index of column label (A -> 0, etc.)"""
    return COLUMN_LABELS.index(input_str)

def get_valid_input(board, player_checker):
    """Prompt current player until valid input is given."""
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single uppercase letter for a column.")
            continue
        if not valid_column(move):
            print(f"Invalid column. Enter one of: {' '.join(COLUMN_LABELS)}")
            continue
        col = get_column_index(move)
        if is_column_full(board, col):
            print(f"Column {move} is full. You lose your turn.")
            return None
        return col

# ----------------- Main Game Loop -----------------

def play_game():
    board = create_board(ROWS, COLUMNS)
    checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly choose first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"\nPlayer {checkers[current_player_idx]} goes first!\n")
    input("Press Enter to begin...")

    moves_played = 0
    while True:
        print_board(board)
        player_checker = checkers[current_player_idx]

        col = get_valid_input(board, player_checker)
        if col is not None:
            coords = place_checker(board, col, player_checker)
            moves_played += 1
            if check_for_win(board, player_checker):
                print_board(board)
                print(f"Player {player_checker} won!")
                break
            if check_for_draw(board):
                print_board(board)
                print("Game is a draw!")
                break
        # else: column is full, player loses turn

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# -------------- Entry Point ---------------------

if __name__ == "__main__":
    play_game()
