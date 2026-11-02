import os
import random
import sys

# Constants (can be changed for testing, defaults for submission as required)
ROWS = 6
COLS = 7       # Must be <= 26 for column letter label
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Check board dimensions
if COLS > 26 or COLS < 1 or ROWS < 1 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Invalid board size or number of players. Exiting.")
    sys.exit(1)

# Board initialization
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    # Print columns headers (A-G, etc.)
    print("  ", end="")
    for c in range(len(board[0])):
        print(f" {chr(ord('A') + c)} ", end=" ")
    print()
    # Print horizontal separator
    print("+" + "---+" * len(board[0]))
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * len(board[0]))

# Get valid columns (not full)
def get_valid_columns(board):
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid.append(col)
    return valid

# Insert a checker for a player in the chosen column
# Returns True if successfully placed, False if column is full
def place_checker(board, col, symbol):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col
    return None

# Checks if move resulted in a win
def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    # Directions: right, down, diag down-right, diag up-right
    dirs = [ (0,1), (1,0), (1,1), (-1,1) ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in dirs:
                count = 1
                rr, cc = r + dr, c + dc
                while (0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol):
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

# Check if board is full
def is_draw(board):
    return all(cell != " " for cell in board[0])

# Validate user input
def validate_input(inp, valid_columns):
    inp = inp.strip().upper()
    if len(inp) != 1 or not inp.isalpha():
        return False, None
    col = ord(inp) - ord('A')
    if col < 0 or col >= COLS:
        return False, None
    if col not in valid_columns:
        return True, None   # Column exists but is full; lose turn
    return True, col       # Valid

def main():
    board = create_board(ROWS, COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    player_names = [f"Player {players[i]}" for i in range(NUM_PLAYERS)]
    curr_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial print
    print_board(board)
    print(f"{player_names[curr_player_idx]} starts!")

    # Main game loop
    move_count = 0
    while True:
        player_symbol = players[curr_player_idx]
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print_board(board)
            print("The board is full! It's a draw!")
            break

        print_board(board)
        print(f"{player_names[curr_player_idx]}, please enter a column:")

        # Get and validate user input
        while True:
            user_input = input().strip()
            is_valid, col = validate_input(user_input, valid_columns)

            # Input invalid format or out of range
            if not is_valid:
                print(f"Invalid input '{user_input}'. Please enter a valid column:")
                continue
            # Input is column label, but column is full
            if col is None:
                print(f"Column {user_input.upper()} is full. You lose your turn.")
                # Lose turn if column full per instructions
                break
            # Place checker, check for win/draw
            pos = place_checker(board, col, player_symbol)
            move_count += 1
            # Check for win
            if check_win(board, player_symbol):
                print_board(board)
                print(f"{player_names[curr_player_idx]} won!")
                return
            if is_draw(board):
                print_board(board)
                print("The board is full! It's a draw!")
                return
            # Alternate player
            curr_player_idx = (curr_player_idx + 1) % NUM_PLAYERS
            break  # next turn

        else:
            # Only reached if the user never enters valid input (shouldn't happen)
            continue
        # If column was full and user loses turn, alternate player
        if col is None:
            curr_player_idx = (curr_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
