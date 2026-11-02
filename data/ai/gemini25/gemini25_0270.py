import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels (A, B, C, ...) and row separators.
    """
    os.system('clear')  # Clear the screen

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print the board content
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_index(col_input):
    """
    Converts a column letter (e.g., 'A', 'B') to a 0-based index.
    Returns -1 if the input is invalid.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return -1
    col_input = col_input.upper()
    col_index = ord(col_input) - ord('A')
    if 0 <= col_index < NUM_COLS:
        return col_index
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a chosen column is valid for placing a checker.
    A column is valid if it's within bounds and not full.
    """
    if col_index == -1:  # Invalid column input
        return False
    # Check if the top row of the chosen column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.
    Returns the row index where the checker was placed, or -1 if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return -1 # Column is full, should not happen if is_valid_move is checked

def check_win(board, checker):
    """
    Checks if the given checker has achieved 4 in a row horizontally, vertically, or diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full (no empty spaces left).
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        player_input = input().strip()
        col_index = get_column_index(player_input)

        if not is_valid_move(board, col_index):
            print("Invalid input or column is full. Please try again.")
            continue # Player does not lose turn

        # Place the checker
        drop_checker(board, col_index, current_checker)

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player_index]

# --- Start the game ---
if __name__ == "__main__":
    play_game()
