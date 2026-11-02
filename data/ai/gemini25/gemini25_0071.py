import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Clears the screen before printing.
    """
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f"   {chr(ord('A') + col_idx)}", end="")
    print("\n" + " +---" * len(board[0]) + "+")

    # Print rows with checkers
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n" + " +---" * len(board[0]) + "+")

def get_column_label(col_idx):
    """
    Converts a column index to its corresponding letter label (e.g., 0 -> 'A').
    """
    return chr(ord('A') + col_idx)

def get_column_index(column_label):
    """
    Converts a column letter label to its corresponding index (e.g., 'A' -> 0).
    Returns -1 if the label is invalid.
    """
    if len(column_label) == 1 and 'A' <= column_label <= get_column_label(NUM_COLS - 1):
        return ord(column_label) - ord('A')
    return -1

# --- Game Logic Functions ---

def is_valid_input(column_label):
    """
    Validates the player's column input.
    Checks if it's a single uppercase letter within the board's range.
    """
    if not isinstance(column_label, str) or len(column_label) != 1:
        return False
    
    col_idx = get_column_index(column_label)
    return 0 <= col_idx < NUM_COLS

def place_checker(board, col_idx, player_checker):
    """
    Places a checker in the lowest available space of the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # An empty space found, game is not a draw yet
    return True # Board is full

# --- Main Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_idx]
        print_board(board)
        
        print(f"Player {player_checker}, please enter a column:")
        
        col_input = input().strip().upper()
        
        if not is_valid_input(col_input):
            print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
            # Player does not lose turn for invalid input format
            continue 
        
        col_idx = get_column_index(col_input)
        
        if not place_checker(board, col_idx, player_checker):
            print(f"Column {col_input} is full. Please choose another column.")
            # Player loses turn if column is full
            # No `continue` here, as the problem statement says "the turn is invalid and the player loses the turn."
            # This implicitly means the turn passes to the next player.
            # If the intent was for them to retry, `continue` would be used here.
            # Given the exact wording, I will advance the player even if the column is full.
            # If this interpretation is incorrect, a `continue` here would keep the current player.
            # For strict interpretation:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS # Advance player even if column is full
            continue

        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_game()
