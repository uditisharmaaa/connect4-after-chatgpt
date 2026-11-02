import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# The actual checkers used for the current game
GAME_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

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
        list: A 2D list representing the game board,
              initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))

    # Print the board rows
    for r in range(len(board)):
        print('+---+---' * len(board[0]) + '+')
        row_str = '|'
        for c in range(len(board[0])):
            row_str += f' {board[r][c]} |'
        print(row_str)
    print('+---+---' * len(board[0]) + '+')

def get_column_from_input(prompt_message):
    """
    Gets a valid column letter input from the player.

    Args:
        prompt_message (str): The message to display to the player.

    Returns:
        str: A valid uppercase column letter.
    """
    while True:
        try:
            user_input = input(prompt_message).strip().upper()
            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(user_input) - ord('A')
            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Column '{user_input}' is out of bounds. Please choose a column from A to {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The index of the column to place the checker.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical wins
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
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
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to play a game of Connect 4.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = GAME_CHECKERS[current_player_index]
        
        print_board(board)
        
        print(f"Player {current_checker}, it's your turn.")
        
        col_index = -1
        checker_placed = False
        while not checker_placed:
            col_index = get_column_from_input(f"Player {current_checker}, please enter a column: ")
            
            # Check if the column is full
            if board[0][col_index] != ' ': # If the top row of the chosen column is not empty
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                continue # Player does not lose turn, asks again
            
            checker_placed = place_checker(board, col_index, current_checker)
            if not checker_placed:
                # This should ideally not be reached if the above check for full column works,
                # but it's a safeguard.
                print(f"Could not place checker in column {chr(ord('A') + col_index)}. Please try again.")

        # After placing, print the board again to show the move
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    play_connect_4()
