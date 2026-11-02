import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers - 'X' and 'O' for 2 players, up to 'M' for 5 players
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_SYMBOLS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    # Clear the terminal screen
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()

    # Print the board with separators
    for r in range(NUM_ROWS):
        print("+---+", end="")
        for _ in range(NUM_COLS - 1):
            print("---+", end="")
        print("---+")

        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()

    # Print the bottom border
    print("+---+", end="")
    for _ in range(NUM_COLS - 1):
        print("---+", end="")
    print("---+")

# --- Game Logic Functions ---

def get_column_input(current_player_symbol):
    """
    Prompts the current player for a column input and validates it.
    Repeatedly asks for input until a valid column letter is entered.

    Args:
        current_player_symbol (str): The symbol of the current player.

    Returns:
        int: The 0-indexed column number corresponding to the player's input.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_symbol}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, player_symbol):
    """
    Drops the player's checker into the specified column.
    The checker falls to the lowest available space.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number where the checker is to be dropped.
        player_symbol (str): The symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = player_symbol
            return True
    return False  # Column is full

def check_win(board, player_symbol):
    """
    Checks if the current player has won the game by getting 4 checkers in a row
    (horizontally, vertically, or diagonally).

    Args:
        board (list): The 2D list representing the game board.
        player_symbol (str): The symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - (WIN_CONDITION - 1)):
            if all(board[r][c + i] == player_symbol for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - (WIN_CONDITION - 1)):
            if all(board[r + i][c] == player_symbol for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(NUM_ROWS - (WIN_CONDITION - 1)):
        for c in range(NUM_COLS - (WIN_CONDITION - 1)):
            if all(board[r + i][c + i] == player_symbol for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - (WIN_CONDITION - 1)):
            if all(board[r - i][c + i] == player_symbol for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full (draw), False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, checks for wins/draws, and ends the game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_symbol = PLAYER_SYMBOLS[current_player_index]
        
        print_board(board)
        
        col_index = get_column_input(current_player_symbol)
        
        if drop_checker(board, col_index, current_player_symbol):
            # Checker was successfully dropped
            
            if check_win(board, current_player_symbol):
                print_board(board) # Show final board with winning move
                print(f"Player {current_player_symbol} won!")
                game_over = True
            elif check_draw(board):
                print_board(board) # Show final board
                print("It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column was full, current player loses turn (as per assignment spec)
            # The prompt says "the turn is invalid and the player loses the turn."
            # This implementation keeps the current player. If the intent was that
            # they get to try again without losing the turn, the `else` block
            # would need to be removed or modified to re-prompt.
            # Assuming "loses the turn" means the turn advances.
            print("That column is full. Player loses the turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # If the intent was to re-prompt the same player, remove the line above.
            # For this assignment, "loses the turn" implies passing it.

# Entry point of the program
if __name__ == "__main__":
    play_game()
