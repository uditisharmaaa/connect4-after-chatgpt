import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for A-Z labeling)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# Valid checkers based on NUM_PLAYERS
CURRENT_PLAYER_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

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

def get_player_input(player_name, board):
    """
    Gets validated column input from the current player.

    Args:
        player_name (str): The checker symbol of the current player.
        board (list): The game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {player_name}, please enter a column: ").strip().upper()

            # Check if input is a single uppercase letter
            if not (len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + NUM_COLS - 1)):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
                continue

            col = ord(column_input) - ord('A')

            # Check if column is within bounds (already checked by char range, but good for robustness)
            if not (0 <= col < NUM_COLS):
                print("Invalid column. Column is out of board range.")
                continue

            # Check if the column is full
            if board[0][col] != " ": # Check the top-most cell of the column
                print("Column is full. Please choose another column.")
                continue

            return col
        except Exception:
            # Catch any unexpected errors, though the checks above should cover most
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    return False # Should not happen if get_player_input validates correctly

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal win
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical win
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal win (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal win (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the game is a draw (board is full).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        clear_screen()
        print_board(board)
        
        current_player_checker = CURRENT_PLAYER_CHECKERS[current_player_index]
        
        # Get valid column input from the current player
        col = get_player_input(current_player_checker, board)
        
        # Drop the checker
        # The drop_checker call here will always succeed because get_player_input validates against full columns.
        drop_checker(board, col, current_player_checker)
        
        # Check for a win
        if check_win(board, current_player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        
        # Check for a draw (only if no win)
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            game_over = True
            
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
