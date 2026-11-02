import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Board Initialization ---
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

# --- Board Display ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print()

    # Print the board content
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()

        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()

    # Print the bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

# --- Player Input and Validation ---
def get_player_input(player_checker, board):
    """
    Prompts the current player for a column choice and validates the input.
    Args:
        player_checker (str): The checker symbol for the current player.
        board (list): The 2D list representing the game board.
    Returns:
        int: The 0-indexed column chosen by the player.
    """
    num_cols = len(board[0])
    valid_columns = string.ascii_uppercase[:num_cols]

    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            column_input = input(prompt).upper()

            if not column_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(column_input) != 1:
                print("Invalid input. Please enter a single letter for the column (e.g., A).")
                continue

            if column_input not in valid_columns:
                print(f"Invalid column. Please choose a column from {valid_columns[0]} to {valid_columns[-1]}.")
                continue

            col_index = ord(column_input) - ord('A')

            if board[0][col_index] != " ":
                print(f"Column {column_input} is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")
        except IndexError:
            # This should ideally be caught by the `column_input not in valid_columns` check
            print("Invalid column. Please choose a column within the board limits.")

# --- Game Logic ---
def drop_checker(board, col_index, checker):
    """
    Drops the checker into the lowest available position in the chosen column.
    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is dropped.
        checker (str): The checker symbol to place.
    Returns:
        tuple: A tuple (row, col) of the placed checker's position, or None if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return None # Column is full (should be caught by input validation)

def check_win(board, checker, last_r, last_c):
    """
    Checks if the last placed checker resulted in a win.
    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player who just moved.
        last_r (int): The row index of the last placed checker.
        last_c (int): The column index of the last placed checker.
    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers
    def count_consecutive(delta_r, delta_c):
        count = 0
        # Check forward direction
        r, c = last_r, last_c
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += delta_r
            c += delta_c
        
        # Check backward direction (excluding the starting position to avoid double counting)
        r, c = last_r - delta_r, last_c - delta_c
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r -= delta_r
            c -= delta_c
        
        return count

    # Check horizontal
    if count_consecutive(0, 1) >= WIN_CONDITION:
        return True

    # Check vertical
    if count_consecutive(1, 0) >= WIN_CONDITION:
        return True

    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1) >= WIN_CONDITION:
        return True

    # Check anti-diagonal (top-right to bottom-left)
    if count_consecutive(1, -1) >= WIN_CONDITION:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.
    Args:
        board (list): The 2D list representing the game board.
    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full

# --- Main Game Loop ---
def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    player_indices = list(range(NUM_PLAYERS))
    current_player_index = random.choice(player_indices)
    
    game_over = False
    winner = None

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        
        col_index = get_player_input(current_checker, board)
        
        placed_pos = drop_checker(board, col_index, current_checker)
        
        if placed_pos: # If checker was successfully placed
            last_r, last_c = placed_pos
            if check_win(board, current_checker, last_r, last_c):
                winner = current_checker
                game_over = True
            elif check_draw(board):
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # else:
            # If drop_checker returns None, it means the column was full.
            # get_player_input should prevent this, so this case shouldn't be reached
            # if validation is robust. If it does, the current player does not lose their turn.

    # Game over, print final board and result
    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Entry Point ---
if __name__ == "__main__":
    play_connect_4()
