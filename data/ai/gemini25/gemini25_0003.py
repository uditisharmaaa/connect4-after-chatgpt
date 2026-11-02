import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def clear_screen():
    """Clears the terminal screen."""
    # 'cls' for Windows, 'clear' for Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(chr(ord('A') + i) for i in range(NUM_COLS)))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---+" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---+" * NUM_COLS + "+")

# --- Game Logic Functions ---

def get_player_move(player_checker, current_player_index, num_players_total):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            prompt = f"Player {player_checker} (Player {current_player_index + 1} of {num_players_total}), please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter for the column (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Column '{col_char}' is out of board range. Please enter a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print("Invalid input. Please enter a single letter for the column.")

def drop_checker(board, col, checker):
    """
    Drops the checker into the lowest available position in the given column.
    Returns True if successful, False if the column is full.
    """
    if not (0 <= col < NUM_COLS):
        # This shouldn't happen if get_player_move validates correctly,
        # but good for robustness.
        return False

    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r  # Return True and the row where it was placed
    return False, -1 # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker at (last_row, last_col).
    Checks horizontally, vertically, and both diagonals.
    """
    # Helper function to count consecutive checkers in a direction
    def count_consecutive(delta_row, delta_col):
        count = 0
        # Check in one direction
        r, c = last_row, last_col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Helper function to check a line (e.g., horizontal, vertical, diagonal)
    def check_line(dr1, dc1, dr2, dc2):
        # Count in one direction from last_row, last_col (inclusive)
        count1 = count_consecutive(dr1, dc1)
        # Count in the opposite direction from one step away from last_row, last_col
        # e.g., if (dr1,dc1) is (0,1) for right, then (-dr1,-dc1) is (0,-1) for left
        # We start from one step away from the current checker to avoid double counting the checker itself
        count2 = count_consecutive(-dr1, -dc1) -1 # Subtract 1 because 'last_row, last_col' itself is counted in both directions
        return (count1 + count2) >= WIN_CONDITION


    # Check horizontally
    # count to the right from last_col
    right_count = 0
    for c in range(last_col, NUM_COLS):
        if board[last_row][c] == checker:
            right_count += 1
        else:
            break
    # count to the left from last_col-1
    left_count = 0
    for c in range(last_col - 1, -1, -1):
        if board[last_row][c] == checker:
            left_count += 1
        else:
            break
    if (right_count + left_count) >= WIN_CONDITION:
        return True


    # Check vertically (only downwards needed from the placed checker)
    vertical_count = 0
    for r in range(last_row, NUM_ROWS):
        if board[r][last_col] == checker:
            vertical_count += 1
        else:
            break
    if vertical_count >= WIN_CONDITION:
        return True

    # Check primary diagonal (top-left to bottom-right)
    # count up-left
    up_left_count = 0
    r, c = last_row, last_col
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
        up_left_count += 1
        r -= 1
        c -= 1
    # count down-right (starting from one step away from last_row,last_col)
    down_right_count = 0
    r, c = last_row + 1, last_col + 1
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
        down_right_count += 1
        r += 1
        c += 1
    if (up_left_count + down_right_count) >= WIN_CONDITION:
        return True

    # Check secondary diagonal (top-right to bottom-left)
    # count up-right
    up_right_count = 0
    r, c = last_row, last_col
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
        up_right_count += 1
        r -= 1
        c += 1
    # count down-left (starting from one step away from last_row,last_col)
    down_left_count = 0
    r, c = last_row + 1, last_col - 1
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
        down_left_count += 1
        r += 1
        c -= 1
    if (up_right_count + down_left_count) >= WIN_CONDITION:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is full (no more empty spaces).
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces, it's a draw

# --- Main Game Loop ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)

    if NUM_COLS > 26:
        print("Error: Number of columns cannot exceed 26 (due to A-Z labeling).")
        sys.exit(1)

    if WIN_CONDITION < 2:
        print("Error: Win condition must be at least 2.")
        sys.exit(1)

    # Prepare player checkers
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Initialize board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker} (Player {current_player_index + 1} of {NUM_PLAYERS}), it's your turn.")

        col_input_valid = False
        last_placed_row = -1
        last_placed_col = -1

        while not col_input_valid:
            chosen_col = get_player_move(current_player_checker, current_player_index, NUM_PLAYERS)
            successful_drop, dropped_row = drop_checker(board, chosen_col, current_player_checker)

            if successful_drop:
                last_placed_row = dropped_row
                last_placed_col = chosen_col
                col_input_valid = True
            else:
                print(f"Column {chr(ord('A') + chosen_col)} is full. Please choose another column.")
                # The turn is NOT lost, player is asked again

        # After placing the checker, print the updated board
        print_board(board)

        # Check for win
        if check_win(board, current_player_checker, last_placed_row, last_placed_col):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over. Thanks for playing!")

if __name__ == "__main__":
    main()
