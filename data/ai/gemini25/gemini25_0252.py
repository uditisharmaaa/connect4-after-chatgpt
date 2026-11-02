import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print()

    # Print board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

# --- Game Logic ---
def get_player_input(current_player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.
    Keeps asking until a valid input is received.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_char:
                print("Error: Input cannot be empty. Please enter a column letter.")
                continue

            col_index = string.ascii_uppercase.find(col_char)

            if col_index == -1:
                print("Error: Invalid column letter. Please enter a letter from A to "
                      f"{string.ascii_uppercase[board_cols - 1]}.")
            elif col_index >= board_cols:
                print("Error: Column out of bounds. Please enter a letter from A to "
                      f"{string.ascii_uppercase[board_cols - 1]}.")
            else:
                return col_index
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def place_checker(board, col, player_checker):
    """
    Places the player's checker in the lowest available space of the given column.
    Returns True if successful, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True, row, col  # Return success and the position
    return False, -1, -1 # Column is full

def check_win(board, player_checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker at (last_row, last_col).
    Checks horizontally, vertically, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for c in range(max(0, last_col - (WIN_CONDITION - 1)), min(cols - (WIN_CONDITION - 1), last_col + 1)):
        if all(board[last_row][c + i] == player_checker for i in range(WIN_CONDITION)):
            return True

    # Check vertical
    for r in range(max(0, last_row - (WIN_CONDITION - 1)), min(rows - (WIN_CONDITION - 1), last_row + 1)):
        if all(board[r + i][last_col] == player_checker for i in range(WIN_CONDITION)):
            return True

    # Check diagonal (top-left to bottom-right)
    # Iterate through possible starting points of a WIN_CONDITION-long diagonal segment
    for r_offset in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        for c_offset in range(-(WIN_CONDITION - 1), WIN_CONDITION):
            start_row = last_row + r_offset
            start_col = last_col + c_offset

            if 0 <= start_row <= rows - WIN_CONDITION and \
               0 <= start_col <= cols - WIN_CONDITION:
                if all(board[start_row + i][start_col + i] == player_checker for i in range(WIN_CONDITION)):
                    return True

    # Check diagonal (bottom-left to top-right)
    # Iterate through possible starting points of a WIN_CONDITION-long diagonal segment
    for r_offset in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        for c_offset in range(-(WIN_CONDITION - 1), WIN_CONDITION):
            start_row = last_row + r_offset
            start_col = last_col + c_offset

            if 0 <= start_row <= rows - WIN_CONDITION and \
               WIN_CONDITION - 1 <= start_col <= cols - 1:
                if all(board[start_row + i][start_col - i] == player_checker for i in range(WIN_CONDITION)):
                    return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        if " " in row:
            return False
    return True

def get_next_player_index(current_player_index, total_players):
    """
    Determines the index of the next player.
    """
    return (current_player_index + 1) % total_players

# --- Main Game Loop ---
def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: Number of players must be between 2 and 5.")
        return
    if NUM_COLS > len(string.ascii_uppercase):
        print(f"Error: Maximum number of columns supported is {len(string.ascii_uppercase)}.")
        return

    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players_checkers = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner = None

    print_board(board)
    print(f"Player {players_checkers[current_player_index]} goes first!")

    while not game_over:
        current_player_checker = players_checkers[current_player_index]

        # Get valid column input
        col_to_place = get_player_input(current_player_checker, NUM_COLS)

        # Place checker
        placed_successfully, last_row, last_col = place_checker(board, col_to_place, current_player_checker)

        if not placed_successfully:
            print("Error: That column is full. Please choose another column.")
            # Player does not lose turn, continue to next iteration of loop for same player
            continue

        print_board(board)

        # Check for win
        if check_win(board, current_player_checker, last_row, last_col):
            winner = current_player_checker
            game_over = True
            print(f"Player {winner} won!")
        # Check for draw if no win
        elif check_draw(board):
            game_over = True
            print("It's a draw!")
        else:
            # Switch to the next player
            current_player_index = get_next_player_index(current_player_index, NUM_PLAYERS)

if __name__ == "__main__":
    main()
