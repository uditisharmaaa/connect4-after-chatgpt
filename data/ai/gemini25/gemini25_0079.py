import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

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
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS[:NUM_COLS]))
    
    # Print board
    for r in range(NUM_ROWS):
        print('+' + '---+' * NUM_COLS)
        row_str = '|'
        for c in range(NUM_COLS):
            row_str += f' {board[r][c]} |'
        print(row_str)
    print('+' + '---+' * NUM_COLS)

def get_player_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter (e.g., A, B).")
                continue

            if user_input not in COLUMN_LABELS[:NUM_COLS]:
                print(f"Invalid column '{user_input}'. Columns are from {COLUMN_LABELS[0]} to {COLUMN_LABELS[NUM_COLS-1]}.")
                continue

            col_index = ord(user_input) - ord('A')
            return col_index

        except ValueError:
            print("Invalid input. Please enter a column letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (True, row_index) if the checker was placed successfully,
               (False, -1) if the column is full.
    """
    if not (0 <= col_index < NUM_COLS):
        return False, -1 # Should already be validated by get_player_input, but good for robustness

    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True, r
    return False, -1  # Column is full

def check_win(board, row, col, checker):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        row (int): The row of the last placed checker.
        col (int): The column of the last placed checker.
        checker (str): The checker symbol of the last placed checker.

    Returns:
        bool: True if a win is found, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    # Start from the current position and expand outwards
    for start_row in range(max(0, row - WIN_CONDITION + 1), min(NUM_ROWS - WIN_CONDITION + 1, row + 1)):
        for start_col in range(max(0, col - WIN_CONDITION + 1), min(NUM_COLS - WIN_CONDITION + 1, col + 1)):
            if start_row >= 0 and start_col >= 0 and start_row + WIN_CONDITION <= NUM_ROWS and start_col + WIN_CONDITION <= NUM_COLS:
                diag_count = 0
                for i in range(WIN_CONDITION):
                    if board[start_row + i][start_col + i] == checker:
                        diag_count += 1
                    else:
                        break
                if diag_count == WIN_CONDITION:
                    return True

    # Check diagonal (top-right to bottom-left)
    # Start from the current position and expand outwards
    for start_row in range(max(0, row - WIN_CONDITION + 1), min(NUM_ROWS - WIN_CONDITION + 1, row + 1)):
        for start_col in range(max(0, col - WIN_CONDITION + 1), min(NUM_COLS - WIN_CONDITION + 1, col + 1)):
            # Adjust for the other diagonal direction
            current_diag_col = start_col + (WIN_CONDITION - 1)
            if current_diag_col < NUM_COLS: # Ensure the end of the diagonal is within bounds
                if start_row >= 0 and current_diag_col >= (WIN_CONDITION - 1) and start_row + WIN_CONDITION <= NUM_ROWS and current_diag_col - WIN_CONDITION + 1 >= 0:
                    diag_count = 0
                    for i in range(WIN_CONDITION):
                        if board[start_row + i][current_diag_col - i] == checker:
                            diag_count += 1
                        else:
                            break
                    if diag_count == WIN_CONDITION:
                        return True
    
    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # Board is full

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_COLS > 26:
        print("Error: Maximum 26 columns supported for labeling (A-Z). Please reduce NUM_COLS.")
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Get checkers for the specified number of players
    active_players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        current_player_checker = active_players[current_player_index]

        col_input_valid = False
        while not col_input_valid:
            col_index = get_player_input(current_player_checker)
            
            # Attempt to drop the checker
            placed, row_placed = drop_checker(board, col_index, current_player_checker)

            if placed:
                col_input_valid = True
            else:
                print(f"Column {COLUMN_LABELS[col_index]} is full. Please choose another column.")
        
        print_board(board)

        if check_win(board, row_placed, col_index, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
