import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Board Functions ---
def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear')  # Clear screen for Linux/Unix
    # os.system('cls') # Use this for Windows if needed

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for i in range(len(board[0])):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


def is_valid_column_input(col_input, num_cols):
    """Checks if the user's column input is valid."""
    if not isinstance(col_input, str) or len(col_input) != 1:
        return False, "Input must be a single letter."
    
    col_input = col_input.upper()
    col_index = ord(col_input) - ord('A')
    
    if not (0 <= col_index < num_cols):
        return False, "Column out of board range."
        
    return True, col_index


def get_next_open_row(board, col):
    """Returns the lowest available row in a given column, or -1 if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1


def drop_checker(board, row, col, checker):
    """Places the checker at the specified location."""
    board[row][col] = checker


# --- Win Condition Functions ---
def check_win(board, checker):
    """Checks if the current player has won the game."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - (WIN_CONDITION - 1)):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - (WIN_CONDITION - 1)):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positively sloped diagonals
    for r in range(rows - (WIN_CONDITION - 1)):
        for c in range(cols - (WIN_CONDITION - 1)):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negatively sloped diagonals
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - (WIN_CONDITION - 1)):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def is_board_full(board):
    """Checks if the board is completely filled."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


# --- Main Game Logic ---
def play_game():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_input = False
        col_index = -1
        while not valid_input:
            user_input = input().upper()
            is_valid, message = is_valid_column_input(user_input, NUM_COLS)
            
            if not is_valid:
                print(f"Invalid input: {message} Please try again.")
                continue
            
            col_index = message # col_index is returned as 'message' when valid
            
            row_to_drop = get_next_open_row(board, col_index)
            if row_to_drop == -1:
                print(f"Column {user_input} is full. Please choose another column.")
            else:
                valid_input = True

        drop_checker(board, row_to_drop, col_index, current_checker)

        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif is_board_full(board):
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = CHECKERS[current_player_index]


if __name__ == "__main__":
    play_game()
