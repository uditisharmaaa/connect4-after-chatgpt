import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "
WIN_SEQUENCE_LENGTH = 4

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Clears the screen before printing.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board rows
    for row_index in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

        print("|", end="")
        for cell in board[row_index]:
            print(f" {cell} |", end="")
        print()

    # Print bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def get_column_input(current_player_checker, num_cols):
    """
    Gets and validates the player's column input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(user_input) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("Invalid input. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == EMPTY_CELL:
            board[row_index][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, rows):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (a draw).
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = players[current_player_index]
        
        print_board(board)
        
        col_input_valid = False
        while not col_input_valid:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            if drop_checker(board, col_index, current_player_checker):
                col_input_valid = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # Player does not lose turn, so they are asked again.

        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
