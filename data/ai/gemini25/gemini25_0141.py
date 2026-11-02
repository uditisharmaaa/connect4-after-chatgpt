import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns for A-Z labels
NUM_PLAYERS = 2
WIN_CONDITION = 4

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Board Functions ---
def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear screen

    # Print column labels
    header = "  "
    for i in range(NUM_COLS):
        header += chr(ord('A') + i) + "   "
    print(header)

    # Print board content
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

# --- Game Logic Functions ---
def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        col_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + NUM_COLS - 1):
            return ord(col_input) - ord('A')
        else:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")

def place_checker(board, col, checker):
    """
    Places a checker in the lowest available space of the given column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    """Checks if the given checker has formed a WIN_CONDITION line."""
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_draw(board):
    """Checks if the board is completely full."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

# --- Main Game Loop ---
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker)

        if place_checker(board, col_index, current_player_checker):
            if check_win(board, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. You lose your turn.")
            # According to the prompt: "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
            # So, the current player index is not advanced, effectively losing their turn.
            
if __name__ == "__main__":
    main()
