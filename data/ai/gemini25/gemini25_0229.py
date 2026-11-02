import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    os.system('clear')  # Clear screen for Linux/Unix

    # Print column labels
    print(" ", end="")
    for col in range(len(board[0])):
        print(f" {chr(ord('A') + col)} ", end="")
    print()

    # Print board
    for r in range(len(board)):
        print("+---+", end="")
        for _ in range(len(board[0]) - 1):
            print("---+", end="")
        print("---+")
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---+", end="")
    for _ in range(len(board[0]) - 1):
        print("---+", end="")
    print("---+")

def get_column_index(col_char):
    """
    Converts a column letter (A, B, ...) to a 0-based index.
    """
    return ord(col_char.upper()) - ord('A')

def is_valid_column_input(col_char, num_cols):
    """
    Checks if the column input is a valid letter within board boundaries.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return False
    col_index = get_column_index(col_char)
    return 0 <= col_index < num_cols

def get_next_available_row(board, col_index):
    """
    Finds the lowest available row in a given column, or -1 if column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return -1

def place_checker(board, player_checker, col_index):
    """
    Places a checker in the specified column. Returns True if successful, False if column is full.
    """
    row_index = get_next_available_row(board, col_index)
    if row_index != -1:
        board[row_index][col_index] = player_checker
        return True
    return False

# --- Win Condition Checks ---
def check_win(board, checker):
    """
    Checks if the given checker has formed a Connect 4.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full (a draw).
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---
def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        
        valid_turn = False
        while not valid_turn:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            if not is_valid_column_input(user_input, NUM_COLS):
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue
            
            col_index = get_column_index(user_input)
            
            if place_checker(board, current_checker, col_index):
                valid_turn = True
            else:
                print(f"Column {user_input} is full. Please choose another column.")
        
        # After placing the checker, check for win or draw
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_connect4()
