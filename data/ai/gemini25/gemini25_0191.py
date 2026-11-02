import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_LENGTH = 4

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"  {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board content
    for r_idx, row in enumerate(board):
        print("+---+" * len(row) + "+")
        print("|", end="")
        for c_idx, cell in enumerate(row):
            print(f" {cell} |", end="")
        print()
    print("+---+" * len(board[0]) + "+")

def get_column_from_input(prompt, num_cols):
    """
    Prompts the player for a column input and validates it.

    Args:
        prompt (str): The message to display to the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + num_cols - 1):
            return ord(user_input) - ord('A')
        else:
            print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}.")

def place_checker(board, col, checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column number.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check positive slope diagonal (bottom-left to top-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check negative slope diagonal (top-left to bottom-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
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
    for row in board:
        if " " in row:
            return False
    return True

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = list(range(NUM_PLAYERS)) # Player indices: 0, 1, 2, ...
    checkers = CHECKERS

    current_player_idx = random.choice(players) # Randomly select first player
    print_board(board)
    print(f"Player {checkers[current_player_idx]} goes first!")
    input("Press Enter to start...")

    game_over = False
    while not game_over:
        current_checker = checkers[current_player_idx]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_placement = False
        while not valid_placement:
            col_input = get_column_from_input(f"Player {current_checker}'s turn: ", NUM_COLS)
            if place_checker(board, col_input, current_checker):
                valid_placement = True
            else:
                print("Column is full! Please choose another column.")

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame aborted by user.")
    sys.exit(0)
