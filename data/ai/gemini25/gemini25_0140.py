import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels (A, B, C, ...) and separators.
    """
    os.system('clear')  # Clear the screen

    num_cols = len(board[0])
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    col_labels = [string.ascii_uppercase[i] for i in range(num_cols)]
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            if col_char not in col_labels:
                print(f"Invalid column. Please enter a letter from A to {col_labels[-1]}.")
                continue

            col_index = ord(col_char) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.
    Returns True if successful, False if the column is full.
    Modifies the board in place.
    """
    num_rows = len(board)
    # Iterate from the bottom up to find the lowest available space
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r, col_index  # Return success and position
    return False, -1, -1  # Column is full

def check_win(board, last_row, last_col, checker):
    """
    Checks if the last placed checker resulted in a win (4 in a row).
    Checks horizontally, vertically, and both diagonals.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers
    def count_consecutive(delta_row, delta_col):
        count = 0
        for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
            r, c = last_row + i * delta_row, last_col + i * delta_col
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0  # Reset count if consecutive checkers are broken
        return False

    # Check horizontal
    if count_consecutive(0, 1):
        return True
    # Check vertical
    if count_consecutive(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1):
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if count_consecutive(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, it's your turn.")

        col_index = get_player_input(current_player_checker, NUM_COLS)

        success, last_placed_row, last_placed_col = drop_checker(board, col_index, current_player_checker)

        if not success:
            print("That column is full! Please choose another column.")
            # Player does not lose turn, will be prompted again in next loop iteration
            continue

        # Check for win after every valid move
        if check_win(board, last_placed_row, last_placed_col, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
