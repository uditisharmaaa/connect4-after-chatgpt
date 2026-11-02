import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# --- Global Variables (initialized later) ---
board = []
players = []
current_player_index = 0

# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with empty cells.
    """
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))
    
    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding 0-based index.

    Args:
        col_char (str): The uppercase letter representing the column.

    Returns:
        int or None: The 0-based column index, or None if the character is invalid.
    """
    if len(col_char) == 1 and 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
        return ord(col_char) - ord('A')
    return None

def is_valid_move(col_index):
    """
    Checks if a move to the given column index is valid.

    Args:
        col_index (int): The 0-based column index.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    return 0 <= col_index < NUM_COLS and board[0][col_index] == EMPTY_CELL

def drop_checker(col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        col_index (int): The 0-based column index.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        int: The row index where the checker was placed, or -1 if the column was full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = checker
            return r
    return -1 # Should not happen if is_valid_move was called first

def check_win(row, col, checker):
    """
    Checks if the last placed checker at (row, col) resulted in a win.

    Args:
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if a win is detected, False otherwise.
    """
    # Helper to count consecutive checkers
    def count_consecutive(r_start, c_start, dr, dc, target_checker):
        count = 0
        for i in range(WIN_CONDITION):
            r, c = r_start + i * dr, c_start + i * dc
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == target_checker:
                count += 1
            else:
                break
        return count

    # Check horizontal
    for c_start in range(max(0, col - WIN_CONDITION + 1), min(NUM_COLS - WIN_CONDITION + 1, col + 1)):
        if count_consecutive(row, c_start, 0, 1, checker) == WIN_CONDITION:
            return True

    # Check vertical
    for r_start in range(max(0, row - WIN_CONDITION + 1), min(NUM_ROWS - WIN_CONDITION + 1, row + 1)):
        if count_consecutive(r_start, col, 1, 0, checker) == WIN_CONDITION:
            return True

    # Check main diagonal (top-left to bottom-right)
    for i in range(WIN_CONDITION):
        r_start = row - i
        c_start = col - i
        if 0 <= r_start <= NUM_ROWS - WIN_CONDITION and 0 <= c_start <= NUM_COLS - WIN_CONDITION:
            if count_consecutive(r_start, c_start, 1, 1, checker) == WIN_CONDITION:
                return True

    # Check anti-diagonal (top-right to bottom-left)
    for i in range(WIN_CONDITION):
        r_start = row - i
        c_start = col + i
        if 0 <= r_start <= NUM_ROWS - WIN_CONDITION and 0 <= c_start < NUM_COLS and \
           0 <= r_start + WIN_CONDITION - 1 < NUM_ROWS and \
           0 <= c_start - (WIN_CONDITION - 1) < NUM_COLS:
            if count_consecutive(r_start, c_start, 1, -1, checker) == WIN_CONDITION:
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

# --- Main Game Logic ---
def play_game():
    """Main function to run the Connect 4 game."""
    global board, players, current_player_index

    # Initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner = None

    while not game_over:
        print_board(board)
        
        current_player_checker = players[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        valid_input = False
        col_char = ""
        col_index = -1

        while not valid_input:
            col_char = input().strip().upper()
            col_index = get_column_index(col_char)

            if col_index is None:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B).")
            elif not (0 <= col_index < NUM_COLS):
                print(f"Column '{col_char}' is out of board range. Please enter a column from A to {string.ascii_uppercase[NUM_COLS-1]}.")
            elif not is_valid_move(col_index):
                print(f"Column '{col_char}' is full. Please choose another column.")
            else:
                valid_input = True

        # Place the checker
        row_placed = drop_checker(col_index, current_player_checker)

        # Check for win
        if check_win(row_placed, col_index, current_player_checker):
            print_board(board)
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End of game
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
