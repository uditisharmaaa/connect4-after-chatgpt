import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Board Functions ---

def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear screen

    # Print column labels
    sys.stdout.write("  ")
    for i in range(len(board[0])):
        sys.stdout.write(f"{chr(ord('A') + i)}   ")
    sys.stdout.write("\n")

    # Print board rows
    for r in range(len(board)):
        sys.stdout.write("+")
        for _ in range(len(board[0])):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for c in range(len(board[0])):
            sys.stdout.write(f" {board[r][c]} |")
        sys.stdout.write("\n")

    sys.stdout.write("+")
    for _ in range(len(board[0])):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

def get_column_input(player_checker, num_cols):
    """Gets and validates column input from the player."""
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + num_cols - 1)):
                raise ValueError("Invalid column. Please enter a single letter within the board range.")
            
            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, checker):
    """Drops the checker into the lowest available spot in the column."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r  # Return True and the row where the checker was placed
    return False, -1 # Column is full

# --- Win Condition Functions ---

def check_win(board, checker, last_move_row, last_move_col):
    """Checks if the last move resulted in a win."""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(cols):
        if board[last_move_row][c] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True

    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][last_move_col] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True

    # Check positive diagonal (bottom-left to top-right)
    count = 0
    start_row = last_move_row + last_move_col
    start_col = 0
    if start_row >= rows:
        start_col = start_row - rows + 1
        start_row = rows - 1
    
    r, c = start_row, start_col
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True
        r -= 1
        c += 1

    # Check negative diagonal (top-left to bottom-right)
    count = 0
    start_row = last_move_row - last_move_col
    start_col = 0
    if start_row < 0:
        start_col = -start_row
        start_row = 0
    
    r, c = start_row, start_col
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
        else:
            count = 0
        if count >= WIN_CONDITION:
            return True
        r += 1
        c += 1

    return False

def check_draw(board):
    """Checks if the board is full, resulting in a draw."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        print_board(board)
        current_checker = PLAYER_CHECKERS[current_player_index]

        last_move_row = -1
        last_move_col = -1

        valid_move = False
        while not valid_move:
            col_index = get_column_input(current_checker, NUM_COLS)
            
            placed, last_move_row = drop_checker(board, col_index, current_checker)
            if placed:
                last_move_col = col_index
                valid_move = True
            else:
                print("Column is full. Please choose another column.")

        if check_win(board, current_checker, last_move_row, last_move_col):
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board)  # Print final board
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
