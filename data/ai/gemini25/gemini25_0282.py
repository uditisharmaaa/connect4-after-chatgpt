import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for 'A' to 'Z' labeling)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
WIN_CONDITION = 4  # Number of checkers in a row needed to win

# Player checkers, ordered for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the Connect 4 board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the Connect 4 board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f"   {chr(ord('A') + col_idx)}", end="")
    print("\n+---+", end="")
    print("---+" * (len(board[0]) - 1))

    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n+---+", end="")
        print("---+" * (len(board[0]) - 1))

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding 0-based index.

    Args:
        column_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= chr(ord('A') + NUM_COLS - 1):
        return ord(column_char) - ord('A')
    return -1

def get_player_input(player_checker, board):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol for the current player.
        board (list): The 2D list representing the Connect 4 board.

    Returns:
        int: The 0-based index of the valid column chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").upper()
        col_index = get_column_index(col_input)

        if col_index == -1:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        elif board[0][col_index] != " ":  # Check if the top row of the column is occupied
            print("That column is full. Please choose another column.")
        else:
            return col_index

def drop_checker(board, col_index, checker):
    """
    Places the player's checker into the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the Connect 4 board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol of the current player.

    Returns:
        tuple: A tuple (row_index, col_index) of where the checker was placed,
               or (-1, -1) if the column was full (though this should be prevented by validation).
    """
    num_rows = len(board)
    for row_idx in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = checker
            return row_idx, col_index
    return -1, -1  # Should not be reached if input is validated correctly

def check_win(board, last_placed_row, last_placed_col, checker):
    """
    Checks if the last placed checker resulted in a win (4 in a row horizontally,
    vertically, or diagonally).

    Args:
        board (list): The 2D list representing the Connect 4 board.
        last_placed_row (int): The row index where the last checker was placed.
        last_placed_col (int): The column index where the last checker was placed.
        checker (str): The checker symbol of the player who just moved.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a specific direction
    def check_direction(dr, dc):
        count = 0
        # Check forward direction
        for i in range(WIN_CONDITION):
            r, c = last_placed_row + i * dr, last_placed_col + i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
            else:
                break
        # Check backward direction (excluding the already counted last_placed_checker)
        for i in range(1, WIN_CONDITION):
            r, c = last_placed_row - i * dr, last_placed_col - i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
            else:
                break
        return count >= WIN_CONDITION

    # Check horizontal win
    if check_direction(0, 1): return True
    # Check vertical win
    if check_direction(1, 0): return True
    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1): return True
    # Check diagonal (top-right to bottom-left)
    if check_direction(1, -1): return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the Connect 4 board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for col_idx in range(len(board[0])):
        if board[0][col_idx] == " ":  # If any cell in the top row is empty, board is not full
            return False
    return True

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles player turns, checks for wins/draws.
    """
    # Initialize game
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS] # Select checkers based on NUM_PLAYERS
    current_player_idx = random.randint(0, NUM_PLAYERS - 1) # Randomly choose first player

    game_over = False
    winner_checker = None

    print_board(board) # Initial board print

    # Game loop
    while not game_over:
        current_checker = players[current_player_idx]

        # Get and validate player input
        col_choice_index = get_player_input(current_checker, board)

        # Place checker
        last_row, last_col = drop_checker(board, col_choice_index, current_checker)

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, last_row, last_col, current_checker):
            winner_checker = current_checker
            game_over = True
        # Check for draw
        elif check_draw(board):
            game_over = True
            print("It's a draw!")
        else:
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # End of game
    if winner_checker:
        print(f"Player {winner_checker} won!")
    print("Game Over!")

if __name__ == "__main__":
    play_connect_4()
