import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers - extend this list if more players are needed
CHECKERS = ["X", "O", "V", "H", "M"]


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Clears the screen before printing.
    """
    os.system('clear')  # Clear the console screen

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for col_idx in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + col_idx)} ")
    sys.stdout.write("\n")

    # Print board rows and cells
    for row in board:
        sys.stdout.write("+")
        sys.stdout.write("---" * len(row))
        sys.stdout.write("+\n")
        sys.stdout.write("|")
        for cell in row:
            sys.stdout.write(f" {cell} |")
        sys.stdout.write("\n")

    sys.stdout.write("+")
    sys.stdout.write("---" * len(board[0]))
    sys.stdout.write("+\n")


def is_valid_column(column_char, num_cols):
    """
    Checks if the given column character is a valid column on the board.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return False
    
    col_idx = ord(column_char.upper()) - ord('A')
    return 0 <= col_idx < num_cols

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A') to its integer index.
    """
    return ord(column_char.upper()) - ord('A')

def drop_checker(board, col_idx, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_idx in range(len(board) - 1, -1, -1):  # Start from the bottom row
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_checker
            return True
    return False # Column is full

def get_player_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Keeps asking until valid input is received.
    """
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip()
        if is_valid_column(col_input, num_cols):
            return get_column_index(col_input)
        else:
            print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + num_cols - 1)}.")


# --- Win Condition Functions ---
def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False  # There's an empty space, so not a draw yet
    return True # Board is full


# --- Main Game Logic ---
def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS) # Randomly select first player

    game_over = False
    
    while not game_over:
        current_player_checker = players[current_player_idx]
        
        print_board(board)
        
        col_idx_to_drop = get_player_input(current_player_checker, NUM_COLS)

        if not drop_checker(board, col_idx_to_drop, current_player_checker):
            print(f"Column {chr(ord('A') + col_idx_to_drop)} is full. You lose your turn.")
            # Player loses turn, so do not advance to next player
        else:
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The board is full. It's a draw!")
                game_over = True
            else:
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS # Next player's turn

# --- Entry Point ---
if __name__ == "__main__":
    play_connect_4()
