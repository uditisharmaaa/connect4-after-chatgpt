import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.
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

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print the board content
    for r in range(len(board)):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.
    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(col_char) - ord('A')
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please choose a column between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("Invalid input. Please enter a single letter.")

def place_checker(board, col, player_checker):
    """
    Places the player's checker in the lowest available space of the given column.
    Args:
        board (list): The game board.
        col (int): The 0-indexed column where the checker is to be placed.
        player_checker (str): The checker symbol of the current player.
    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False

def check_win(board, player_checker, num_to_win=4):
    """
    Checks if the current player has won the game.
    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        num_to_win (int): The number of checkers in a row required to win.
    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - num_to_win + 1):
            if all(board[r][c + i] == player_checker for i in range(num_to_win)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - num_to_win + 1):
            if all(board[r + i][c] == player_checker for i in range(num_to_win)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - num_to_win + 1):
        for c in range(num_cols - num_to_win + 1):
            if all(board[r + i][c + i] == player_checker for i in range(num_to_win)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(num_to_win - 1, num_rows):
        for c in range(num_cols - num_to_win + 1):
            if all(board[r - i][c + i] == player_checker for i in range(num_to_win)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (a draw).
    Args:
        board (list): The game board.
    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True # No empty spaces found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = NUM_PLAYERS
    player_checkers = PLAYER_CHECKERS

    current_player_index = random.randint(0, num_players - 1)

    game_over = False
    winner = None

    while not game_over:
        current_player_checker = player_checkers[current_player_index]
        print_board(board)

        while True:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            if place_checker(board, col_index, current_player_checker):
                break
            else:
                print("Column is full! Please choose another column.")

        print_board(board) # Print board after placing checker

        if check_win(board, current_player_checker):
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
            print("The board is full! It's a draw!")
        else:
            current_player_index = (current_player_index + 1) % num_players

    if winner:
        print(f"Player {winner} won!")
    print("\nGame Over! Thanks for playing!")

if __name__ == "__main__":
    main()
