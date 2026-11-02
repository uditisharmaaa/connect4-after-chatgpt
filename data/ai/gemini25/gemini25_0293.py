import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Utility Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_column_label(col_index):
    """Converts a column index to its corresponding letter label."""
    return chr(ord('A') + col_index)


def get_column_index(col_label):
    """Converts a column letter label to its corresponding index."""
    return ord(col_label.upper()) - ord('A')


def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the Connect 4 board to the console."""
    clear_screen()
    num_cols = len(board[0])

    # Print column labels
    print("  " + "   ".join([get_column_label(i) for i in range(num_cols)]))

    # Print board content
    for r in range(len(board)):
        print("+" + "---+" * num_cols)
        print("| " + " | ".join(board[r]) + " |")
    print("+" + "---+" * num_cols)


def is_valid_column_input(col_input, num_cols):
    """Checks if the user's column input is valid."""
    if not (isinstance(col_input, str) and len(col_input) == 1 and col_input.isalpha()):
        return False, "Invalid input. Please enter a single letter (e.g., A, B)."
    
    col_index = get_column_index(col_input)
    if not (0 <= col_index < num_cols):
        return False, f"Column '{col_input.upper()}' is out of board range (A-{get_column_label(num_cols - 1)})."
    
    return True, ""


def drop_checker(board, col_index, player_token):
    """
    Drops a checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_token
            return True
    return False


def check_win(board, player_token, win_condition):
    """Checks if the given player has won the game."""
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_token for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_token for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_token for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_token for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """Checks if the board is full, indicating a draw."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True


# --- Main Game Logic ---
def play_connect_4():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        player_token = PLAYER_TOKENS[current_player_index]
        print_board(board)
        print(f"Player {player_token}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            is_valid, error_msg = is_valid_column_input(user_input, NUM_COLS)
            if not is_valid:
                print(error_msg)
                print(f"Player {player_token}, please enter a column:")
                continue

            col_index = get_column_index(user_input)
            
            if drop_checker(board, col_index, player_token):
                break  # Valid move, break inner loop
            else:
                print(f"Column {user_input} is full. Please choose another column.")
                print(f"Player {player_token}, please enter a column:")
                # Player does not lose turn for a full column (as per clarification implicitly)

        if check_win(board, player_token, WIN_CONDITION):
            print_board(board)
            print(f"Player {player_token} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_connect_4()
