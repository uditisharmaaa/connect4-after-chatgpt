import os
import random

# Constant variables
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} |".format(" | ".join(row)))
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_index):
    """Get the checker for the given player."""
    return CHECKERS[player_index]

def is_valid_input(column):
    """Check if the input is a valid column."""
    return column.upper() >= 'A' and column.upper() <= chr(ord('A') + COLUMNS - 1)

def is_column_full(board, column):
    """Check if the column is full."""
    return board[0][ord(column.upper()) - ord('A')]!= " "

def get_next_open_row(board, column):
    """Get the next open row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][ord(column.upper()) - ord('A')] == " ":
            return row

def drop_checker(board, column, checker):
    """Drop the checker in the given column."""
    row = get_next_open_row(board, column)
    board[row][ord(column.upper()) - ord('A')] = checker

def check_for_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def play_game():
    """Play the Connect 4 game."""
    board = create_board()
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        os.system('clear')
        print_board(board)
        checker = get_player_checker(players[current_player])
        print("Player", checker, ", please enter a column:")

        column = input().strip()
        while not is_valid_input(column) or is_column_full(board, column):
            print("Invalid input. Please enter a valid column:")
            column = input().strip()

        drop_checker(board, column, checker)

        if check_for_win(board, checker):
            os.system('clear')
            print_board(board)
            print("Player", checker, "won!")
            break

        if all(all(cell!= " " for cell in row) for row in board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
