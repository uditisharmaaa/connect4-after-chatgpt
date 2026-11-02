import random
import os

# Constants
ROWS = 6  # Number of rows on the board
COLS = 7  # Number of columns on the board (max is 26)
PLAYERS = 2  # Number of players (max 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for each player

def clear_screen():
    """Clear the console screen."""
    os.system('clear')

def initialize_board():
    """Initialize the game board with blank spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Check if the column is valid and not full."""
    return column.isalpha() and len(column) == 1 and 0 <= ord(column.upper()) - 65 < COLS and board[0][ord(column.upper()) - 65] == " "

def get_column_input():
    """Prompt the player for a column and validate input."""
    while True:
        column = input("Please enter a column: ").strip().upper()
        if is_valid_column(column, board):
            return ord(column) - 65
        print("Invalid column. Try again.")

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row, column

def check_win(board, row, col, checker):
    """Check if the current placement results in a win."""
    # Directions: (row_dir, col_dir)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for row_dir, col_dir in directions:
        count = 1  # Include the placed checker
        # Check in the positive direction
        r, c = row + row_dir, col + col_dir
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += row_dir
            c += col_dir

        # Check in the negative direction
        r, c = row - row_dir, col - col_dir
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= row_dir
            c -= col_dir

        # If four or more checkers are aligned
        if count >= 4:
            return True

    return False

def is_draw(board):
    """Check if the board is full and no moves are possible."""
    return all(board[0][col] != " " for col in range(COLS))

# Initialize game settings
board = initialize_board()
players = [CHECKERS[i] for i in range(PLAYERS)]
random.shuffle(players)  # Randomize player order
turn_index = 0  # Index of the current player

# Game loop
while True:
    print_board(board)
    current_player = players[turn_index]
    print(f"Player {current_player}'s turn.")
    
    column = get_column_input()
    row, col = drop_checker(board, column, current_player)

    # Check for a win
    if check_win(board, row, col, current_player):
        print_board(board)
        print(f"Player {current_player} won!")
        break

    # Check for a draw
    if is_draw(board):
        print_board(board)
        print("It's a draw!")
        break

    # Alternate to the next player
    turn_index = (turn_index + 1) % PLAYERS
