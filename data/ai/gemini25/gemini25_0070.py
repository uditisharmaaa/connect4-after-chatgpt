import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers, chosen in order
CHECKERS = ["X", "O", "V", "H", "M"]


# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates a new game board initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def get_column_label(col_index):
    """
    Converts a column index (0-based) to its corresponding uppercase letter label.
    Assumes max 26 columns (A-Z).
    """
    return chr(ord('A') + col_index)

def print_board(board):
    """
    Clears the screen and prints the current state of the board.
    """
    os.system('clear')

    # Print column labels
    col_labels = "  " + "   ".join([get_column_label(i) for i in range(len(board[0]))])
    print(col_labels)

    # Print board
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")


# --- Game Logic ---

def get_player_input(current_player_checker, board):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-based column index if valid, otherwise keeps prompting.
    """
    num_cols = len(board[0])
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if len(user_input) != 1 or not 'A' <= user_input <= get_column_label(num_cols - 1):
                print(f"Invalid input. Please enter a single letter from A to {get_column_label(num_cols - 1)}.")
                continue

            col_index = ord(user_input) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Column '{user_input}' is out of bounds. Please enter a column from A to {get_column_label(num_cols - 1)}.")
                continue

            # Check if column is full
            if board[0][col_index] != " ": # If the top row of the column is not empty
                print(f"Column '{user_input}' is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a letter.")


def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if placement was successful, False if the column was full (shouldn't happen with prior validation).
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Column was full


def check_win(board, checker):
    """
    Checks if the given checker has formed a winning sequence (4 in a row)
    horizontally, vertically, or diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - (WIN_SEQUENCE_LENGTH - 1)):
        for c in range(num_cols - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, num_rows):
        for c in range(num_cols - (WIN_SEQUENCE_LENGTH - 1)):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (no empty spaces).
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    """
    Main function to run the Connect 4 game.
    """
    game_board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers for the actual number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = player_checkers[current_player_index]

    game_over = False

    while not game_over:
        print_board(game_board)
        
        col_to_place = get_player_input(current_player_checker, game_board)
        
        # Place the checker
        place_checker(game_board, col_to_place, current_player_checker)

        # Check for a win
        if check_win(game_board, current_player_checker):
            print_board(game_board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for a draw
        elif check_draw(game_board):
            print_board(game_board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = player_checkers[current_player_index]

if __name__ == "__main__":
    main()
