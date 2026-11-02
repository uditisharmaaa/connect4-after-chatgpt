import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers, ordered for easy selection
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.
    The board is a list of lists, where each inner list represents a row.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.
    Columns are labeled with letters (A, B, C, ...).
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print top border
    print("+---" * NUM_COLS + "+")

    # Print rows with checkers
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding
    0-based integer index. Returns -1 if invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= chr(ord('A') + NUM_COLS - 1):
        return ord(column_char) - ord('A')
    return -1

def is_valid_column_input(column_char):
    """
    Checks if the user's column input is a single uppercase letter
    within the valid range of columns for the board.
    """
    return get_column_index(column_char) != -1

def place_checker(board, col_index, checker):
    """
    Places a checker in the specified column. It falls to the lowest
    available row. Returns True if placement was successful, False if
    the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Column is full

# --- Win Condition Functions ---

def check_win(board, checker):
    """
    Checks if the given checker has won the game (4 in a row
    horizontally, vertically, or diagonally).
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
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randrange(NUM_PLAYERS) # Randomly choose first player
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get valid input from player
        col_input = input().strip().upper()
        while not is_valid_column_input(col_input):
            print("Invalid column. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1) + ":")
            col_input = input().strip().upper()

        col_index = get_column_index(col_input)

        # Try to place the checker
        if place_checker(board, col_index, current_checker):
            # Check for win
            if check_win(board, current_checker):
                winner_checker = current_checker
                game_over = True
            # Check for draw
            elif check_draw(board):
                game_over = True
        else:
            print_board(board) # Re-print board to show it's still the same
            print(f"Column {col_input} is full! Player {current_checker}, you lose this turn. Please choose another column:")
            # Player does not lose turn if column is full, they just need to re-enter
            continue # Continue to the current player's turn

        # Switch to next player if turn was valid
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over
    print_board(board) # Print final board
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
