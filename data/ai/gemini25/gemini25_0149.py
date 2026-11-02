import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
        list[list[str]]: A 2D list representing the board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list[list[str]]): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)]))

    # Print top border
    print("+" + "---+".join(["" for _ in range(num_cols)]) + "+")

    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+".join(["" for _ in range(num_cols)]) + "+")

def get_valid_column_input(player_token, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_token (str): The current player's token.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed integer representation of the valid column chosen.
    """
    while True:
        try:
            col_char = input(f"Player {player_token}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, player_token):
    """
    Drops a checker into the specified column.

    Args:
        board (list[list[str]]): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_token (str): The token of the current player.

    Returns:
        tuple[bool, int, int]: A tuple containing:
            - bool: True if the checker was successfully placed, False if the column is full.
            - int: The row index where the checker was placed (-1 if column full).
            - int: The column index where the checker was placed (-1 if column full).
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_token
            return True, r, col_index
    return False, -1, -1

def check_win(board, row, col, player_token):
    """
    Checks if the last placed checker at (row, col) results in a win.

    Args:
        board (list[list[str]]): The game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        player_token (str): The token of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    def check_direction(dr, dc):
        count = 0
        # Check in one direction
        r, c = row, col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc

        # Check in the opposite direction
        r, c = row - dr, col - dc # Start from the cell next to the original (row,col)
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        return count >= WIN_CONDITION

    # Check horizontal
    if check_direction(0, 1):
        return True
    # Check vertical
    if check_direction(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True
    # Check diagonal (top-right to bottom-left)
    if check_direction(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list[list[str]]): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_game():
    """Manages the main Connect 4 game flow."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_token = None

    while not game_over:
        current_player_token = PLAYER_TOKENS[current_player_index]
        print_board(board)

        col_index = get_valid_column_input(current_player_token, NUM_COLS)
        
        placed, row, col = drop_checker(board, col_index, current_player_token)

        if not placed:
            print("Column is full! Please choose another column.")
            # Player does not lose turn, loop continues for the same player
            continue
        
        # Check for win
        if check_win(board, row, col, current_player_token):
            winner_token = current_player_token
            game_over = True
            
        # Check for draw if no win
        elif check_draw(board):
            game_over = True
        
        # Switch to next player if game not over
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End game
    print_board(board) # Print final board
    if winner_token:
        print(f"Player {winner_token} won!")
    else:
        print("The game is a draw!")

# --- Entry Point ---

if __name__ == "__main__":
    play_game()
