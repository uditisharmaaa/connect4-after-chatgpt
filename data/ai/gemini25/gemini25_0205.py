import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear')  # Clear screen for Linux/Unix

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    
    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(board[r]) + " |")
    print("+---" * NUM_COLS + "+")

def get_column_from_input(prompt):
    """Gets and validates column input from the player."""
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + NUM_COLS - 1):
            return ord(col_input) - ord('A')
        else:
            print(f"Invalid input. Please enter a column letter from A to {chr(ord('A') + NUM_COLS - 1)}.")

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

# --- Win Condition Checks ---

def check_win(board, checker):
    """Checks if the given checker has won the game."""
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))

def check_horizontal_win(board, checker):
    """Checks for 4 in a row horizontally."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c+i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_vertical_win(board, checker):
    """Checks for 4 in a row vertically."""
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r+i][c] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_diagonal_win(board, checker):
    """Checks for 4 in a row diagonally (both directions)."""
    # Check positive slope diagonals (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_CONDITION)):
                return True
    
    # Check negative slope diagonals (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_draw(board):
    """Checks if the board is full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Empty space found, not a draw yet
    return True # No empty spaces, it's a draw

# --- Main Game Loop ---

def play_game():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        player_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        print(f"Player {player_checker}, please enter a column:")

        chosen_col = get_column_from_input(f"Player {player_checker}, your turn: ")
        
        if not drop_checker(board, chosen_col, player_checker):
            print(f"Column {chr(ord('A') + chosen_col)} is full. Please choose another column.")
            continue # Player's turn is not lost, they choose again

        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
