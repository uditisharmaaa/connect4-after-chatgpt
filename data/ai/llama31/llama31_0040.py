import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS_ENABLED = 2

def create_board():
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A", end="")  # print column labels
    for col in range(1, BOARD_COLS):
        print(" ", chr(65 + col), end="")  # A to G
    print()
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLS + "+")  # print row separators
        for col in range(BOARD_COLS):
            print("| " + board[row][col], end=" ")
        print("|")
    print("+---" * BOARD_COLS + "+")  # print row separators

def get_player_checker(player_id):
    """Get the checker for a player"""
    return CHECKERS[player_id % len(CHECKERS)]

def is_valid_input(input_str):
    """Check if the input is a valid column label"""
    return input_str.upper() >= "A" and input_str.upper() <= chr(65 + BOARD_COLS - 1)

def get_col_from_input(input_str):
    """Get the column index from the input string"""
    return ord(input_str.upper()) - 65

def is_column_full(board, col):
    """Check if a column is full"""
    return board[0][col]!= " "

def place_checker(board, col, checker):
    """Place a checker in the given column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return

def check_win(board, checker):
    """Check for a win in the given board"""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def game():
    board = create_board()
    players = [get_player_checker(i) for i in range(PLAYERS_ENABLED)]
    current_player = random.choice(players)
    players.remove(current_player)
    players.insert(0, current_player)

    while True:
        print_board(board)
        print("Player", current_player, ", please enter a column:")
        input_str = input()
        while not is_valid_input(input_str) or is_column_full(board, get_col_from_input(input_str)):
            print("Invalid input. Please enter a valid column.")
            input_str = input()
        col = get_col_from_input(input_str)
        place_checker(board, col, current_player)
        if check_win(board, current_player):
            print_board(board)
            print("Player", current_player, "won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

game()
