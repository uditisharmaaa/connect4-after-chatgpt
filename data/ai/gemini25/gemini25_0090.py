import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for letter labels)
NUM_PLAYERS = 2  # Number of players (2 to 5)
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# Get the checkers for the specified number of players
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Board Initialization and Printing ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    # Clear the terminal screen
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col in range(NUM_COLS):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()

    # Print the top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers and borders
    for row in range(NUM_ROWS):
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
        print()
        # Print horizontal separator for each row
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

# --- Player Input and Checker Placement ---

def get_player_input(current_player_checker):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        str: The validated uppercase column letter chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + NUM_COLS - 1):
                return column_input
            else:
                print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + NUM_COLS - 1)}.")

def place_checker(board, col_char, player_checker):
    """
    Places the player's checker in the lowest available space of the chosen column.

    Args:
        board (list): The 2D list representing the game board.
        col_char (str): The uppercase letter representing the chosen column.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    # Convert column character to a 0-indexed integer
    col_index = ord(col_char) - ord('A')

    # Check from the bottom up to find the first empty spot
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player_checker
            return True  # Checker placed successfully
    return False  # Column is full

# --- Win Condition Checking ---

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
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
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Main Game Loop ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, checks for wins/draws, and ends the game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_found = False

    while not game_over:
        current_player_checker = ACTIVE_CHECKERS[current_player_index]
        
        print_board(board)
        
        valid_turn = False
        while not valid_turn:
            column_choice = get_player_input(current_player_checker)
            valid_turn = place_checker(board, column_choice, current_player_checker)
            if not valid_turn:
                print(f"Column {column_choice} is full. Please choose another column.")

        # Print the board after a valid move
        print_board(board)

        # Check for a win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        # Check for a draw if no winner yet
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        
        # If game is not over, switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_connect_4()
