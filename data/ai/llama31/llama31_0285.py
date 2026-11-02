import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
MAX_PLAYERS = 5

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    board = []
    for _ in range(BOARD_ROWS):
        row = [" "] * BOARD_COLS
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print("\n+---+---+---+---+---+---+---+")

def get_column_index(column):
    """Convert a column letter to a column index."""
    return ord(column.upper()) - ord('A')

def is_valid_input(column):
    """Check if the user input is a valid column."""
    return column.upper() >= 'A' and column.upper() <= chr(ord('A') + BOARD_COLS - 1)

def drop_checker(board, player, column):
    """Drop a checker into a column."""
    column_index = get_column_index(column)
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = CHECKERS[player]
            return

def check_win(board, player):
    """Check if a player has won."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row][col + 1] == CHECKERS[player] and board[row][col + 2] == CHECKERS[player] and board[row][col + 3] == CHECKERS[player]:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == CHECKERS[player] and board[row + 1][col] == CHECKERS[player] and board[row + 2][col] == CHECKERS[player] and board[row + 3][col] == CHECKERS[player]:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row + 1][col + 1] == CHECKERS[player] and board[row + 2][col + 2] == CHECKERS[player] and board[row + 3][col + 3] == CHECKERS[player]:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row - 1][col + 1] == CHECKERS[player] and board[row - 2][col + 2] == CHECKERS[player] and board[row - 3][col + 3] == CHECKERS[player]:
                return True

    return False

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
    players = [i for i in range(PLAYERS)]
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board)
        print("Player", CHECKERS[players[current_player]], "please enter a column:")
        column = input()
        while not is_valid_input(column):
            print("Invalid input. Please enter a column letter (A-G):")
            column = input()
        drop_checker(board, players[current_player], column)
        if check_win(board, players[current_player]):
            print_board(board)
            print("Player", CHECKERS[players[current_player]], "won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

game()
