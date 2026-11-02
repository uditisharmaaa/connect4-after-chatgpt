import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# Ensure NUM_COLS is not greater than 26 for column labels
if NUM_COLS > 26:
    sys.exit("Error: NUM_COLS cannot be greater than 26 for column labeling.")
if NUM_PLAYERS > len(CHECKERS):
    sys.exit(f"Error: NUM_PLAYERS cannot exceed {len(CHECKERS)}.")

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # 'cls' for Windows, 'clear' for Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows in the board.
        cols (int): The number of columns in the board.

    Returns:
        list: A 2D list representing the board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current state of the board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"  {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+---+", end="")
        for _ in range(len(board[0]) - 1):
            print("---+", end="")
        print("---+" if len(board[0]) == 1 else "") # For a single column board edge case

        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()

    # Print bottom border
    print("+---+", end="")
    for _ in range(len(board[0]) - 1):
        print("---+", end="")
    print("---+" if len(board[0]) == 1 else "")
    print()

def get_player_input(current_player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board (list): The current state of the board.

    Returns:
        int: The 0-based index of the chosen valid column.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Invalid input: Please enter a column letter (e.g., A).")
                continue

            col_char = user_input[0]

            if not ('A' <= col_char <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid input: Column '{col_char}' is out of board range (A-{chr(ord('A') + num_cols - 1)}).")
                continue

            col_index = ord(col_char) - ord('A')

            if board[0][col_index] != " ":
                print(f"Invalid move: Column {col_char} is full. Please choose another column.")
                continue

            return col_index

        except IndexError:
            print("Invalid input: Please enter a single column letter (e.g., A).")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space of the specified column.

    Args:
        board (list): The current state of the board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (row_placed, col_placed) if successful, otherwise (None, None).
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return None, None  # Column is full (should be caught by input validation)

def check_win(board, checker, last_move_row, last_move_col):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The current state of the board.
        checker (str): The checker symbol of the player who just moved.
        last_move_row (int): The row index where the last checker was placed.
        last_move_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a given direction
    def count_consecutive(row, col, d_row, d_col):
        count = 0
        r, c = row, col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += d_row
            c += d_col
        return count

    # Check horizontal
    count = count_consecutive(last_move_row, last_move_col, 0, 1) + count_consecutive(last_move_row, last_move_col, 0, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check vertical
    count = count_consecutive(last_move_row, last_move_col, 1, 0) + count_consecutive(last_move_row, last_move_col, -1, 0) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonal (top-left to bottom-right)
    count = count_consecutive(last_move_row, last_move_col, 1, 1) + count_consecutive(last_move_row, last_move_col, -1, -1) - 1
    if count >= WIN_CONDITION:
        return True

    # Check diagonal (top-right to bottom-left)
    count = count_consecutive(last_move_row, last_move_col, 1, -1) + count_consecutive(last_move_row, last_move_col, -1, 1) - 1
    if count >= WIN_CONDITION:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The current state of the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        print(f"Current Turn: Player {current_player_checker}")

        col_to_place = get_player_input(current_player_checker, board)
        last_move_row, last_move_col = drop_checker(board, col_to_place, current_player_checker)

        # Re-print board after a valid move
        print_board(board)

        if check_win(board, current_player_checker, last_move_row, last_move_col):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    main()
