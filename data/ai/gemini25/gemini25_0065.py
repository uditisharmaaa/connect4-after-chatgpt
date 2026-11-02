import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers, chosen in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

# --- Board Printing ---
def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    # Clear screen for better game experience
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(NUM_COLS):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board content
    for r in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

# --- Game Logic Functions ---
def get_column_from_input(prompt):
    """
    Gets valid column input (A-Z) from the user.
    """
    while True:
        user_input = input(prompt).upper()
        if len(user_input) == 1 and user_input in string.ascii_uppercase[:NUM_COLS]:
            return ord(user_input) - ord('A')  # Convert char to 0-indexed column
        else:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")

def place_checker(board, col, checker):
    """
    Places a checker in the lowest available space in the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.
    A player wins if they have WIN_SEQUENCE_LENGTH checkers in a row
    (horizontally, vertically, or diagonally).
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full (a draw).
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's still an empty space
    return True  # Board is full

# --- Main Game Function ---
def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join([f'Player {p}' for p in players])}")
    print(f"Board size: {NUM_ROWS} rows, {NUM_COLS} columns")
    print(f"Win condition: {WIN_SEQUENCE_LENGTH} in a row")
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get and validate player input
        valid_move_made = False
        while not valid_move_made:
            chosen_col_char = input(f"Player {current_checker}, choose a column (A-{string.ascii_uppercase[NUM_COLS-1]}): ").upper()
            
            if len(chosen_col_char) != 1 or not ('A' <= chosen_col_char <= string.ascii_uppercase[NUM_COLS-1]):
                print("Invalid input. Please enter a single uppercase letter within the board range.")
                continue
            
            chosen_col = ord(chosen_col_char) - ord('A')
            
            if place_checker(board, chosen_col, current_checker):
                valid_move_made = True
            else:
                print(f"Column {chosen_col_char} is full. Please choose another column.")
        
        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Run the game ---
if __name__ == "__main__":
    play_connect_4()
