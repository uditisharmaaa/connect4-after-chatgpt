import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def create_board():
    """Initialize the Connect 4 board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_column_choice():
    """Get and validate the column choice from the user."""
    while True:
        choice = input("Player {}, please enter a column: ".format(current_player)).strip().upper()
        if len(choice) == 1 and choice.isalpha() and 'A' <= choice < chr(ord('A') + COLUMNS):
            return ord(choice) - ord('A')
        print("Invalid input. Please enter a valid column.")

def get_next_open_row(board, col):
    """Get the next open row in the given column."""
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, row, col, checker):
    """Place a checker in the board at the specified location."""
    board[row][col] = checker

def check_win(board, checker):
    """Check for a win in all directions."""
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == checker:
                return True

    # Check vertical locations
    for r in range(ROWS-3):
        for c in range(COLUMNS):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLUMNS-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS-3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == checker:
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is filled)."""
    return all(board[0][c] != " " for c in range(COLUMNS))

# Game setup
board = create_board()
current_player_index = random.randint(0, NUM_PLAYERS - 1)
current_player = PLAYER_TOKENS[current_player_index]

print_board(board)

# Game loop
while True:
    col_choice = get_column_choice()
    row_choice = get_next_open_row(board, col_choice)

    if row_choice is None:
        print("Column is full. Player {} loses turn.".format(current_player))
    else:
        place_checker(board, row_choice, col_choice, current_player)
        print_board(board)

        if check_win(board, current_player):
            print("Player {} won!".format(current_player))
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = PLAYER_TOKENS[current_player_index]
