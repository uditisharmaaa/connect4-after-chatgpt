import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))]))
    
    # Print board content
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        print("|" + "|".join([f" {board[r][c]} " for c in range(len(board[0]))]) + "|")
    print("+" + "---+" * len(board[0]))

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_column_input(current_player_checker):
    """
    Prompts the current player to enter a column and validates the input.

    Args:
        current_player_checker (str): The checker of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            
            # Check for empty input
            if not player_input:
                print("Invalid input. Please enter a column letter (e.g., A, B, C).")
                continue

            # Check if input is a single letter
            if len(player_input) != 1 or not 'A' <= player_input[0] <= chr(ord('A') + NUM_COLS - 1):
                print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            col_index = ord(player_input[0]) - ord('A')
            return col_index
        except (ValueError, IndexError):
            print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + NUM_COLS - 1)}.")

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    # Find the lowest available row in the column
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # An empty space is found, not a draw yet
    return True  # No empty spaces, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers for active players
    active_player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False

    while not game_over:
        current_player_checker = active_player_checkers[current_player_index]
        
        print_board(board)
        
        col_index = get_column_input(current_player_checker)

        # Validate column full
        if not drop_checker(board, col_index, current_player_checker):
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn if column is full
            continue 
        
        print_board(board) # Print board after valid move

        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
