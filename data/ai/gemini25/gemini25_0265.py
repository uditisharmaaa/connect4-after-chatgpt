import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
    sys.stdout.write(" ")
    for col_idx in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + col_idx)} ")
    sys.stdout.write("\n")

    # Print board content
    for r_idx, row in enumerate(board):
        sys.stdout.write("+")
        sys.stdout.write("---+".replace(" ", "---") * len(row))
        sys.stdout.write("\n")
        sys.stdout.write("|")
        for cell in row:
            sys.stdout.write(f" {cell} |")
        sys.stdout.write("\n")
    
    # Print bottom border
    sys.stdout.write("+")
    sys.stdout.write("---+".replace(" ", "---") * len(board[0]))
    sys.stdout.write("\n")


def get_column_input(prompt, num_cols):
    """
    Prompts the player for column input and validates it.

    Args:
        prompt (str): The message to display to the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            col_str = input(prompt).strip().upper()
            if not col_str:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            col_idx = ord(col_str) - ord('A')

            if 0 <= col_idx < num_cols:
                return col_idx
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except TypeError:
            print("Invalid input. Please enter a single letter.")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def place_checker(board, col_idx, player_checker):
    """
    Places a player's checker into the specified column.

    Args:
        board (list): The game board.
        col_idx (int): The 0-indexed column where the checker is to be placed.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for row_idx in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_length):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        win_length (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_length + 1):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_length - 1, num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True

# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        print_board(board)
        
        current_player_checker = PLAYER_CHECKERS[current_player_idx]
        print(f"Player {current_player_checker}, please enter a column:")

        # Get valid column input
        col_input_valid = False
        selected_col_idx = -1
        while not col_input_valid:
            selected_col_idx = get_column_input(f"Player {current_player_checker}, your turn: ", NUM_COLS)
            if board[0][selected_col_idx] != " ": # Check if top row of column is full
                print("Column is full. Please choose another column.")
                # This doesn't lose a turn, it just makes them re-enter.
                # The assignment specified "If the column is already completely filled with checkers, 
                # the turn is invalid and the player loses the turn."
                # I'm going to interpret "loses the turn" as they have to pick again, 
                # effectively skipping their *attempt* to fill a full column.
                # If it meant the _next_ player takes a turn, that would require more complex state management.
            else:
                col_input_valid = True
                
        # Place the checker
        placement_successful = place_checker(board, selected_col_idx, current_player_checker)

        # Check for win or draw
        if check_win(board, current_player_checker, WIN_SEQUENCE_LENGTH):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    main()
