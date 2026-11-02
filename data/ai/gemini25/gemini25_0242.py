import os
import random
import sys

# --- Global Constants ---
# Board dimensions (can be changed, max 26 columns)
NUM_ROWS = 6
NUM_COLS = 7

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
CONNECT_N = 4

# --- Functions ---

def clear_screen():
    """
    Clears the terminal screen. Works on Linux/Unix systems.
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.

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
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(num_cols):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

    # Print rows with checkers and separators
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()

def get_player_input(player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker of the current player.
        board_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            prompt_message = f"Player {player_checker}, please enter a column: "
            col_input = input(prompt_message).upper()

            if not col_input.isalpha() or len(col_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_input) - ord('A')

            if 0 <= col_index < board_cols:
                return col_index
            else:
                print(f"Column '{col_input}' is out of board range (A-{chr(ord('A') + board_cols - 1)}). Please try again.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for row_index in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker):
    """
    Checks if the given player has won the game by getting CONNECT_N checkers
    in a row horizontally, vertically, or diagonally.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a specific direction
    def check_direction(r, c, dr, dc):
        count = 0
        for i in range(CONNECT_N):
            curr_r, curr_c = r + i * dr, c + i * dc
            if 0 <= curr_r < num_rows and 0 <= curr_c < num_cols and board[curr_r][curr_c] == player_checker:
                count += 1
            else:
                break
        return count == CONNECT_N

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - (CONNECT_N - 1)):
            if check_direction(r, c, 0, 1):
                return True

    # Check vertical
    for r in range(num_rows - (CONNECT_N - 1)):
        for c in range(num_cols):
            if check_direction(r, c, 1, 0):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - (CONNECT_N - 1)):
        for c in range(num_cols - (CONNECT_N - 1)):
            if check_direction(r, c, 1, 1):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(num_rows - (CONNECT_N - 1)):
        for c in range(CONNECT_N - 1, num_cols):
            if check_direction(r, c, 1, -1):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = NUM_PLAYERS
    player_checkers = CHECKERS

    # Randomly select the first player
    current_player_idx = random.randint(0, num_players - 1)

    game_over = False
    winner = None

    while not game_over:
        current_checker = player_checkers[current_player_idx]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_index = get_player_input(current_checker, NUM_COLS)

            if drop_checker(board, col_index, current_checker):
                valid_turn = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # Player does not lose turn for a full column, they are asked again

        # After placing the checker, check for win or draw
        if check_win(board, current_checker):
            print_board(board)
            winner = current_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % num_players

    # Game end messages
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

    print("\nThanks for playing Connect 4!")

if __name__ == "__main__":
    main()
