import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- FUNCTIONS ---

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
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(NUM_COLS):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers and borders
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

def get_column_input(prompt):
    """
    Gets and validates the user's column input.
    Returns the 0-indexed column number if valid, otherwise continually prompts.
    """
    while True:
        try:
            user_input = input(prompt).strip().upper()
            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            col_char = user_input[0]
            if len(user_input) > 1:
                print("Please enter only one column letter.")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except TypeError:
            print("Invalid input type. Please enter a letter.")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space of the given column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index, col_index
    return False, -1, -1 # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the given checker has won the game after the last move.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    count = 0
    for col in range(NUM_COLS):
        if board[last_row][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for row in range(NUM_ROWS):
        if board[row][last_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start at the top-leftmost cell of the diagonal that contains (last_row, last_col)
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)
    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    # Check anti-diagonal (top-right to bottom-left)
    count = 0
    # Start at the top-rightmost cell of the anti-diagonal that contains (last_row, last_col)
    start_row = last_row - min(last_row, NUM_COLS - 1 - last_col)
    start_col = last_col + min(last_row, NUM_COLS - 1 - last_col)
    while start_row < NUM_ROWS and start_col >= 0:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col -= 1

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, not a draw
    return True # All cells are full

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = players[current_player_index]

    game_over = False
    winner = None

    while not game_over:
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        col_index = get_column_input(f"Enter column (A-{chr(ord('A') + NUM_COLS - 1)}): ")

        placed_successfully, last_row, last_col = place_checker(board, col_index, current_player_checker)

        if not placed_successfully:
            print("Column is full. Please choose another column.")
            # Player does not lose turn, continue to next iteration for same player
            continue

        if check_win(board, current_player_checker, last_row, last_col):
            print_board(board)
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = players[current_player_index]

    # Game end messages
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
