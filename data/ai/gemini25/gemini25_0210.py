import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for 'A' to 'Z')
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates a 2D list representing the Connect 4 board, initialized with spaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end=" ")
    print()

    # Print the board rows
    for row_index in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()

    # Print the bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def get_column_input(player_checker, board_cols):
    """
    Prompts the current player to enter a column and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.
        board_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= chr(ord('A') + board_cols - 1):
                raise ValueError("Invalid column. Please enter a single letter corresponding to a column.")

            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except EOFError:  # Handle Ctrl+D or end-of-file for robust input
            print("\nExiting game. Goodbye!")
            exit()


def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):  # Iterate from bottom row upwards
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal wins
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for r in range(rows - win_condition + 1):
        for c in range(cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full (draw), False otherwise.
    """
    for row in board:
        if " " in row:
            return False  # An empty space found, not a draw
    return True  # No empty spaces, it's a draw

def main():
    """Main function to run the Connect 4 game."""

    # 1. Initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        # 2. Game phase: Player's turn
        col_to_drop = -1
        input_valid = False
        while not input_valid:
            col_to_drop = get_column_input(current_player_checker, NUM_COLS)

            # Validate if column is full
            if board[0][col_to_drop] != " ": # Check the top-most row
                print(f"Column {chr(ord('A') + col_to_drop)} is full. Please choose another column.")
            else:
                input_valid = True

        # Place the checker
        drop_checker(board, col_to_drop, current_player_checker)

        # After every turn, print the board
        print_board(board)

        # Check for a win
        if check_win(board, current_player_checker, WIN_CONDITION):
            winner = current_player_checker
            game_over = True
        # Check for a draw (only if no one won)
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    print_board(board) # Print final board one last time
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    main()
