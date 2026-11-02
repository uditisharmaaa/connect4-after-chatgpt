import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
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
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)]))

    # Print the board
    for r in range(len(board)):
        print("+" + "---+" * num_cols)
        print("| " + " | ".join(board[r]) + " |")
    print("+" + "---+" * num_cols)

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.

    Args:
        column_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The integer index of the column, or None if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return None
    
    col_index = ord(column_char.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return None

def is_valid_move(board, col_index):
    """
    Checks if a move to a given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The integer index of the chosen column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if col_index is None:
        return False
    
    if not (0 <= col_index < len(board[0])):
        return False

    # Check if the top row of the column is empty
    return board[0][col_index] == ' '

def drop_checker(board, col_index, player_token):
    """
    Drops a player's checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The integer index of the chosen column.
        player_token (str): The token of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = player_token
            return True
    return False # Column is full, though this should ideally be caught by is_valid_move

def check_win(board, player_token, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_token (str): The token of the current player.
        win_condition (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_token for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_token for i in range(win_condition)):
                return True

    # Check diagonally (positive slope)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_token for i in range(win_condition)):
                return True

    # Check diagonally (negative slope)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_token for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_cols = len(board[0])
    for c in range(num_cols):
        if board[0][c] == ' ':  # If any space in the top row is empty, board is not full
            return False
    return True

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_PLAYERS > len(PLAYER_TOKENS) or NUM_PLAYERS < 2:
        print(f"Error: NUM_PLAYERS must be between 2 and {len(PLAYER_TOKENS)}.")
        sys.exit(1)
    if NUM_COLS > 26 or NUM_COLS < WIN_CONDITION:
        print(f"Error: NUM_COLS must be between {WIN_CONDITION} and 26.")
        sys.exit(1)
    if NUM_ROWS < WIN_CONDITION:
        print(f"Error: NUM_ROWS must be at least {WIN_CONDITION}.")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False

    while not game_over:
        current_player_token = players[current_player_index]
        print_board(board)

        valid_input = False
        col_char = ''
        col_index = None

        while not valid_input:
            col_char = input(f"Player {current_player_token}, please enter a column: ").strip().upper()
            
            if len(col_char) != 1:
                print("Invalid input: Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = get_column_index(col_char, NUM_COLS)

            if col_index is None:
                print(f"Invalid column: '{col_char}' is not a valid column letter for this board size.")
            elif not is_valid_move(board, col_index):
                print(f"Column {col_char} is full. Please choose another column.")
            else:
                valid_input = True
        
        # Drop the checker (should always succeed at this point due to validation)
        drop_checker(board, col_index, current_player_token)

        # Check for win
        if check_win(board, current_player_token, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_token} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    main()
