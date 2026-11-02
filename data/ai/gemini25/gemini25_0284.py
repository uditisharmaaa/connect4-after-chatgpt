import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

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

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board content
    for r_idx, row in enumerate(board):
        print("+", end="")
        print("---+", "---+" * (len(row) - 1))
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+", end="")
    print("---+", "---+" * (len(board[0]) - 1))

def get_column_input(current_player_checker, max_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        max_cols (int): The maximum number of columns allowed (for validation).

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            col_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_input.isalpha() or len(col_input) != 1:
                raise ValueError("Invalid input. Please enter a single letter (e.g., A, B).")

            col_index = ord(col_input) - ord('A')
            if not (0 <= col_index < max_cols):
                raise ValueError(f"Column '{col_input}' is out of board range (A-{chr(ord('A') + max_cols - 1)}).")
            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except EOFError:
            print("\nExiting game.")
            sys.exit(0)

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: (bool, int) - True if the checker was successfully placed, False otherwise.
               The second element is the row index where the checker was placed, or -1 if failed.
    """
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True, row_index
    return False, -1  # Column is full

def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Helper function to count consecutive checkers in a direction
    def count_direction(r_start, c_start, dr, dc):
        count = 0
        r, c = r_start, c_start
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        return count

    # Check horizontally
    count = count_direction(last_row, last_col, 0, 1) + count_direction(last_row, last_col, 0, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check vertically
    count = count_direction(last_row, last_col, 1, 0) + count_direction(last_row, last_col, -1, 0) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonally (top-left to bottom-right)
    count = count_direction(last_row, last_col, 1, 1) + count_direction(last_row, last_col, -1, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonally (top-right to bottom-left)
    count = count_direction(last_row, last_col, 1, -1) + count_direction(last_row, last_col, -1, 1) - 1
    if count >= WIN_CONDITION:
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
    for col in range(len(board[0])):
        if board[0][col] == " ":  # If the top row of any column is empty, board is not full
            return False
    return True

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker, NUM_COLS)

        placed, row_index = drop_checker(board, col_index, current_player_checker)

        if not placed:
            print(f"Column {chr(ord('A') + col_index)} is full. Player {current_player_checker} loses turn.")
            # Note: Assignment states "player loses turn" if column is full.
            # If the assignment meant the player gets to re-enter, remove the 'continue'
            # and wrap the column input in another loop for re-try.
            # For strict interpretation, we move to the next player.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        if check_win(board, current_player_checker, row_index, col_index):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_connect_4()
