import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board,
              initialized with empty cells.
    """
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    
    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
        except Exception:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")

def place_checker(board, col_index, checker):
    """
    Places a checker in the specified column at the lowest available row.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number where the checker is to be placed.
        checker (str): The checker symbol to place.

    Returns:
        tuple: A tuple (row, col) indicating the position where the checker was placed,
               or None if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = checker
            return r, col_index
    return None  # Column is full

def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check for a win.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)
        
        col_index = get_column_input(current_player_checker, NUM_COLS)
        
        placement_result = place_checker(board, col_index, current_player_checker)
        
        if placement_result is None:
            print("Column is full! Please choose another column.")
            # Player does not lose turn if column is full, they just need to pick again
            continue 
        
        # Check for win
        if check_win(board, current_player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
            
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
