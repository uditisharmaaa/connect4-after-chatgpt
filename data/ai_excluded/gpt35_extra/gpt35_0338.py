import os
import random

# Constants for the game dimensions and players
ROWS = 6          # Number of rows
COLS = 7          # Number of columns (max 26)
NUM_PLAYERS = 2   # Number of players (between 2 and 5)
WIN_COUNT = 4     # Number of consecutive checkers needed to win

# Players' checkers symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constants to adhere to assignment constraints
assert 1 <= ROWS
assert 1 <= COLS <= 26
assert 2 <= NUM_PLAYERS <= 5

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column labels and grid borders."""
    cols = len(board[0])
    
    # Print column labels from A onwards
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Print top border
    print("+---" * cols + "+")

    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")

def get_column_index(col_letter, cols):
    """
    Converts column letter (A-G) to zero based index.
    Returns index if valid, else None.
    """
    if len(col_letter) != 1:
        return None
    col_letter = col_letter.upper()
    index = ord(col_letter) - ord('A')
    if 0 <= index < cols:
        return index
    return None

def is_valid_input(user_input, cols):
    """
    Checks if the user input is a single letter corresponding to a valid column.
    """
    return get_column_index(user_input, cols) is not None

def place_checker(board, col, checker):
    """
    Places the checker in the lowest empty space in the specified column.
    Returns True if placed successfully, False if the column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """
    Checks if the given checker has at least WIN_COUNT in a row
    horizontally, vertically or diagonally.
    Returns True if winning condition is met.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
                
    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
                
    # Diagonal check (/ diagonal)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal check (\ diagonal)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    """Checks if the board has any space left."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Create game board
    board = create_board(ROWS, COLS)
    
    # Determine players in use and their checkers
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    # Start game loop
    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        
        # Prompt for input until valid and non-full column or loses turn if full
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            # Validate input is a valid column letter within range
            if not is_valid_input(user_input, COLS):
                print("Invalid input. Please enter a letter corresponding to an available column (A-G).")
                continue
            
            col_idx = get_column_index(user_input, COLS)
            
            # Check if column is full
            if not place_checker(board, col_idx, current_checker):
                # Turn is lost if column full (inform the player)
                print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
                # Wait briefly before continuing to next player to show message
                input("Press Enter to continue...")
                break
            else:
                # Checker placed successfully, exit input loop
                break
        
        # Check if player won
        if check_winner(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            return
        
        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            return
        
        # Move to next player turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
