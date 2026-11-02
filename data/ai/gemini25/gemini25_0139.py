import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board filled with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Clears the screen and prints the current state of the board.
    """
    os.system('clear')  # Clear screen for Linux/Unix
    
    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print()

    # Print board rows
    for r_idx, row in enumerate(board):
        # Print top border of the row
        print("+", end="")
        for _ in range(len(row)):
            print("---+", end="")
        print()

        # Print cells
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()

    # Print bottom border of the last row
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


def get_column_input(current_player_checker, max_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[max_cols - 1]:
                raise ValueError("Invalid column. Please enter a single letter corresponding to a column.")
            
            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r_idx in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[r_idx][col_index] == " ":
            board[r_idx][col_index] = player_checker
            return True, r_idx, col_index  # Return success and position
    return False, -1, -1  # Column is full


# --- Win Condition Functions ---

def check_win(board, last_row, last_col, player_checker):
    """
    Checks if the last placed checker resulted in a win (4 in a row).
    Checks horizontally, vertically, and both diagonals.
    """
    return (
        check_horizontal_win(board, last_row, last_col, player_checker) or
        check_vertical_win(board, last_row, last_col, player_checker) or
        check_diagonal_win_positive(board, last_row, last_col, player_checker) or
        check_diagonal_win_negative(board, last_row, last_col, player_checker)
    )

def check_horizontal_win(board, last_row, last_col, player_checker):
    """Checks for a horizontal win."""
    count = 0
    # Check to the left
    for c in range(max(0, last_col - (WIN_LENGTH - 1)), last_col + 1):
        if c < len(board[0]) and board[last_row][c] == player_checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_vertical_win(board, last_row, last_col, player_checker):
    """Checks for a vertical win."""
    count = 0
    # Check downwards only
    for r in range(last_row, min(len(board), last_row + WIN_LENGTH)):
        if board[r][last_col] == player_checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            # If a different checker is encountered, it's not a vertical line
            break
    return False

def check_diagonal_win_positive(board, last_row, last_col, player_checker):
    """Checks for a diagonal win (bottom-left to top-right)."""
    count = 0
    # Start from the bottom-leftmost possible position of a 4-in-a-row diagonal
    # that includes (last_row, last_col)
    start_row = last_row + min(last_col, WIN_LENGTH - 1)
    start_col = last_col - min(last_col, WIN_LENGTH - 1)

    while start_row >= 0 and start_col < len(board[0]):
        if start_row < len(board) and start_col >= 0 and board[start_row][start_col] == player_checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0 # Reset count if sequence is broken
        
        start_row -= 1
        start_col += 1
    return False


def check_diagonal_win_negative(board, last_row, last_col, player_checker):
    """Checks for a diagonal win (top-left to bottom-right)."""
    count = 0
    # Start from the top-leftmost possible position of a 4-in-a-row diagonal
    # that includes (last_row, last_col)
    start_row = last_row - min(last_row, WIN_LENGTH - 1)
    start_col = last_col - min(last_col, WIN_LENGTH - 1)
    
    while start_row < len(board) and start_col < len(board[0]):
        if start_row >= 0 and start_col >= 0 and board[start_row][start_col] == player_checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0 # Reset count if sequence is broken

        start_row += 1
        start_col += 1
    return False


def check_draw(board):
    """
    Checks if the board is completely filled (draw condition).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, not a draw
    return True  # No empty cells, it's a draw


# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26.")
        return
    if not (1 <= NUM_ROWS):
        print("Error: NUM_ROWS must be at least 1.")
        return

    # Initialize players and their checkers
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Create the board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = players[current_player_index]
        
        print_board(board)
        
        col_index = get_column_input(current_player_checker, NUM_COLS)
        
        # Drop checker and validate column
        success, last_row, last_col = drop_checker(board, col_index, current_player_checker)

        if not success:
            print("Column is full! You lose your turn.")
            # Player loses turn if column is full
        else:
            # Check for win
            if check_win(board, last_row, last_col, current_player_checker):
                winner_checker = current_player_checker
                game_over = True
            # Check for draw
            elif check_draw(board):
                game_over = True
            
            # Switch to next player if game is not over
            if not game_over:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over, print final board and result
    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    play_game()
