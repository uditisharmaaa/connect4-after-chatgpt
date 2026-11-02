import os
import random

# --- Global Constants (for easy modification as per assignment) ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns as per requirement
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS] # Only use checkers up to NUM_PLAYERS

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def initialize_board(rows, cols):
    """
    Initializes a 2D list representing the game board with empty spaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list (list of lists) representing the game board,
              initialized with " " (whitespace) in each cell.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the current state of the game board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(NUM_COLS):
        print(f"   {chr(ord('A') + col_index)}", end="")
    print("\n+---+---+---+---+---+---+---+") # Top border (specific to 7 columns for example)

    # Print rows with checkers and separators
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n+---+---+---+---+---+---+---+") # Row separator
    print() # Add a newline for better spacing

def get_player_input(player_checker):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player (if valid).
    """
    while True:
        try:
            column_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if not column_input.isalpha() or len(column_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(column_input) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except ValueError:
            print("Invalid input. Please enter a letter.")

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row up
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game by getting WIN_CONDITION checkers
    in a row horizontally, vertically, or diagonally.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Helper function to check a line (horizontal, vertical, or diagonal)
    def check_line(r, c, dr, dc):
        count = 0
        for i in range(WIN_CONDITION):
            current_r, current_c = r + i * dr, c + i * dc
            if 0 <= current_r < NUM_ROWS and 0 <= current_c < NUM_COLS and \
               board[current_r][current_c] == player_checker:
                count += 1
            else:
                break
        return count == WIN_CONDITION

    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, 0, 1): # dr=0, dc=1 for horizontal
                return True

    # Check vertical wins
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if check_line(r, c, 1, 0): # dr=1, dc=0 for vertical
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, 1, 1): # dr=1, dc=1 for diagonal
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, -1, 1): # dr=-1, dc=1 for anti-diagonal
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
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full, it's a draw

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, checks for wins/draws, and manages game flow.
    """
    board = initialize_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False
    winner = None

    while not game_over:
        print_board(board)
        
        col_index = get_player_input(current_player_checker)

        # Attempt to drop the checker
        if drop_checker(board, col_index, current_player_checker):
            # Checker was placed successfully, now check for win/draw
            if check_win(board, current_player_checker):
                print_board(board) # Print final board with winning move
                winner = current_player_checker
                game_over = True
            elif check_draw(board):
                print_board(board) # Print final board
                game_over = True # No winner, but board is full
            else:
                # Game continues, switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = PLAYER_CHECKERS[current_player_index]
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn if column is full, they re-enter input
            # The loop will continue, asking the current player again.

    # Game ended, print results
    print_board(board) # Final print to show the end state
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Start the game ---
if __name__ == "__main__":
    play_connect_4()
