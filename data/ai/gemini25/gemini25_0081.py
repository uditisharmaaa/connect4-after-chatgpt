import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board rows and separators
    for row in board:
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom separator
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()


def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.

    Args:
        column_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= chr(ord('A') + NUM_COLS - 1):
        return ord(column_char) - ord('A')
    return -1

def is_valid_input(column_input, board):
    """
    Validates the player's column input.

    Args:
        column_input (str): The raw input from the player.
        board (list): The current game board.

    Returns:
        tuple: (bool, int) - True if valid, False otherwise. The integer is the column index
               if valid, otherwise -1.
    """
    if not column_input:
        print("Invalid input: Please enter a column letter.")
        return False, -1

    column_char = column_input.strip().upper()
    col_idx = get_column_index(column_char)

    if col_idx == -1:
        print(f"Invalid column: Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        return False, -1

    # Check if the column is full
    if board[0][col_idx] != " ":
        print(f"Column {column_char} is full. Please choose another column.")
        return False, -1

    return True, col_idx

def drop_checker(board, col_idx, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_idx (int): The 0-based index of the column.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed, False if the column is full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False # Should not happen if is_valid_input is called first

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly choose the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_idx]
        
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        player_input = input()
        is_valid, col_idx = is_valid_input(player_input, board)

        if not is_valid:
            # If input is invalid or column is full, the turn is not lost,
            # so we continue the loop to ask the same player again.
            continue
        
        # Place the checker
        drop_checker(board, col_idx, current_checker)

        # Check for win
        if check_win(board, current_checker):
            print_board(board) # Print final board
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board) # Print final board
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
