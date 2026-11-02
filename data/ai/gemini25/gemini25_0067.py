import os
import random
import string

# --- Global Constants (for easy modification as per assignment) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS] # Limit checkers to NUM_PLAYERS
WIN_CONDITION = 4 # Number of checkers in a row to win

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
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))

    for r in range(num_rows):
        # Print horizontal line separator
        print("+---" * num_cols + "+")
        # Print row content
        row_content = []
        for c in range(num_cols):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")
    # Print bottom horizontal line
    print("+---" * num_cols + "+")

def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        col_char = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not col_char:
            print("Invalid input. Please enter a letter.")
            continue

        if len(col_char) != 1 or not col_char.isalpha():
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")
            continue

        col_index = ord(col_char) - ord('A')

        if 0 <= col_index < num_cols:
            return col_index
        else:
            print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker of the current player.

    Returns:
        tuple: (True, row_index) if the checker was placed successfully,
               (False, None) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1): # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, r # Return success and the row where it was placed
    return False, None # Column is full

def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        player_checker (str): The checker of the current player.
        last_row (int): The row where the last checker was placed.
        last_col (int): The column where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Directions for checking (horizontal, vertical, diagonal)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]

    for dr, dc in directions:
        count = 0
        # Check in one direction
        for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
            r, c = last_row + i * dr, last_col + i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0 # Reset count if current position is not player_checker or out of bounds
    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False # Found an empty spot, not a draw
    return True # No empty spots found, it's a draw

# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    print_board(board)
    print(f"Player {CHECKERS[current_player_index]} starts!")

    while not game_over:
        player_checker = CHECKERS[current_player_index]
        
        valid_turn = False
        while not valid_turn:
            col_input = get_column_input(player_checker, NUM_COLS)
            success, placed_row = drop_checker(board, col_input, player_checker)

            if success:
                last_placed_row = placed_row
                last_placed_col = col_input
                valid_turn = True
            else:
                print(f"Column {string.ascii_uppercase[col_input]} is full. Please choose another column.")
        
        print_board(board)

        # Check for win after every turn
        if check_win(board, player_checker, last_placed_row, last_placed_col):
            print(f"Player {player_checker} won!")
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
