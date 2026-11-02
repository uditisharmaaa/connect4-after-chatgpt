import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = CHECKERS[:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board filled with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    Clears the screen before printing.
    """
    os.system('clear')  # Clear the console for a clean display

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(NUM_COLS):
        print(f"{chr(ord('A') + col_idx):^3}", end="")
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


def get_column_index(column_char):
    """
    Converts a column letter (e.g., 'A') to its corresponding 0-based index.
    """
    return ord(column_char.upper()) - ord('A')

def is_valid_column_input(column_char):
    """
    Checks if the user's column input is valid (a single uppercase letter
    within the board's column range).
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return False
    
    col_idx = get_column_index(column_char)
    return 0 <= col_idx < NUM_COLS

def get_next_available_row(board, col_idx):
    """
    Finds the lowest available row in a given column.
    Returns -1 if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return -1 # Column is full

def place_checker(board, col_idx, player_checker):
    """
    Places the player's checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    row_idx = get_next_available_row(board, col_idx)
    if row_idx != -1:
        board[row_idx][col_idx] = player_checker
        return True
    return False

# --- Win Condition Functions ---

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = PLAYERS[current_player_idx]
        print_board(board)
        
        # Display whose turn it is
        print(f"Player {current_checker}, please enter a column: ", end="")

        valid_turn = False
        while not valid_turn:
            user_input = sys.stdin.readline().strip() # Use sys.stdin.readline for broader compatibility
            
            if not is_valid_column_input(user_input):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
                print(f"Player {current_checker}, please enter a column: ", end="")
                continue
            
            col_idx = get_column_index(user_input)
            
            if not place_checker(board, col_idx, current_checker):
                print(f"Column {user_input} is full. Please choose another column.")
                print(f"Player {current_checker}, please enter a column: ", end="")
            else:
                valid_turn = True
        
        # After placing the checker, check for win or draw
        if check_win(board, current_checker):
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True # It's a draw
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
    
    # Game Over
    print_board(board) # Print final board
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_connect_4()
