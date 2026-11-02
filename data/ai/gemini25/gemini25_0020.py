import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4 # Number of checkers needed to win

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    Each cell is initialized with a whitespace.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Clears the screen and prints the current state of the board.
    """
    os.system('clear')  # Clear the screen

    # Print column labels
    header = "  "
    for i in range(NUM_COLS):
        header += f"{string.ascii_uppercase[i]}   "
    print(header)

    # Print top border
    print("+" + "---+" * NUM_COLS)

    # Print board rows
    for r in range(NUM_ROWS):
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * NUM_COLS)

def get_column_from_input(prompt):
    """
    Prompts the user for a column input (A, B, C, ...) and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        col_input = input(prompt).strip().upper()
        if len(col_input) == 1 and col_input in string.ascii_uppercase[:NUM_COLS]:
            return ord(col_input) - ord('A')
        else:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")

def place_checker(board, col, player_checker):
    """
    Places a checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from the bottom row
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False  # Column is full

# --- Win Condition Functions ---

def check_win(board, player_checker):
    """
    Checks if the given player has won horizontally, vertically, or diagonally.
    """
    return (check_horizontal_win(board, player_checker) or
            check_vertical_win(board, player_checker) or
            check_diagonal_win(board, player_checker))

def check_horizontal_win(board, player_checker):
    """
    Checks for 4 in a row horizontally.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - (WIN_LENGTH - 1)):
            if all(board[r][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_vertical_win(board, player_checker):
    """
    Checks for 4 in a row vertically.
    """
    for r in range(NUM_ROWS - (WIN_LENGTH - 1)):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal_win(board, player_checker):
    """
    Checks for 4 in a row diagonally (both directions).
    """
    # Check diagonals from bottom-left to top-right (positive slope)
    for r in range(NUM_ROWS - (WIN_LENGTH - 1)):
        for c in range(NUM_COLS - (WIN_LENGTH - 1)):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonals from top-left to bottom-right (negative slope)
    for r in range(WIN_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - (WIN_LENGTH - 1)):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_draw(board):
    """
    Checks if the board is completely full (a draw).
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's an empty space, not a draw yet
    return True  # Board is full

# --- Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner = None

    while not game_over:
        player_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {player_checker}, please enter a column:")

        column_placed = False
        while not column_placed:
            col_index = get_column_from_input(f"Player {player_checker}, please enter a column: ")
            if place_checker(board, col_index, player_checker):
                column_placed = True
            else:
                print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")

        print_board(board) # Print board after placing the checker

        if check_win(board, player_checker):
            winner = player_checker
            game_over = True
            print(f"Player {winner} won!")
        elif check_draw(board):
            game_over = True
            print("The board is full. It's a draw!")
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Main execution ---
if __name__ == "__main__":
    play_game()
