import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the Connect 4 board."""
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

# --- Game Logic ---

def get_player_input(player_checker, current_player_index):
    """Gets and validates column input from the player."""
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')
            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print("Invalid column. Please enter a column within the board limits.")
        except Exception:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")

def place_checker(board, col_index, player_checker):
    """Places the checker in the lowest available space in the chosen column."""
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, (r, col_index)  # Return success and position
    print("Column is full! Please choose another column.")
    return False, None  # Column is full

def check_win(board, last_pos, player_checker):
    """Checks if the last placed checker results in a win."""
    if last_pos is None:  # No checker was placed (e.g., column full)
        return False

    r, c = last_pos

    # Check horizontal
    count = 0
    for col in range(NUM_COLS):
        if board[r][col] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for row in range(NUM_ROWS):
        if board[row][c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = r - min(r, c)
    start_col = c - min(r, c)
    for i in range(min(NUM_ROWS - start_row, NUM_COLS - start_col)):
        curr_r, curr_c = start_row + i, start_col + i
        if board[curr_r][curr_c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-right to bottom-left)
    count = 0
    start_row = r - min(r, NUM_COLS - 1 - c)
    start_col = c + min(r, NUM_COLS - 1 - c)
    for i in range(min(NUM_ROWS - start_row, start_col + 1)):
        curr_r, curr_c = start_row + i, start_col - i
        if board[curr_r][curr_c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    return False

def check_draw(board):
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's still an empty space
    return True  # Board is full

# --- Main Game Loop ---

def play_game():
    """Manages the main Connect 4 game flow."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_found = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_placement = False
        last_placed_position = None
        while not valid_placement:
            col_to_place = get_player_input(current_player_checker, current_player_index)
            valid_placement, last_placed_position = place_checker(board, col_to_place, current_player_checker)

        if check_win(board, last_placed_position, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
