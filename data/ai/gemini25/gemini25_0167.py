import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

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
        list: A 2D list representing the board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS[:NUM_COLS]))
    
    # Print top border
    print("+" + "---+-" * NUM_COLS)

    # Print rows with checkers and separators
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+" + "---+-" * NUM_COLS)

def get_valid_column_input(player_checker, board):
    """
    Prompts the current player for a column input and validates it.
    Keeps asking until a valid and available column is entered.

    Args:
        player_checker (str): The checker of the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., A, B).")
                continue

            col_char = user_input[0]
            if col_char not in COLUMN_LABELS[:NUM_COLS]:
                print(f"Invalid column '{col_char}'. Please enter a letter from A to {COLUMN_LABELS[NUM_COLS-1]}.")
                continue

            col_index = COLUMN_LABELS.index(col_char)

            if board[0][col_index] != " ":
                print("Column is full. Please choose another column.")
                continue

            return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single column letter (e.g., A, B).")

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The 0-indexed column number.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (row_index, col_index) of where the checker was placed, or None if column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    return None  # Column is full, though handled by get_valid_column_input

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Starting player is Player {players[current_player_index]}!")

    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = players[current_player_index]

        col_index = get_valid_column_input(current_checker, board)
        
        drop_checker(board, col_index, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board) # Print final board one last time

    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")
    
    print("Thanks for playing!")

if __name__ == "__main__":
    play_game()
