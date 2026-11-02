import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checker symbols for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


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
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for col_index in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + col_index)} ")
    sys.stdout.write("\n")

    # Print board content
    for r in range(len(board)):
        sys.stdout.write("+")
        for _ in range(len(board[0])):
            sys.stdout.write("---+")
        sys.stdout.write("\n")
        sys.stdout.write("|")
        for c in range(len(board[0])):
            sys.stdout.write(f" {board[r][c]} |")
        sys.stdout.write("\n")

    sys.stdout.write("+")
    for _ in range(len(board[0])):
        sys.stdout.write("---+")
    sys.stdout.write("\n")


def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its corresponding integer index.

    Args:
        column_char (str): The character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The integer index of the column, or -1 if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return -1
    
    char_code = ord(column_char.upper())
    
    if ord('A') <= char_code < ord('A') + num_cols:
        return char_code - ord('A')
    else:
        return -1


def drop_checker(board, col_index, player_symbol):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The index of the column to drop the checker into.
        player_symbol (str): The symbol of the current player's checker.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_symbol
            return True
    return False  # Column is full


def check_win(board, player_symbol):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_symbol (str): The symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_symbol for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols):
            if all(board[r + i][c] == player_symbol for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_symbol for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_symbol for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """
    Checks if the game is a draw (board is full).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False

    while not game_over:
        current_player_symbol = PLAYER_SYMBOLS[current_player_index]
        print_board(board)
        
        print(f"Player {current_player_symbol}, please enter a column:")

        valid_input = False
        col_to_drop = -1

        while not valid_input:
            user_input = input().strip().upper()

            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., A).")
                continue
            
            col_to_drop = get_column_index(user_input, NUM_COLS)

            if col_to_drop == -1:
                print(f"Invalid column '{user_input}'. Please enter a letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
            elif not drop_checker(board, col_to_drop, current_player_symbol):
                print(f"Column {user_input} is full. Please choose another column.")
            else:
                valid_input = True
        
        # After a valid move, check for win or draw
        if check_win(board, current_player_symbol):
            print_board(board)
            print(f"Player {current_player_symbol} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
