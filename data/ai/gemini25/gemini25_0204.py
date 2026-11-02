import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


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

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print the board content
    for r_idx, row in enumerate(board):
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()

        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()

    # Print the bottom border
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()


def get_column_input(player_checker):
    """
    Gets valid column input from the current player.

    Args:
        player_checker (str): The checker of the current player.

    Returns:
        int: The 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
                continue
            col_idx = ord(col_char) - ord('A')
            return col_idx
        except ValueError:
            print("Invalid input. Please enter a letter.")


def drop_checker(board, col_idx, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_idx (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol for the current player.

    Returns:
        tuple: (True, int) if the checker was successfully placed (row_idx),
               (False, None) if the column is full.
    """
    for r_idx in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r_idx][col_idx] == " ":
            board[r_idx][col_idx] = player_checker
            return True, r_idx
    return False, None  # Column is full


def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the player to check for a win.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontally
    for c_start in range(max(0, last_col - WIN_CONDITION + 1), min(NUM_COLS - WIN_CONDITION + 1, last_col + 1)):
        if all(board[last_row][c] == player_checker for c in range(c_start, c_start + WIN_CONDITION)):
            return True

    # Check vertically
    for r_start in range(max(0, last_row - WIN_CONDITION + 1), min(NUM_ROWS - WIN_CONDITION + 1, last_row + 1)):
        if all(board[r][last_col] == player_checker for r in range(r_start, r_start + WIN_CONDITION)):
            return True

    # Check diagonally (positive slope /)
    for i in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        if last_row + i >= 0 and last_row + i < NUM_ROWS and \
           last_col - i >= 0 and last_col - i < NUM_COLS:
            
            # Find the start of the diagonal sequence
            start_row = last_row + i
            start_col = last_col - i

            # Adjust to the actual top-left of a potential WIN_CONDITION sequence
            while start_row > 0 and start_col < NUM_COLS -1:
                if board[start_row-1][start_col+1] == player_checker: # Check if part of the same sequence
                    start_row -= 1
                    start_col += 1
                else:
                    break
            
            # Iterate through the diagonal from this potential start
            count = 0
            for k in range(WIN_CONDITION):
                r = start_row + k
                c = start_col - k
                if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                    count += 1
                    if count == WIN_CONDITION:
                        return True
                else:
                    count = 0 # Reset count if sequence is broken
    
    # Check diagonally (negative slope \)
    for i in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        if last_row + i >= 0 and last_row + i < NUM_ROWS and \
           last_col + i >= 0 and last_col + i < NUM_COLS:

            # Find the start of the diagonal sequence
            start_row = last_row + i
            start_col = last_col + i

            # Adjust to the actual top-left of a potential WIN_CONDITION sequence
            while start_row > 0 and start_col > 0:
                if board[start_row-1][start_col-1] == player_checker:
                    start_row -= 1
                    start_col -= 1
                else:
                    break
            
            # Iterate through the diagonal from this potential start
            count = 0
            for k in range(WIN_CONDITION):
                r = start_row + k
                c = start_col + k
                if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == player_checker:
                    count += 1
                    if count == WIN_CONDITION:
                        return True
                else:
                    count = 0 # Reset count if sequence is broken

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False  # There's an empty space
    return True  # Board is full


# --- Main Game Logic ---
def play_game():
    """
    Runs the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_move_row = -1
    last_move_col = -1

    while not game_over:
        current_player_checker = CHECKERS[current_player_idx]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_input = get_column_input(current_player_checker)

            # Validate column is not full
            if board[0][col_input] != " ":
                print(f"Column {chr(ord('A') + col_input)} is full. Please choose another column.")
                continue

            placed, row_idx = drop_checker(board, col_input, current_player_checker)
            if placed:
                last_move_row = row_idx
                last_move_col = col_input
                valid_turn = True
            else:
                # This case should ideally not be reached if the column full check above works
                print(f"Error placing checker in column {chr(ord('A') + col_input)}. Please try again.")

        print_board(board)  # Print board after successful move

        if check_win(board, current_player_checker, last_move_row, last_move_col):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
