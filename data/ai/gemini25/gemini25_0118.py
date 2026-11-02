import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

# --- Board Printing ---
def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    # Clear screen for cleaner output
    # os.system('clear')  # This might not work on all systems (e.g., Windows)
    # Using print('\033c') or print('\x1bc') for better cross-platform clear
    print('\033c', end='') # ANSI escape code to clear screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(NUM_COLS):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board rows
    for row in board:
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

# --- Game Logic Functions ---
def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index, col_index  # Return success and placed position
    return False, -1, -1  # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win (horizontal, vertical, or diagonal).
    """
    # Check horizontal
    if check_line(board, checker, last_row, last_col, 0, 1): return True  # Right
    if check_line(board, checker, last_row, last_col, 0, -1): return True # Left

    # Check vertical
    if check_line(board, checker, last_row, last_col, 1, 0): return True  # Down
    # No need to check up for vertical as checkers only fall down

    # Check diagonal (top-left to bottom-right)
    if check_line(board, checker, last_row, last_col, 1, 1): return True   # Down-right
    if check_line(board, checker, last_row, last_col, -1, -1): return True # Up-left

    # Check diagonal (top-right to bottom-left)
    if check_line(board, checker, last_row, last_col, 1, -1): return True  # Down-left
    if check_line(board, checker, last_row, last_col, -1, 1): return True  # Up-right

    return False

def check_line(board, checker, r, c, dr, dc):
    """
    Helper function to check for WIN_CONDITION consecutive checkers
    in a given direction (dr, dc) starting from (r, c).
    """
    count = 0
    # Check in positive direction
    temp_r, temp_c = r, c
    while 0 <= temp_r < NUM_ROWS and 0 <= temp_c < NUM_COLS and board[temp_r][temp_c] == checker:
        count += 1
        temp_r += dr
        temp_c += dc
    
    # Check in negative direction (excluding the starting cell which was counted)
    temp_r, temp_c = r - dr, c - dc # Start one step back from original cell
    while 0 <= temp_r < NUM_ROWS and 0 <= temp_c < NUM_COLS and board[temp_r][temp_c] == checker:
        count += 1
        temp_r -= dr
        temp_c -= dc
    
    return count >= WIN_CONDITION

def is_board_full(board):
    """
    Checks if the board is completely filled (draw condition).
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Loop ---
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers for players
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {player_checkers[current_player_index]} starts!")

    game_over = False
    while not game_over:
        current_player_checker = player_checkers[current_player_index]
        
        col_index = get_column_input(current_player_checker)

        success, last_row, last_col = place_checker(board, col_index, current_player_checker)

        if not success:
            print(f"Column {chr(ord('A') + col_index)} is full. You lose your turn.")
            # Player loses turn if column is full
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Skip to next player's turn, do not print board yet for invalid turn
        
        print_board(board)

        if check_win(board, current_player_checker, last_row, last_col):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif is_board_full(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
