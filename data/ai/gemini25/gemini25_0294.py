import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current state of the board.
    """
    clear_screen()
    
    # Print column labels
    print(" ", end="")
    for col_label in COLUMN_LABELS:
        print(f" {col_label} ", end="")
    print()

    # Print the board
    for row in board:
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print the bottom border
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()

def get_player_input(player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").upper()
            
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            if user_input not in COLUMN_LABELS:
                print(f"Invalid column '{user_input}'. Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
                continue

            col_index = COLUMN_LABELS.index(user_input)
            return col_index
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the current state of the board.
        col_index (int): The 0-indexed column number where the checker is dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the current state of the board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(NUM_ROWS - WIN_CONDITION + 1):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(WIN_CONDITION - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row - i][col + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the current state of the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False  # There's still an empty space
    return True  # Board is full

# --- Main Game Logic ---

def play_connect_4():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        
        col_index = get_player_input(current_player_checker)
        
        if drop_checker(board, col_index, current_player_checker):
            # Check for win
            if check_win(board, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Column is full. Please choose another column.")
            # Player does not lose turn if column is full, they just retry.
            # The assignment says "the turn is invalid and the player loses the turn."
            # Reinterpreting this as the player must choose a valid column to complete their turn.
            # If the strict interpretation of "loses the turn" is required, remove the "else" block.
            # For now, I'll stick to the interpretation where the turn is not lost until a valid move is made.
            # If a strict "lose turn" is needed, the `current_player_index` would advance even on a full column.
            # For a first-year assignment, re-prompting is more common for invalid moves.
            # Let's re-read: "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
            # Okay, this means the player effectively passes their turn.
            # To implement that, we would simply advance `current_player_index` here.
            # Let's adjust for the strict interpretation.
            print(f"Player {current_player_checker} loses their turn because column {COLUMN_LABELS[col_index]} is full.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            
    print("Game over!")

# --- Start the game ---
if __name__ == "__main__":
    play_connect_4()
