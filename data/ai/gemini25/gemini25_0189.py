import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns supported by label generation
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_LENGTH = 4

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# --- Board Initialization ---
def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def get_column_labels(cols):
    """Generates column labels A, B, C..."""
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board):
    """Prints the Connect 4 board."""
    os.system('clear')  # Clear the screen

    column_labels = get_column_labels(len(board[0]))
    print("  " + "   ".join(column_labels))

    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

# --- Game Logic ---
def get_player_input(player_checker, board):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    column_labels = get_column_labels(len(board[0]))
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(user_input) != 1 or user_input not in column_labels:
                print(f"Invalid input. Please enter a single letter from {column_labels[0]} to {column_labels[-1]}.")
                continue

            col_index = ord(user_input) - ord('A')
            if col_index < 0 or col_index >= len(board[0]):
                print("Invalid column. Please choose a column within the board limits.")
                continue

            # Check if column is full
            if board[0][col_index] != EMPTY_CELL:
                print("This column is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, checker):
    """
    Drops the checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            board[r][col] = checker
            return True
    return False # Column is full (should be caught by input validation)

def check_win(board, checker):
    """Checks if the given checker has won the game."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_draw(board):
    """Checks if the board is completely full (a draw)."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

# --- Main Game Function ---
def play_connect4():
    """Main function to play Connect 4."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner = None

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)

        col_to_play = get_player_input(current_player_checker, board)
        drop_checker(board, col_to_play, current_player_checker)

        if check_win(board, current_player_checker):
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_connect4()
