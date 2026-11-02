import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def create_board():
    """Create a 2D board with all elements initialized to whitespace."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_num):
    """Return the checker for the given player."""
    return CHECKERS[player_num - 1]

def get_column_index(column):
    """Return the column index for the given column letter."""
    return ord(column.upper()) - ord('A')

def is_valid_input(column):
    """Check if the input column is valid."""
    return column.upper().isalpha() and get_column_index(column) < NUM_COLS

def is_valid_move(board, column):
    """Check if the move is valid (column not full)."""
    return board[0][get_column_index(column)] == " "

def get_next_open_row(board, column):
    """Return the next open row in the given column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][get_column_index(column)] == " ":
            return row

def drop_checker(board, column, checker):
    """Drop the checker in the given column."""
    row = get_next_open_row(board, column)
    board[row][get_column_index(column)] = checker

def check_win(board, checker):
    """Check for a win in the given direction."""
    # Check horizontal locations for win
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def game():
    """Play the Connect 4 game."""
    board = create_board()
    players = [get_player_checker(i) for i in range(1, NUM_PLAYERS + 1)]
    current_player = random.choice(players)
    print("Player", current_player, "is chosen to play first.")

    while True:
        print_board(board)
        column = input("Player {}, please enter a column: ".format(current_player))
        if not is_valid_input(column):
            print("Invalid input. Please enter a letter between A and G.")
            continue
        if not is_valid_move(board, column):
            print("Column is full. Please choose another column.")
            continue
        drop_checker(board, column, current_player)
        if check_win(board, current_player):
            print_board(board)
            print("Player", current_player, "won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

game()
