import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """Creates an empty game board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    clear_screen()
    
    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for i in range(len(board[0])):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()

    # Print the board rows
    for r_idx in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for c_idx in range(len(board[0])):
            print(f" {board[r_idx][c_idx]} |", end="")
        print()
    
    # Print the last horizontal line
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def get_player_input(player_checker, board_cols):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + board_cols - 1)):
                print("Invalid input. Please enter a single letter corresponding to a column (e.g., A, B).")
                continue
            
            col_idx = ord(col_char) - ord('A')
            return col_idx
        except Exception:
            print("Invalid input. Please enter a single letter corresponding to a column (e.g., A, B).")

def place_checker(board, col_idx, player_checker):
    """
    Places the player's checker in the lowest available spot in the given column.
    Returns True if successful, False if the column is full.
    """
    for r_idx in range(len(board) - 1, -1, -1):
        if board[r_idx][col_idx] == " ":
            board[r_idx][col_idx] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal wins
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for r in range(rows - win_condition + 1):
        for c in range(cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """Checks if the board is completely full (a draw)."""
    for r_idx in range(len(board)):
        for c_idx in range(len(board[0])):
            if board[r_idx][c_idx] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found

# --- Main Game Logic ---

def play_game():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_idx]
        
        print_board(board)
        
        valid_turn = False
        while not valid_turn:
            col_idx = get_player_input(player_checker, NUM_COLS)
            
            if not (0 <= col_idx < NUM_COLS):
                print("Invalid column. Please choose a column within the board limits.")
                continue

            if place_checker(board, col_idx, player_checker):
                valid_turn = True
            else:
                print("That column is full! Please choose another column.")
        
        if check_win(board, player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
