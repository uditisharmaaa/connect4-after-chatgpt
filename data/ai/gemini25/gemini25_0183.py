import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS_CHECKERS = CHECKERS[:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    """
    Prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))

    # Print board
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * len(board[0]))

# --- Game Logic ---

def get_player_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            if col_char not in COLUMN_LABELS:
                print(f"Invalid column. Please choose a column from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
                continue

            col_index = COLUMN_LABELS.index(col_char)
            return col_index
        except Exception:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: (True, row_index) if the checker was placed successfully,
               (False, None) if the column is full.
    """
    if board[0][col] != " ":  # Check if the top row of the column is occupied
        return False, None

    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True, r  # Return the row where the checker was placed
    return False, None # Should not be reached if board[0][col] check works

def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won the game after their last move.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        last_row (int): The row where the last checker was placed.
        last_col (int): The column where the last checker was placed.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    # Check horizontally
    if check_direction(board, player_checker, last_row, last_col, 0, 1): return True  # Right
    if check_direction(board, player_checker, last_row, last_col, 0, -1): return True # Left

    # Check vertically
    if check_direction(board, player_checker, last_row, last_col, 1, 0): return True  # Down
    if check_direction(board, player_checker, last_row, last_col, -1, 0): return True # Up

    # Check diagonally (top-left to bottom-right)
    if check_direction(board, player_checker, last_row, last_col, 1, 1): return True # Down-right
    if check_direction(board, player_checker, last_row, last_col, -1, -1): return True # Up-left

    # Check diagonally (top-right to bottom-left)
    if check_direction(board, player_checker, last_row, last_col, 1, -1): return True # Down-left
    if check_direction(board, player_checker, last_row, last_col, -1, 1): return True # Up-right

    return False

def check_direction(board, player_checker, start_row, start_col, dr, dc):
    """
    Checks for a win in a specific direction from a starting point.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol to look for.
        start_row (int): The starting row.
        start_col (int): The starting column.
        dr (int): The change in row for the direction (e.g., 1 for down).
        dc (int): The change in column for the direction (e.g., 1 for right).

    Returns:
        bool: True if WIN_CONDITION checkers are found in a row in that direction, False otherwise.
    """
    count = 0
    # Check in the positive direction
    for i in range(WIN_CONDITION):
        r, c = start_row + i * dr, start_col + i * dc
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
            count += 1
        else:
            break
    if count >= WIN_CONDITION:
        return True

    # Check in the negative direction (if dr, dc are not 0)
    count = 0
    for i in range(1, WIN_CONDITION): # Start from 1 to avoid double counting the starting cell
        r, c = start_row - i * dr, start_col - i * dc
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
            count += 1
        else:
            break
    
    # The total number of checkers connected in both directions through the last placed piece
    # Must include the last placed piece itself, so add 1 for it
    return (count + (WIN_CONDITION - 1) + 1) >= WIN_CONDITION 

def check_win_optimized(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won the game after their last move.
    This optimized version focuses on the vicinity of the last placed checker.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        last_row (int): The row where the last checker was placed.
        last_col (int): The column where the last checker was placed.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Horizontal, Vertical, Diagonal1, Diagonal2
    
    for dr, dc in directions:
        count = 1 # Start with 1 for the last placed checker itself

        # Check in positive direction
        for i in range(1, WIN_CONDITION):
            r, c = last_row + i * dr, last_col + i * dc
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                break
        
        # Check in negative direction
        for i in range(1, WIN_CONDITION):
            r, c = last_row - i * dr, last_col - i * dc
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                count += 1
            else:
                break
        
        if count >= WIN_CONDITION:
            return True
            
    return False


def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

# --- Main Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    game_over = False
    last_row_placed = -1
    last_col_placed = -1

    while not game_over:
        current_player_checker = PLAYERS_CHECKERS[current_player_index]
        print_board(board)
        
        valid_move = False
        while not valid_move:
            col_index = get_player_input(current_player_checker)
            placed, row_index = drop_checker(board, col_index, current_player_checker)

            if placed:
                valid_move = True
                last_row_placed = row_index
                last_col_placed = col_index
            else:
                print(f"Column {COLUMN_LABELS[col_index]} is full. Please choose another column.")
        
        # After a valid move, check for win or draw
        if check_win_optimized(board, current_player_checker, last_row_placed, last_col_placed):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
