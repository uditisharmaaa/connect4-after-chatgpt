import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players (up to 5 players)
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Functions ---

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
    Clears the screen and prints the current state of the board.
    Columns are labeled with letters (A, B, C...).
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels
    sys.stdout.write("  ")
    for col_index in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + col_index)} ")
    sys.stdout.write("\n")

    # Print board rows and separators
    for row_index in range(len(board)):
        sys.stdout.write("+")
        sys.stdout.write("---+")
        sys.stdout.write("---+" * (len(board[0]) - 1))
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for col_index in range(len(board[0])):
            sys.stdout.write(f" {board[row_index][col_index]} |")
        sys.stdout.write("\n")

    # Print the bottom separator
    sys.stdout.write("+")
    sys.stdout.write("---+")
    sys.stdout.write("---+" * (len(board[0]) - 1))
    sys.stdout.write("\n")

def is_valid_column_input(col_input, num_cols):
    """
    Checks if the user's column input is valid.
    It must be a single uppercase letter within the board's range.
    """
    if len(col_input) != 1:
        return False
    if not 'A' <= col_input <= chr(ord('A') + num_cols - 1):
        return False
    return True

def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A') to its integer index (e.g., 0).
    """
    return ord(col_char) - ord('A')

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index, col_index
    return False, -1, -1 # Column is full

def is_board_full(board):
    """
    Checks if the entire board is filled, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False
    return True

# --- Win Condition Functions ---

def check_win(board, row, col, checker):
    """
    Checks if the last placed checker at (row, col) results in a win.
    Checks horizontally, vertically, and both diagonals.
    """
    return (check_horizontal_win(board, row, col, checker) or
            check_vertical_win(board, row, col, checker) or
            check_diagonal_win(board, row, col, checker))

def check_horizontal_win(board, row, col, checker):
    """ Checks for 4 in a row horizontally. """
    count = 0
    # Check to the left
    for c in range(col, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    # Check to the right (starting from col + 1 to avoid double counting the placed checker)
    for c in range(col + 1, len(board[0])):
        if board[row][c] == checker:
            count += 1
        else:
            break
    return count >= WIN_CONDITION

def check_vertical_win(board, row, col, checker):
    """ Checks for 4 in a row vertically. """
    count = 0
    # Check downwards
    for r in range(row, len(board)):
        if board[r][col] == checker:
            count += 1
        else:
            break
    # No need to check upwards as checkers only fall down
    return count >= WIN_CONDITION

def check_diagonal_win(board, row, col, checker):
    """ Checks for 4 in a row in both diagonal directions. """
    return check_pos_diagonal_win(board, row, col, checker) or \
           check_neg_diagonal_win(board, row, col, checker)

def check_pos_diagonal_win(board, row, col, checker):
    """ Checks for 4 in a row on positive slope diagonals (bottom-left to top-right). """
    count = 0
    # Move to the start of the current diagonal (bottom-left most cell)
    temp_row, temp_col = row, col
    while temp_row < len(board) - 1 and temp_col > 0:
        temp_row += 1
        temp_col -= 1

    # Check along the diagonal from bottom-left to top-right
    while temp_row >= 0 and temp_col < len(board[0]):
        if board[temp_row][temp_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        temp_row -= 1
        temp_col += 1
    return False

def check_neg_diagonal_win(board, row, col, checker):
    """ Checks for 4 in a row on negative slope diagonals (top-left to bottom-right). """
    count = 0
    # Move to the start of the current diagonal (top-left most cell)
    temp_row, temp_col = row, col
    while temp_row > 0 and temp_col > 0:
        temp_row -= 1
        temp_col -= 1

    # Check along the diagonal from top-left to bottom-right
    while temp_row < len(board) and temp_col < len(board[0]):
        if board[temp_row][temp_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        temp_row += 1
        temp_col += 1
    return False


# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS] # Select checkers based on NUM_PLAYERS
    current_player_index = random.randint(0, NUM_PLAYERS - 1) # Randomly choose first player

    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = players[current_player_index]
        print_board(board)
        sys.stdout.write(f"Player {current_checker}, please enter a column: ")

        player_input = input().upper().strip()

        # Validate input
        if not is_valid_column_input(player_input, NUM_COLS):
            sys.stdout.write("Invalid input. Please enter a single uppercase letter (e.g., A, B).\n")
            continue

        col_index = get_column_index(player_input)

        # Drop checker
        success, placed_row, placed_col = drop_checker(board, col_index, current_checker)

        if not success:
            sys.stdout.write("That column is full. Please choose another column.\n")
            # Player does not lose turn if column is full
            continue

        # Check for win
        if check_win(board, placed_row, placed_col, current_checker):
            print_board(board)
            winner_checker = current_checker
            game_over = True
        elif is_board_full(board):
            print_board(board)
            game_over = True # It's a draw
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End game message
    if winner_checker:
        sys.stdout.write(f"Player {winner_checker} won!\n")
    else:
        sys.stdout.write("The game is a draw!\n")

if __name__ == "__main__":
    main()
