import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
    Prints the current state of the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    cols = len(board[0])
    rows = len(board)

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(cols)]))

    # Print board rows
    for r in range(rows):
        print("+---" * cols + "+")
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * cols + "+")

def get_player_input(current_player_idx, players_checkers, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_idx (int): The index of the current player.
        players_checkers (list): A list of checker symbols for each player.
        board (list): The current game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    cols = len(board[0])
    player_checker = players_checkers[current_player_idx]
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            col_input = input(prompt).strip().upper()

            if not col_input:
                print("Invalid input: Column cannot be empty. Please try again.")
                continue

            # Check if input is a single letter
            if len(col_input) != 1 or not 'A' <= col_input[0] <= chr(ord('A') + cols - 1):
                print(f"Invalid input: Please enter a single letter from A to {chr(ord('A') + cols - 1)}. Please try again.")
                continue

            col = ord(col_input[0]) - ord('A')

            # Check if column is full
            if board[0][col] != " ":
                print("Invalid move: This column is full. Please choose another column.")
                continue

            return col
        except ValueError:
            print("Invalid input: Please enter a single letter corresponding to a column. Please try again.")
        except IndexError:
            print("Invalid input: Column out of range. Please try again.")

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol ("X", "O", etc.).

    Returns:
        tuple: (row, col) where the checker was placed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column is full (should be caught by validation earlier, but good for safety)

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    def check_direction(dr, dc):
        """Helper to check a specific direction."""
        count = 1
        # Check forward direction
        for i in range(1, WIN_LENGTH):
            r, c = last_row + dr * i, last_col + dc * i
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
                count += 1
            else:
                break
        # Check backward direction
        for i in range(1, WIN_LENGTH):
            r, c = last_row - dr * i, last_col - dc * i
            if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
                count += 1
            else:
                break
        return count >= WIN_LENGTH

    # Check horizontal
    if check_direction(0, 1):
        return True
    # Check vertical
    if check_direction(1, 0):
        return True
    # Check diagonal (positive slope: /)
    if check_direction(1, 1):
        return True
    # Check diagonal (negative slope: \)
    if check_direction(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    cols = len(board[0])
    for c in range(cols):
        if board[0][c] == " ":  # If the top row of any column is empty, not a draw
            return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Manages the main Connect 4 game flow.
    """
    clear_screen()
    board = create_board(NUM_ROWS, NUM_COLS)
    players_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print("Welcome to Connect 4!")
    print(f"Number of players: {NUM_PLAYERS}")
    print(f"Board dimensions: {NUM_ROWS} rows x {NUM_COLS} columns")
    print(f"Checkers: {', '.join(players_checkers)}")
    print(f"Player {players_checkers[current_player_idx]} goes first!\n")

    input("Press Enter to start the game...")

    game_over = False
    winner_checker = None

    while not game_over:
        clear_screen()
        print_board(board)
        current_checker = players_checkers[current_player_idx]

        col = get_player_input(current_player_idx, players_checkers, board)

        last_pos = drop_checker(board, col, current_checker)
        if last_pos is None: # This should ideally not happen due to get_player_input validation
            print("Error: Column was unexpectedly full. Skipping turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        
        last_row, last_col = last_pos

        if check_win(board, current_checker, last_row, last_col):
            clear_screen()
            print_board(board)
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            clear_screen()
            print_board(board)
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game End
    print("\n--- GAME OVER ---")
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")
    print("Thanks for playing!")

if __name__ == "__main__":
    play_game()
