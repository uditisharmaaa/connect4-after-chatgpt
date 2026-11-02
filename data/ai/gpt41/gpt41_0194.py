import os
import random
import string

# -----------------------
# CONSTANTS / SETTINGS
# -----------------------
ROWS = 6
COLS = 7
MAX_COLS = 26   # For flexible future extensions, column labels up to 'Z'
PLAYERS = 2     # (Can be 2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]

# -------------------------------------
# Function to clear the terminal screen
# -------------------------------------
def clear_screen():
    os.system('clear')  # For Linux/Unix

# ------------------------------------------
# Function to initialize the empty game board
# ------------------------------------------
def create_board(rows, cols):
    # Create a 2D board with ' ' (spaces)
    return [[" " for _ in range(cols)] for _ in range(rows)]

# ------------------------------------------
# Function to print the current game board
# ------------------------------------------
def print_board(board):
    cols = len(board[0])
    # Print column labels
    headers = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(headers)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

# -----------------------------------------------
# Function to get and validate the user's move
# -----------------------------------------------
def get_valid_column_input(board, current_player_name):
    cols = len(board[0])
    valid_inputs = set(string.ascii_uppercase[:cols])
    input_prompt = f"Player {current_player_name}, please enter a column: "
    while True:
        user_input = input(input_prompt).strip().upper()
        if len(user_input) != 1 or user_input not in valid_inputs:
            print(f"Invalid input! Please enter a letter A-{string.ascii_uppercase[cols-1]}.")
            continue
        col_index = string.ascii_uppercase.index(user_input)
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn!")
            return None   # This denotes a lost turn due to full column
        else:
            return col_index

# ----------------------------------------------
# Function to place a checker in the board
# ----------------------------------------------
def place_checker(board, col_index, checker):
    rows = len(board)
    # Place the checker in the lowest available space in the column
    for row in reversed(range(rows)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index   # Return position for win-checking

# ----------------------------------------------
# Check if a player has won after placing a disc
# ----------------------------------------------
def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for d_row, d_col in directions:
        count = 1
        # Check in the positive direction
        r, c = row + d_row, col + d_col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += d_row
            c += d_col
        # Check in the negative direction
        r, c = row - d_row, col - d_col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= d_row
            c -= d_col
        if count >= 4:
            return True
    return False

# -------------------------------------------
# Function to check for a draw
# -------------------------------------------
def check_draw(board):
    # If there is any empty cell in the top row, game is not a draw
    return all(cell != " " for cell in board[0])

# -------------------------------------------
# Main game loop
# -------------------------------------------
def main():
    # Setup players
    player_checkers = CHECKERS[:PLAYERS]
    board = create_board(ROWS, COLS)
    # Randomly pick the first player
    current_player = random.randint(0, PLAYERS-1)

    clear_screen()
    print_board(board)

    while True:
        checker = player_checkers[current_player]

        col_index = get_valid_column_input(board, checker)

        # If column is full, player loses turn (do nothing else this round)
        if col_index is None:
            # Next player's turn
            current_player = (current_player + 1) % PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place the checker
        row, col = place_checker(board, col_index, checker)

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

# -------------------------------------------
# Run the program
# -------------------------------------------
if __name__ == "__main__":
    main()
