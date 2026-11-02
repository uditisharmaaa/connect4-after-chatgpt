import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with EMPTY_CELL.
    """
    board = []
    for _ in range(rows):
        board.append([EMPTY_CELL] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.
    Includes column labels (A, B, C, ...) and row separators.
    """
    os.system('clear')  # Clear the screen before printing

    # Print column headers (A, B, C, ...)
    header = "  "
    for col_index in range(len(board[0])):
        header += chr(ord('A') + col_index) + "   "
    print(header)

    # Print the board rows
    for row_index in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for col_index in range(len(board[0])):
            row_str += f" {board[row_index][col_index]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def get_column_label(col_index):
    """
    Converts a column index to its corresponding letter label (e.g., 0 -> 'A').
    """
    return chr(ord('A') + col_index)

def get_column_index(column_label):
    """
    Converts a column letter label to its corresponding index (e.g., 'A' -> 0).
    Returns -1 if the label is invalid.
    """
    if len(column_label) == 1 and 'A' <= column_label <= get_column_label(NUM_COLS - 1):
        return ord(column_label) - ord('A')
    return -1

# --- Game Logic Functions ---

def is_valid_column(board, col_index):
    """
    Checks if a column index is within the board boundaries and if the column
    is not already full.
    """
    if 0 <= col_index < len(board[0]):
        return board[0][col_index] == EMPTY_CELL  # Check if the top row of the column is empty
    return False

def drop_checker(board, col_index, player_token):
    """
    Drops a player's checker into the specified column.
    Returns the row index where the checker landed, or -1 if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == EMPTY_CELL:
            board[row_index][col_index] = player_token
            return row_index
    return -1 # Column is full

def check_win(board, player_token, last_row, last_col):
    """
    Checks if the current player has won after placing a checker at (last_row, last_col).
    Checks horizontally, vertically, and both diagonals.
    """
    # Check horizontal
    if check_line(board, player_token, last_row, last_col, 0, 1): return True
    # Check vertical
    if check_line(board, player_token, last_row, last_col, 1, 0): return True
    # Check diagonal (top-left to bottom-right)
    if check_line(board, player_token, last_row, last_col, 1, 1): return True
    # Check diagonal (bottom-left to top-right)
    if check_line(board, player_token, last_row, last_col, 1, -1): return True
    return False

def check_line(board, player_token, r, c, dr, dc):
    """
    Checks for a win condition along a specific direction (dr, dc) from a given cell (r, c).
    Counts consecutive tokens in both forward and backward directions.
    """
    count = 1  # The token at (r, c) itself
    rows = len(board)
    cols = len(board[0])

    # Check forward direction
    for i in range(1, WIN_CONDITION):
        nr, nc = r + dr * i, c + dc * i
        if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player_token:
            count += 1
        else:
            break
    if count >= WIN_CONDITION:
        return True

    # Check backward direction (only if forward didn't win)
    # Reset count to 1 (for the current token) and check backward
    count = 1
    for i in range(1, WIN_CONDITION):
        nr, nc = r - dr * i, c - dc * i
        if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player_token:
            count += 1
        else:
            break
    if count >= WIN_CONDITION:
        return True

    # Combined check (this is more robust for checking around the placed token)
    # The above two 'if count >= WIN_CONDITION' lines are not strictly necessary
    # if the following block is used, but they are kept for conceptual clarity
    # for a first-year student. A better way:
    # count = 0
    # for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
    #     nr, nc = r + dr * i, c + dc * i
    #     if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player_token:
    #         count += 1
    #         if count >= WIN_CONDITION:
    #             return True
    #     else:
    #         count = 0
    # return False

    return False


def is_board_full(board):
    """
    Checks if the entire board is filled with checkers.
    """
    for col_index in range(len(board[0])):
        if board[0][col_index] == EMPTY_CELL: # Check only the top row
            return False
    return True

# --- Main Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winning_player_token = None

    while not game_over:
        current_player_token = PLAYER_TOKENS[current_player_index]
        print_board(board)
        print(f"Player {current_player_token}, please enter a column:")

        column_input = input().strip().upper()
        col_index = get_column_index(column_input)

        if not is_valid_column(board, col_index):
            print("Invalid input or column is full. Please try again.")
            # Player does not lose turn for invalid input
            continue

        # Drop the checker
        row_placed = drop_checker(board, col_index, current_player_token)

        # Check for win
        if check_win(board, current_player_token, row_placed, col_index):
            winning_player_token = current_player_token
            game_over = True
        elif is_board_full(board):
            game_over = True # Draw
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over, print final board and result
    print_board(board)
    if winning_player_token:
        print(f"Player {winning_player_token} won!")
    else:
        print("It's a draw!")

# --- Entry Point ---
if __name__ == "__main__":
    play_game()
