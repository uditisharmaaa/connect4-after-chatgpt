import os
import random
import string

# Constants for settings
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2                # Set to 2 for submission
CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY = " "

# Helper to clear screen
def clear_screen():
    os.system('clear')

# Initialize board (ROWS x COLUMNS filled with EMPTY)
def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

# Print the board as specified in the assignment
def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, C ...)
    print("  ", end="")
    for i in range(cols):
        print(f" {string.ascii_uppercase[i]}  ", end="")
    print()
    print("+" + "---+" * cols)
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * cols)

# Get the player's move, make sure it's valid
def get_valid_move(board, valid_columns):
    cols = len(board[0])
    while True:
        move = input("Please enter a column: ").strip().upper()
        if len(move) != 1 or move not in valid_columns:
            print(f"Invalid input. Please enter a letter A-{valid_columns[-1]}.")
            continue
        col_num = string.ascii_uppercase.index(move)
        # Check if the column is not full
        if board[0][col_num] != EMPTY:
            print("Column is full. You lose your turn!")
            return None
        return col_num

# Drop checker in the lowest empty spot in the selected column
def place_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY:
            board[row][col] = checker
            return row, col
    return None # Shouldn't be reached if we check for full columns before

# Check if the last move wins the game
def check_for_win(board, row, col, checker):
    directions = [
        (0,1),      # horizontal
        (1,0),      # vertical
        (1,1),      # diagonal down-right
        (1,-1)      # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in both directions
        for dir in [1, -1]:
            r, c = row, col
            while True:
                r += dr * dir
                c += dc * dir
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

# Check if the game board is full (draw)
def is_draw(board):
    return all(cell != EMPTY for cell in board[0])

# Main Game Function
def connect4():
    # Prepare players
    num_players = NUM_PLAYERS
    # Error check on max allowed
    if not (2 <= num_players <= 5):
        print("Number of players must be between 2 and 5.")
        return

    player_symbols = CHECKERS[:num_players]
    # Which columns are valid for player input
    valid_columns = string.ascii_uppercase[:COLUMNS]

    # Create the board
    board = create_board(ROWS, COLUMNS)
    # Randomly select starting player
    current_player = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {player_symbols[current_player]} starts!")

    # Game loop
    while True:
        print_board(board)
        print(f"Player {player_symbols[current_player]}, ", end="")
        col = get_valid_move(board, valid_columns)
        # If col is None, player's turn is lost (full column)
        if col is not None:
            row, col_actual = place_checker(board, col, player_symbols[current_player])
            # Check for win
            if check_for_win(board, row, col_actual, player_symbols[current_player]):
                print_board(board)
                print(f"Player {player_symbols[current_player]} won!")
                break
            # Check for draw
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break
        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    connect4()
