import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Maximum 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"] # Symbols for players

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the Connect 4 board.
    """
    # Create a list of lists, where each inner list represents a row.
    # Initialize all cells with a single whitespace character.
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the Connect 4 board.
    """
    os.system('clear') # Clear the terminal screen before printing

    # Print column labels (A, B, C, ...)
    print(" ", end="") # Space for alignment with the '+'
    for col_idx in range(len(board[0])):
        # Convert column index to a letter (0 -> A, 1 -> B, etc.)
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print the board rows
    for row_idx in range(len(board)):
        # Print the top border of each row
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

        # Print the cells of the current row
        print("|", end="")
        for cell in board[row_idx]:
            print(f" {cell} |", end="")
        print()

    # Print the bottom border of the last row
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def get_column_from_letter(column_letter):
    """
    Converts a column letter (e.g., 'A', 'B') to its corresponding 0-based index.

    Args:
        column_letter (str): The uppercase letter representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(column_letter) == 1 and 'A' <= column_letter <= chr(ord('A') + NUM_COLS - 1):
        return ord(column_letter) - ord('A')
    return -1 # Indicate an invalid column letter

def get_letter_from_column(column_index):
    """
    Converts a 0-based column index to its corresponding letter.

    Args:
        column_index (int): The 0-based index of the column.

    Returns:
        str: The uppercase letter representing the column.
    """
    return chr(ord('A') + column_index)

def is_valid_column_input(column_letter):
    """
    Checks if the user's column input is valid.

    Args:
        column_letter (str): The user's input for the column.

    Returns:
        bool: True if the input is a single uppercase letter within the board's range, False otherwise.
    """
    return len(column_letter) == 1 and 'A' <= column_letter <= chr(ord('A') + NUM_COLS - 1)

def get_available_row(board, col_idx):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The 2D list representing the Connect 4 board.
        col_idx (int): The 0-based index of the column.

    Returns:
        int: The 0-based index of the lowest empty row, or -1 if the column is full.
    """
    # Iterate from the bottom row upwards
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            return row_idx
    return -1 # Column is full

def place_checker(board, col_idx, player_symbol):
    """
    Places a player's checker in the specified column.

    Args:
        board (list): The 2D list representing the Connect 4 board.
        col_idx (int): The 0-based index of the column.
        player_symbol (str): The symbol of the current player.

    Returns:
        tuple: (bool, int) - True if placement was successful, False otherwise.
               The integer is the row where the checker was placed, or -1 if not placed.
    """
    row_idx = get_available_row(board, col_idx)
    if row_idx != -1:
        board[row_idx][col_idx] = player_symbol
        return True, row_idx
    return False, -1

# --- Win Condition Functions ---

def check_win(board, player_symbol, last_row, last_col):
    """
    Checks if the current player has won after placing a checker at (last_row, last_col).

    Args:
        board (list): The 2D list representing the Connect 4 board.
        player_symbol (str): The symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check all possible winning directions: horizontal, vertical, and both diagonals.
    return (check_horizontal_win(board, player_symbol, last_row) or
            check_vertical_win(board, player_symbol, last_col) or
            check_diagonal_win(board, player_symbol, last_row, last_col))

def check_horizontal_win(board, player_symbol, row):
    """
    Checks for a horizontal win in the given row.

    Args:
        board (list): The 2D list representing the Connect 4 board.
        player_symbol (str): The symbol of the current player.
        row (int): The row index to check.

    Returns:
        bool: True if a horizontal win is found, False otherwise.
    """
    count = 0
    for col_idx in range(NUM_COLS):
        if board[row][col_idx] == player_symbol:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0 # Reset count if the sequence is broken
    return False

def check_vertical_win(board, player_symbol, col):
    """
    Checks for a vertical win in the given column.

    Args:
        board (list): The 2D list representing the Connect 4 board.
        player_symbol (str): The symbol of the current player.
        col (int): The column index to check.

    Returns:
        bool: True if a vertical win is found, False otherwise.
    """
    count = 0
    for row_idx in range(NUM_ROWS):
        if board[row_idx][col] == player_symbol:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0 # Reset count if the sequence is broken
    return False

def check_diagonal_win(board, player_symbol, last_row, last_col):
    """
    Checks for a diagonal win (both directions) passing through (last_row, last_col).

    Args:
        board (list): The 2D list representing the Connect 4 board.
        player_symbol (str): The symbol of the current player.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if a diagonal win is found, False otherwise.
    """
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start checking from 3 positions up and left from the last piece
    # until 3 positions down and right, ensuring within board bounds.
    for i in range(-3, 4):
        r, c = last_row + i, last_col + i
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            if board[r][c] == player_symbol:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        else:
            count = 0 # Reset if out of bounds

    # Reset count for the other diagonal
    count = 0
    # Check diagonal (top-right to bottom-left)
    # Start checking from 3 positions up and right from the last piece
    # until 3 positions down and left.
    for i in range(-3, 4):
        r, c = last_row + i, last_col - i
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            if board[r][c] == player_symbol:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        else:
            count = 0
    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the Connect 4 board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    # A board is full if there are no empty spaces in the top row.
    # More generally, iterate through all cells or check if any column is not full.
    for col_idx in range(NUM_COLS):
        if board[0][col_idx] == " ": # If the top row of any column has an empty space, it's not a draw
            return False
    return True

# --- Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, validates input, checks for wins/draws.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS] # Select symbols based on NUM_PLAYERS
    current_player_idx = random.randint(0, NUM_PLAYERS - 1) # Randomly choose first player

    game_over = False
    winner_symbol = None
    last_placed_row = -1
    last_placed_col = -1

    while not game_over:
        current_player_symbol = players[current_player_idx]
        print_board(board)

        # Prompt for player input
        print(f"Player {current_player_symbol}, please enter a column: ", end="")
        user_input = input().upper().strip() # Get input, convert to uppercase, remove whitespace

        # Input validation loop
        while not is_valid_column_input(user_input):
            print("Invalid column. Please enter a letter from "
                  f"A to {get_letter_from_column(NUM_COLS - 1)}: ", end="")
            user_input = input().upper().strip()

        col_index = get_column_from_letter(user_input)

        # Attempt to place the checker
        placed, last_placed_row = place_checker(board, col_index, current_player_symbol)

        if not placed:
            # If the column is full, the player loses their turn.
            # The assignment states "If the column is already completely filled with checkers,
            # the turn is invalid and the player loses the turn."
            # This means the current_player_idx should still advance.
            print_board(board) # Print board after invalid move
            print(f"Column {get_letter_from_column(col_index)} is full. Player {current_player_symbol} loses turn.")
            # Advance to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue # Continue to the next turn without checking for win/draw this turn
        else:
            # If checker was placed successfully, update last_placed_col
            last_placed_col = col_index


        # Check for win condition
        if check_win(board, current_player_symbol, last_placed_row, last_placed_col):
            winner_symbol = current_player_symbol
            game_over = True
        elif check_draw(board): # Check for draw only if no win
            game_over = True
        else:
            # If no win or draw, switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game over - print final board and result
    print_board(board)
    if winner_symbol:
        print(f"Player {winner_symbol} won!")
    else:
        print("It's a draw!")

# --- Main Execution ---

if __name__ == "__main__":
    play_game()
