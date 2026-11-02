import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the Connect 4 board.
    """
    # Clear screen for cleaner output (specific to Linux/Unix)
    os.system('clear')

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    
    # Print board content
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * len(board[0]))

def get_empty_row(board, col):
    """
    Finds the lowest available row in a given column.
    Returns the row index, or -1 if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1 # Column is full

def place_checker(board, row, col, checker):
    """
    Places a checker on the board at the specified row and column.
    """
    board[row][col] = checker

# --- Input Validation and Game Logic ---

def get_player_move(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not player_input.isalpha() or len(player_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(player_input) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column '{player_input}'. Column must be between A and {COLUMN_LABELS[-1]}.")
            else:
                return col_index
        except EOFError:
            print("\nGame terminated by user.")
            sys.exit()
        except KeyboardInterrupt:
            print("\nGame terminated by user.")
            sys.exit()

def is_valid_move(board, col):
    """
    Checks if a column is a valid place to drop a checker (i.e., not full).
    """
    return get_empty_row(board, col) != -1

def check_win(board, checker):
    """
    Checks if the given player's checker has achieved a winning condition (4 in a row).
    Checks horizontally, vertically, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_index]} goes first!")

    game_over = False
    winner_found = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]

        # Get and validate player move
        chosen_col_index = get_player_move(current_player_checker)
        
        # Check if column is full
        if not is_valid_move(board, chosen_col_index):
            print(f"Column {COLUMN_LABELS[chosen_col_index]} is full. Please choose another column.")
            # Player does not lose turn, loop again for input
            continue 

        # Place checker
        row_to_place = get_empty_row(board, chosen_col_index)
        place_checker(board, row_to_place, chosen_col_index, current_player_checker)

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        
        # Check for draw if no win yet
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        
        # Switch to next player if game isn't over
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
