import os
import random

# Constant variables
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def validate_input(column):
    """Validate user input."""
    if column.isdigit():
        return False
    column = column.upper()
    if column < 'A' or column > chr(ord('A') + COLUMNS - 1):
        return False
    return True

def get_column_index(column):
    """Get the column index from the user input."""
    return ord(column.upper()) - ord('A')

def drop_checker(board, column, checker):
    """Drop the checker into the column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_win(board, checker):
    """Check for a win in all directions."""
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell!= " " for row in board for cell in row)

def game():
    """Start the game."""
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_player = players[current_player_index]
        print("Player {}, please enter a column:".format(current_player))
        column = input()
        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue
        column_index = get_column_index(column)
        if board[0][column_index]!= " ":
            print("Column is full. Please try again.")
            continue
        drop_checker(board, column_index, current_player)
        print_board(board)
        if check_win(board, current_player):
            print("Player {} won!".format(current_player))
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

game()
